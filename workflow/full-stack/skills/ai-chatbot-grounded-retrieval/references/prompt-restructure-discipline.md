# Prompt Restructure Discipline

Validated during the ITOPPLUS take-home (2026-08-30): re-skinning a Thai admin prompt into an agent-soul layout — **every rule word identical** — still changed model behavior on the hardest scenario. Structure alone is a behavior lever.

## The safe procedure

1. **Backup** the current prompt file outside the project (one `cp` — no git needed).
2. **Copy constraint rules verbatim.** Never paraphrase guardrails while restructuring; wording drift = behavior drift. Only scaffolding (headers, section labels) may be new. If the target language and scaffold language differ (Thai rules + English headers), that's fine — keep the rule text itself untouched.
3. **Verify integrity programmatically before testing behavior**: every non-empty line of the ORIGINAL prompt must appear verbatim in the new file, except an explicitly listed set of intentional replacements. Three-line Python check against the backup — do not trust eyeballs on Thai text.
4. **Re-run the E2E scenario suite** — not just unit tests. Unit tests check context assembly; the model's *use* of the prompt is only observable live. Run flaky-prone scenarios 2–3×.
5. **Diff behavior, not just pass/fail**: a scenario can still "pass" while answering worse (e.g. a bare clarifying question instead of facts+question).

## The over-conservatism fix (nudge pattern)

Soul/boundary framing can make a model *more* guarded: on ambiguous references ("the red one from earlier") it asked "which one do you mean?" while sitting on the facts. Fix without weakening any guardrail — add one closing instruction:

> ถ้าลูกค้าอ้างถึงสินค้าก่อนหน้าแบบกำกวม (เช่น "ตัวสีแดงเมื่อกี้") ให้แสดงราคาและสต็อกของสินค้าที่ตรงกันทุกตัว พร้อมถามว่าหมายถึงตัวไหน — อย่าถามกลับโดยไม่ให้ข้อมูล

*("If the customer references a product ambiguously, show price+stock for every matching product AND ask which one — never ask back without giving data.")*

Result: facts + clarifying question, strictly better than the original. Generalizes: when a restructure makes the model ask instead of show, add "show what you know, then ask" — never remove the boundary.

## What NOT to import from agent-persona templates

Soul/persona templates built for agentic runtimes carry routing tables, tool inventories, memory protocols, self-update clauses. A stateless single-shot chatbot has none of that machinery — importing it is cargo-cult. Import only: Identity block → numbered hard rules → data section → closing instruction.