#!/usr/bin/env python3
"""Mechanical kode-thai pre-check for Thai prose files.

Triage only. It flags candidates; it does not judge them.
Known false positives are filtered so only real hits reach the auditor:
  - ถูก inside ไม่ถูก / ถูกต้อง / ถูกกว่า / ถูกลง / ถูกหวย / ถูกล็อตเตอรี่
  - ';' inside the invariant '> **Source:**' citation line (blockquotes are content)
  - '[[path\\|label]]' table links, where the backslash is vault convention
Still inspect genuine hits: a 'ถูก' that is neither adversative nor agentless
should be recast to active, and a Thai spelling that looks wrong may be a
combining-mark artifact — compare codepoints before editing.

Usage:
    python3 audit_thai_prose.py FILE [FILE ...] [--vault ROOT]

Exit codes: 0 = no hard hits, 1 = hard hits found, 2 = usage/read error.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

THAI = r"[\u0e00-\u0e7f]"

FORBIDDEN = [
    "ในยุคปัจจุบัน",
    "ในโลกปัจจุบัน",
    "เป็นที่ทราบกันดีว่า",
    "เป็นที่รู้กันว่า",
    "ปฏิเสธไม่ได้ว่า",
    "เป็นสิ่งสำคัญที่ต้องตระหนัก",
    "มีความสำคัญ",
    "ในเรื่องของ",
    "ในส่วนของ",
    "อย่างมหาศาล",
    "โดยสรุปแล้ว",
    "กล่าวโดยสรุป",
    "นั่นเอง!",
]

# ถูก followed by one of these is the ordinary word, not a passive.
THUK_NOT_PASSIVE = ("ต้อง", "กว่า", "ลง", "หวย", "สลาก", "ล็อตเตอรี่")


def strip_noise(raw: str) -> str:
    """Drop frontmatter, fenced code, inline code, and Source citation lines.

    Inline code and the Source line are use/mention exemptions. Blockquotes in
general are kept: the Thai rendering under an English quote is prose under audit.
    """
    text = re.sub(r"\A---\n.*?\n---\n", "", raw, flags=re.S)
    text = re.sub(r"```.*?```", "", text, flags=re.S)
    text = re.sub(r"`[^`\n]*`", "", text)
    text = re.sub(r"^>\s*\*?\*?Source[:*].*$", "", text, flags=re.M)
    return text


def paragraphs(text: str) -> list[str]:
    return [p for p in re.split(r"\n\s*\n", text) if p.strip()]


def real_thuk_hits(body: str) -> list[str]:
    hits = []
    for m in re.finditer("ถูก|โดน", body):
        before = body[max(0, m.start() - 3):m.start()]
        after = body[m.end():m.end() + 10]
        if before.endswith("ไม่"):
            continue
        if any(after.startswith(w) for w in THUK_NOT_PASSIVE):
            continue
        hits.append(m.group())
    return hits


def scan(path: Path, vault: Path | None) -> tuple[list[tuple[str, str]], list[tuple[str, str]]]:
    raw = path.read_text(encoding="utf-8")
    body = strip_noise(raw)
    hard: list[tuple[str, str]] = []
    warn: list[tuple[str, str]] = []

    for phrase in FORBIDDEN:
        if phrase in body:
            hard.append(("forbidden-phrase", phrase))

    for word, label in (("ทำการ", "tham-kan-padding"), ("การที่", "garn-thi-tham-hai")):
        n = body.count(word)
        if n:
            hard.append((label, f"{n}x {word}"))

    thuk = real_thuk_hits(body)
    if thuk:
        hard.append(("non-adversative-thuk?", f"{len(thuk)} hit(s) — inspect each"))

    n = body.count("ครับ") + body.count("ค่ะ")
    if n:
        hard.append(("khrap-kha-in-body", f"{n}x"))

    if "—" in body or ";" in body:
        hard.append(("em-dash-semicolon", f"— x{body.count('—')}, ; x{body.count(';')}"))

    if re.search(r"ต่างๆ", body):
        hard.append(("mai-yamok-spacing", "ต่างๆ without space"))

    n = len(re.findall(r"(?<!ไม่)มัน", body))
    if n:
        warn.append(("dummy-man?", f"{n} hit(s) — inspect each"))

    for i, para in enumerate(paragraphs(body)):
        counts = {
            "ซึ่ง": len(re.findall("ซึ่ง", para)),
            "โดย": len(re.findall("โดย", para)),
            "ดังนั้น": len(re.findall("ดังนั้น", para)),
        }
        over = {k: v for k, v in counts.items() if v > 1}
        if over:
            warn.append(("connective-budget", f"para {i + 1}: {over}"))

    periods = len(re.findall(THAI + r"\.\s", body))
    if periods:
        warn.append(("mid-paragraph-period?", f"{periods} hit(s) — inspect rhythm"))

    for target in re.findall(r"\[\[([^\]|#]+)", body):
        if vault is None:
            continue
        tgt = target.strip().rstrip("\\")  # table links escape the pipe
        candidate = vault / (tgt if tgt.endswith(".md") else tgt + ".md")
        if not candidate.exists():
            warn.append(("unresolved-wikilink", f"[[{tgt}]]"))

    return hard, warn


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description="Mechanical kode-thai pre-check for Thai prose.")
    ap.add_argument("files", nargs="+", help="Markdown files to scan")
    ap.add_argument("--vault", help="Vault root used to resolve wikilink targets")
    args = ap.parse_args(argv)

    vault = Path(args.vault).expanduser() if args.vault else None
    failed = False

    for name in args.files:
        path = Path(name)
        if not path.is_file():
            print(f"ERROR  {path}: not a file")
            return 2
        try:
            hard, warn = scan(path, vault)
        except OSError as exc:
            print(f"ERROR  {path}: {exc}")
            return 2

        print(f"\n{path}")
        for slug, detail in hard:
            print(f"  FAIL  {slug}: {detail}")
        for slug, detail in warn:
            print(f"  warn  {slug}: {detail}")
        if not hard and not warn:
            print("  clean")
        failed = failed or bool(hard)

    print("\nNote: triage only. Inspect every hit in context before editing.")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
