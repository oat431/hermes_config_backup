// Real-parser check for ```mermaid blocks in a markdown note.
// Setup (once): npm install mermaid jsdom
// Run from the directory holding node_modules:  node mermaid_parse_check.mjs "F:/path/to/note.md"
// Exit codes: 0 = all blocks parse, 1 = at least one failure, 2 = usage error.
import fs from 'node:fs';
import { JSDOM } from 'jsdom';

const dom = new JSDOM('<!DOCTYPE html><html><body></body></html>');
globalThis.window = dom.window;
globalThis.document = dom.window.document;
// Node 22: globalThis.navigator is getter-only; override via defineProperty.
Object.defineProperty(globalThis, 'navigator', { value: dom.window.navigator, configurable: true });

const { default: mermaid } = await import('mermaid');
mermaid.initialize({ startOnLoad: false });

const path = process.argv[2];
if (!path) {
  console.error('usage: node mermaid_parse_check.mjs <note.md>');
  process.exit(2);
}

const lines = fs.readFileSync(path, 'utf8').split(/\r?\n/);
const blocks = [];
let inBlock = false;
let startLine = 0;
let buf = [];
for (let i = 0; i < lines.length; i++) {
  const line = lines[i];
  if (!inBlock && line.trim().startsWith('```mermaid')) {
    inBlock = true;
    startLine = i + 1;
    buf = [];
    continue;
  }
  if (inBlock && line.trim().startsWith('```')) {
    blocks.push({ startLine, text: buf.join('\n') });
    inBlock = false;
    continue;
  }
  if (inBlock) buf.push(line);
}

let failures = 0;
for (const block of blocks) {
  try {
    await mermaid.parse(block.text);
    console.log(`OK   block at line ${block.startLine}`);
  } catch (err) {
    failures++;
    console.log(`FAIL block at line ${block.startLine}: ${String((err && err.message) || err)}`);
  }
}
console.log(`\n${blocks.length} mermaid blocks, ${failures} failures`);
process.exit(failures ? 1 : 0);
