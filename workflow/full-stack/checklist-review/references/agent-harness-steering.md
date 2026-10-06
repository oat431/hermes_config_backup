# Agent Harness Steering Conventions (2026)

Depth for writing/maintaining the `claude-driven.md` + `general-agents-driven.md` checklists. Distilled from the agents.md open standard and per-vendor docs, researched 2026-09.

## The two-channel rule (most important)

**Persona and project memory are different channels — never conflate them.**

- **Persona** ("who I am / how I work": voice, principles, boundaries, decision style) rides the *system-prompt channel*, which carries the highest instruction-following weight. Mechanisms per tool below.
- **Project memory** ("this repo's facts": commands, layout, architecture, conventions, red lines) lives in the always-loaded instruction file (`CLAUDE.md` / `AGENTS.md`).
- Dumping a full persona into the memory file wastes context AND lowers adherence — the more instructions, the weaker each one. Distill a persona to ~10 lines (identity, mission, 3–5 non-negotiables, how decisions get framed) when seeding it from a SOUL.md. Copy/adapt; never reference a machine-local path.

## Instruction files (per tool)

| Tool | Instruction file(s) | Config | Notes |
|---|---|---|---|
| **Codex CLI** (OpenAI) | `AGENTS.md` (root + nested, closest-wins) + `~/.codex/AGENTS.md` (user) | `~/.codex/config.toml` | Approval modes `read-only`/`auto`/`full-auto`; sandbox; subagents via TOML; **no `.codex/commands/` yet**; reasoning-effort dial; headless `codex exec` |
| **Qwen Code** | `AGENTS.md` + `QWEN.md` | `settings.json` (shared w/ desktop) | Forked from Gemini CLI, diverged; multi-protocol, OpenAI-compatible; local via llama-server/LM Studio; has commands/agents/skills/MCP |
| **Gemini CLI** (Google) | `GEMINI.md` (hierarchical: `~/.gemini/GEMINI.md` + root→leaf) | `.gemini/settings.json` (can set `context.fileName` → AGENTS.md) | ⚠️ **being sunset in favor of Antigravity** — target Antigravity for new projects |
| **Antigravity** (Google) | Rules (markdown, size-limited) | workflows + skills + `agy` CLI | Agent Manager, async agents, dedicated browser subagent, custom tools + lifecycle hooks + declarative safety policies |
| **Cursor** | `AGENTS.md` + `.cursor/rules/*.mdc` | frontmatter `description` + `alwaysApply`/`globs` | legacy `.cursorrules` deprecated |
| **GitHub Copilot** | `AGENTS.md` + `.github/copilot-instructions.md` | VS Code/GitHub settings | thin "follow AGENTS.md" delta |
| **Claude Code** (Anthropic) | `CLAUDE.md` | `.claude/` (settings.json, rules/, skills/, agents/, output-styles/) | full steering stack below |

**AGENTS.md is the cross-tool standard** — write once, every tool reads it. Tool-specific files are *thin deltas pointing at AGENTS.md*, never duplicated rules. Commit only the harness config the team actually uses; dead config is noise.

## Claude Code steering stack (the five tools + when)

- **CLAUDE.md** — always-on facts: commands, layout, architecture constraints, conventions. Start late, grow on error; every line earns its place.
- **`.claude/rules/`** — path-scoped constraints (frontmatter `paths:`). "This file/zone must X" → scoped rule, not CLAUDE.md.
- **`.claude/skills/`** — procedural knowledge (deploy runbooks, release checklists, review processes). Body loads on invoke (progressive disclosure); only name+description load at start. A 30-line procedure in CLAUDE.md is a smell.
- **`.claude/agents/`** — isolated subagents; body = their system prompt (and persona). Clutter-producing side tasks (search, audit) → subagent; steerable procedure → skill. Second-opinion reviewer = fresh model, different family.
- **Hooks** (`settings.json`) — *deterministic* enforcement. "Never do X" → `PreToolUse` hook (exit code 2), NOT an instruction — instructions fail under pressure/injection. "Every time X, do Y" → `PostToolUse`. Stop hook = quality gate. Command/HTTP/mcp_tool are deterministic; prompt/agent hooks use judgment.
- **Permissions** — deny-by-default allowlist; `--dangerously-skip-permissions` only in a sandbox.
- **Output styles** (`.claude/output-styles/`) — persona in the system prompt. ⚠️ a custom style *replaces* the default engineering behavior unless `keep-coding-instructions: true`. Check built-ins (Proactive/Explanatory/Learning) first. `--append-system-prompt` is additive + per-invocation.
- **MCP** (`.mcp.json`) + **plugins** bundle the whole setup for teammates.

## Verification discipline (cross-tool)

- Every task has a runnable pass/fail check (tests/build/lint/screenshot diff); agent shows command + output.
- Layered verification: in-prompt "run until green" → deterministic gate (hook/CI) → second-opinion model. Pick layer by risk tier.
- "Fix root cause, never suppress" is an instruction-file red line (no bare `except:`, no fake fallback, no disabling the failing test).
- Context: fresh context per task; compaction *preserves* wrong assumptions (so /clear + sharper prompt, not /compact); heavy research → subagent.

## Why this matters for the checklist library

The agent-driven pair is "build with AI agents", distinct from `ai.md` ("build an AI product"). The 2-layer split mirrors the web family: general file = OS (task decomposition, verification, orchestration, review gates), tool file = driver's manual (one vendor's steering stack). Both carry the 7-tier matrix + Mermaid flowchart.
