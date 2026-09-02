# Specialist-Path Soul Upgrades — Batch Worked Example (2026-08-06)

Four specialist souls upgraded/created in one session: devops, qa, product-owner, data-engineer. The pattern from `references/soul-level-upgrade.md` was applied identically to all four, confirming it is stable and reusable.

## At-a-glance comparison

| Element | DevOps | QA | Product Owner | Data Engineer (new) |
|---|---|---|---|---|
| Career path | `07_SRE_and_Platform_Engineer` (6 areas) | `10_Quality_and_Test_Engineering` (6 areas) | `14_Product_Manager` (7 areas) | `09_Data_and_ML_Engineer` (7 areas) |
| `entry_from` | Senior SWE ✓ | Senior SWE + SE ✓ | Senior SWE + TPM ✓ | Senior SWE ✓ |
| `career_family` | specialist-engineering | specialist-engineering | product-and-business | specialist-engineering |
| Foundation mapping | All 9 senior areas → ops relevance | All 9 → quality relevance | All 9 → product relevance | All 9 → data relevance |
| BOKs added | PMBOK, CyBOK | CyBOK, DMBOK | DMBOK (on top of BABOK/PMBOK) | DMBOK primary + CyBOK |
| Role Boundary section | Yes — Data/App/QA/PO splits | Yes — quality vs gate vs test | Yes — product vs project vs EM | Yes — Data vs DevOps vs FS vs QA |
| Identity change | Dev → Senior DevOps (SRE & Platform) | QA → Senior QA (Quality & Test Eng) | PO → Senior PO (Product Mgmt) | New: Data (Data & AI Engineer) |
| Principle shift | Automate → reliability-as-product | Test → risk-based quality strategy | Backlog → outcomes/discovery | New: fitness/trust/reproducibility |
| Principle count | 6 → 9 | 6 → 9 | 6 → 9 | 9 (new) |
| Soul size | 11.7 KB → 19.8 KB | 11.5 KB → 26.1 KB | 11.1 KB → 30.9 KB | 29.7 KB (new) |
| Vault refs verified | 80 ✓ | 87 ✓ | 100 ✓ | 144 ✓ |
| Smoke test | Passed ✓ | Passed ✓ | Passed ✓ | Pending (draft only) |

## Confirmed patterns

1. **Specialist path is primary, Senior SWE is foundation.** The specialist capability areas become the primary charter table with full paths. Senior SWE sits as a compact "foundation" table with one-line "why it matters for me" per area. Never duplicate the senior soul verbatim.

2. **Progression chain is explicit.** Every soul states: `Software Engineer → Senior Software Engineer → [Specialist]` with a brief note on why the senior capabilities are prerequisites.

3. **Role Boundary is essential for specialist souls.** A dedicated section preventing cross-profile confusion. Without it, specialist souls absorb responsibilities belonging to other fleet members. Example from Data Engineer:
   - "I own data architecture, pipelines, models, data quality, MLOps"
   - "DevOps owns infrastructure (k8s, VMs, networking, deployment)"
   - "Full-Stack owns application code, APIs, transactional schemas"
   - "QA owns test verification"

4. **Principle count grows from ~6 to ~9** when the senior foundation is layered in. The new principles encode ownership, framing, economics, and team multiplication — the senior behaviors that distinguish a specialist from a practitioner.

5. **BOKs expand beyond SWEBOK/SEBoK.** Each specialist path cites the BOKs its career notes reference: DMBOK for data, CyBOK for security, PMBOK for delivery/risk, BABOK for business analysis/product.

6. **Grill format is identical for upgrades and new souls.** Numbered questions with lettered options (a/b/c/d), max ~8 per round. User answers in shorthand (`1d, 2b, 3a`). Works for both:
   - **New souls:** identity, scope, output, language, destination, tone, coverage
   - **Upgrades:** scope of level-up, what to preserve, doc depth, foundation inclusion

7. **Verification is non-negotiable.** `scripts/verify_soul_refs.py` catches backtick-wrapped paths. Hand-check folder-only refs and multi-file backtick cells. The regex stops at the first `.md` in a cell, so `Deployment-Plan.md`, `Operations-Manual-Runbook.md` needs manual confirmation.

8. **Product/business paths need special framing.** Product Manager is `career_family: product-and-business`, `level: manager` — NOT `senior-specialist`. The upgrade elevates from backlog ownership to outcome ownership (discovery, strategy, analytics, roadmapping, technical partnership). It explicitly does NOT become a project manager or engineering manager soul. See `references/product-business-soul-upgrade.md`.

## Sync flow (identical for all four)

1. Draft to `soul-collection/<DOMAIN>/<position>-soul.md` only.
2. Run `verify_soul_refs.py` + targeted template existence checks.
3. Present to user: what changed table, review points.
4. User confirms.
5. Backup old soul → copy collection → profile → `md5sum` both (byte-identical) → smoke test:
   ```bash
   hermes -p <profile> chat -q "Answer in one sentence: What is your name, your role, and what is your number one core principle?"
   ```
6. For NEW profiles only: also update `profile-registry.md` + main soul routing table. For upgrades: registry/routing unchanged (domain/triggers don't change, only depth).

## Template verification approach

Before writing the soul, verify the template folders that will be referenced:

```bash
# Check folder existence + list contents
for d in 13_Testing_and_Verification 18_Quality_Assurance 15_Data_Management 14_Security; do
  echo "=== $d ==="
  ls "F:/obsidian_note/swe-knowledge/document-template/$d"
done

# Check BOK chapter existence
ls "F:/obsidian_note/swe-knowledge/body-of-knowledge/DMBOK"
ls "F:/obsidian_note/swe-knowledge/body-of-knowledge/CyBOK"
```

After writing, run the verifier:
```bash
python "C:/Users/Admin/AppData/Local/hermes/skills/hermes-profile-setup/scripts/verify_soul_refs.py" \
  "F:/obsidian_note/oralita_md/soul-collection/AI-SDLC"
```

Then spot-check templates that are unique to the specialist role (not covered by the verifier's regex):
```bash
python -c "
from pathlib import Path
checks = [
    r'F:/obsidian_note/swe-knowledge/document-template/15_Data_Management/ETL-ELT-Specification.md',
    r'F:/obsidian_note/swe-knowledge/document-template/15_Data_Management/API-Data-Contract.md',
    # ... etc
]
missing = [x for x in checks if not Path(x).exists()]
print('checked', len(checks))
print('missing', missing)
raise SystemExit(bool(missing))
"
```
