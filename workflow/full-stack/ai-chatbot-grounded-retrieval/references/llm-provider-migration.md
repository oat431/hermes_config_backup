# LLM Provider / Model Migration Checklist

Validated during the ITOPPLUS take-home OpenAI → DeepSeek migration (2026-08-30). Zero code changes were needed thanks to provider-neutral `LLM_*` env config — but zero code change ≠ zero validation.

## The rule

**Connectivity is not compatibility.** A successful auth + simple completion proves almost nothing. Generation params, token budgets, and reply behavior must be re-validated against the new model family.

## The reasoning-model max_tokens trap (the one that bites)

Reasoning models spend invisible reasoning tokens from the **same** `max_tokens` budget as the visible reply.

- Symptom: some prompts return `content == ""`, others answer fine — *intermittent by prompt complexity*. Simple prompts (short reasoning) fit in the budget; complex grounded prompts (long reasoning) exhaust it.
- Diagnosis probe: call the API directly and inspect
  - `choices[0].finish_reason == "length"`
  - `usage.completion_tokens` large, `choices[0].message.content` empty
  - `choices[0].message.reasoning_content` (the hidden tokens) — large
- Fix: raise `max_tokens` (500 → 4000 fixed it). Rule of thumb for reasoning models: budget ≥ ~10× the longest expected reply.
- Probe pattern (stdlib + openai SDK): small script that calls `chat.completions.create` at increasing `max_tokens` (500 / 2000 / 4000) on the **real production prompt**, printing `finish_reason`, `content_len`, `reasoning_len`, `completion_tokens` — plus `client.models.list()` to confirm available model IDs.

## Migration checklist

1. Env: base URL + model ID + key (`https://api.deepseek.com`, model names are family-specific — list them via `client.models.list()`, don't guess).
2. Probe small + complex prompts at the current `max_tokens`; check `finish_reason`.
3. Re-run the **full integration test suite** against the new provider (grounded bots: price accuracy, handoff, deflection tests all re-validated live).
4. Re-run the E2E scenario suite at least twice per scenario — new model families shift tone and conservatism; look for *behavior* regressions (e.g. asking instead of answering), not just test failures.
5. Update README/env-example docs with provider-specific warnings (e.g. "set 4000+ for reasoning models").
6. Log the finding in the project's decision log — provider-swap lessons are walkthrough gold.