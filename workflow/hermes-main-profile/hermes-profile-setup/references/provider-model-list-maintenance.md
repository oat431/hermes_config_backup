# Provider Model-List Maintenance (model picker)

Use when the model picker shows a stale or wrong list for a provider — e.g. a model the user already
runs is missing from their own provider's block. **A home carries NO model list in `config.yaml`**;
the picker derives rows at read time, so the fix is per Hermes home, not a config edit.

## Where the list actually comes from

Resolution order:

1. **Live `GET <base_url>/v1/models`**, cached to `$HERMES_HOME/provider_models_cache.json` — keyed by
   *credential fingerprint*, 1h TTL, served stale up to 7d with a background revalidate.
2. **Curated static fallback** — `_PROVIDER_MODELS` in `hermes_cli/models_catalog_static.py`.
3. **models.dev metadata** — `$HERMES_HOME/models_dev_cache.json`, keyed by provider slug.

**Every home has its own cache file**: `$HERMES_HOME/provider_models_cache.json` plus
`$HERMES_HOME/profiles/<name>/provider_models_cache.json` for every profile. A fleet-wide fix
touches all of them.

## Diagnose before touching anything

Read each home's row and compare it to the curated static lists. A served list that **exactly equals**
a `_PROVIDER_MODELS` entry means the live probe failed and the fallback is being shown — that is
**not** evidence about the account's entitlement. Never conclude "the plan lacks model X" from the
picker alone.

Probe results decode as:

| Probe answer | Meaning |
|---|---|
| `401 invalid_api_key` | Wrong key tier for that endpoint — check which tier the key is provisioned for before trusting a classic-tier catalog on a token-plan account |
| `InvalidParameter: Not support` | Key **authenticated** but the endpoint exposes no listing route (common on flat-token / anthropic-format gateways). Treat the catalog as *unavailable*, not *empty* |

Provider slugs can imply a different tier than the key's. Keys provisioned on a flat/token tier
often have a dedicated provider profile whose name matches the models.dev catalog key; prefer that
slug (see Durable alternative).

## The supported write path

**Never hand-edit `provider_models_cache.json`.** The row is keyed by a credential fingerprint, so a
row written with a wrong fingerprint is invalid — the next picker open replaces it with the curated
fallback (a silent revert that looks like the fix never worked).

Use the module's own writer, which computes the fingerprint itself:

```python
from hermes_cli import models as M
M.update_provider_cache_entry("<provider-slug>", ["model-a", "model-b"])
```

Run it with the **Hermes venv interpreter**, with `$HERMES_HOME/hermes-agent` on `sys.path`.

### Per-home loop

- Set `os.environ["HERMES_HOME"]` to the target home **before** each call — the cache path and the
  fingerprint resolve it at call time, so no reimport is needed.
- **Load that home's `.env` first.** The fingerprint hashes the provider's env vars
  (`DASHSCOPE_API_KEY`, `XIAOMI_API_KEY`, …). Without them the fingerprint differs from the running
  app's and the write is dead on arrival.
- **Clear provider env keys between homes** so one home's credentials never fingerprint another
  home's row.

## Why a correct entry survives — and when it does not

The writer refuses to overwrite a **valid, non-fallback** row with a curated fallback result, so once
the row is right, a failing live probe no longer clobbers it. The row *is* invalidated whenever the
fingerprint changes — and the fingerprint includes `auth.json` / `credentials.json` **mtimes**. Any
auth write (credential-pool update, re-login, provider setup) therefore silently reverts the list.
Re-run the update after auth changes, or verify as below.

## Verify through the real read path

The picker filters at read time as well (generation-only models are dropped), so a raw JSON check can
pass while the UI still disagrees. Verify with the function the UI uses:

```python
served = M.cached_provider_model_ids("<provider-slug>", non_blocking=True)
assert "<expected-model>" in served
```

## Durable alternative

Patching `models_catalog_static.py` is a local edit **inside the app tree** — wiped by `hermes update`,
so it is a temporary edit, not a fix. If a provider slug matches a models.dev catalog key, using that
slug yields an always-current catalog with no local maintenance. Prefer that over a
fingerprint-dependent cache row whenever one exists.
