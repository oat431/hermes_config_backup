# Thai PDPA owner-readiness pattern for public identifiers and scores

Use this reference when a small creator/community product collects platform handles or donor names, links them to scores, and publishes a public leaderboard.

## Product framing

Treat the following as potentially personal data when they identify or can be linked to a natural person:

- platform user IDs and handles;
- donor names and payment/donation events;
- contribution points, ranks, tiers, or inferred participation;
- logs, exports, caches, and backups containing those fields.

A public handle is not automatically outside PDPA. Normalization, lowercasing, removing `@`, hashing, or tokenization does not automatically anonymize a value if the system can link it back to a person.

## Owner handoff: MUST DO

1. Identify the likely controller and developer/host processor roles from actual decision-making, not labels alone.
2. Document separate purposes: registration, internal matching/scoring, public display, security logs, legal/record-keeping, and backups.
3. Decide and record a lawful-basis analysis for each purpose. Treat optional public display as a separate disclosure purpose; prefer a clear opt-in or document a defensible legitimate-interest assessment.
4. Publish a plain-language privacy notice covering controller contact, fields, sources, purposes, recipients, hosting/transfer locations, retention, rights, and consequences of not providing optional data.
5. Provide usable hide/withdraw/correct/access/erase/removal paths, including a contact channel outside the live chat.
6. Set field-level retention and deletion triggers for raw donor names/messages, member records, inactive records, logs, projections/caches, exports, and backups.
7. Record written processor instructions covering no independent reuse, least privilege, security, subprocessors, incident escalation, rights assistance, retention, backup deletion, return/destruction, and locations.
8. Prepare a breach escalation playbook; the processor/developer should notify the owner immediately, and the owner/counsel assess regulator and data-subject notification duties.
9. Gate public release on owner sign-off and, where legal certainty is needed, Thai privacy-counsel review.

## Owner handoff: MUST NOT DO

- Do not publish raw donor names, messages, payment identifiers, or exact donation records by default.
- Do not expose stable internal/provider IDs publicly.
- Do not collect display names the product does not need.
- Do not treat the user's registration command as blanket consent to every later purpose.
- Do not infer identity from fuzzy name similarity; exact equality is still only a heuristic and collisions/impersonation are possible.
- Do not retain raw donor data indefinitely without a documented need.
- Do not edit scores without backup, transaction, reason, operator, and before/after evidence.
- Do not place personal data or secrets in source control, issues, logs, screenshots, or fixtures.
- Do not claim "PDPA compliant" from a feature checklist alone.

## Thai PDPA section map for counsel discussion

Use as a signpost, not a legal conclusion; re-check the Thai-language Act/Gazette and current PDPC material:

| Topic | Commonly relevant sections | Product question |
|---|---|---|
| Scope, personal data, controller/processor | 5–6 | Who decides why/how the data is processed? |
| Consent and other lawful bases | 19–24 | Which purpose is necessary, optional, consent-based, or legitimate-interest based? |
| Notice and indirect collection | 23, 25 | How are data received from platforms/providers explained and when? |
| Use/disclosure | 27 | Is the public scoreboard a new disclosure purpose? |
| Rights | 30–36 | Can a viewer access, correct, hide, withdraw, restrict, or erase data? |
| Security and breach | 37 | Are safeguards, deletion controls, and escalation testable? |
| Records, processors, DPO-related questions | 39–41 | Are records, processor instructions, and obligations documented? |

## Cross-document propagation checklist

When adding this gate to a project:

- overview: add a short owner MUST/MUST NOT summary and source links;
- security: add a PDPA owner-readiness release gate;
- risk register: expand privacy risk mitigation beyond `private` visibility;
- plan: add a blocking owner-readiness action before public release;
- handoff minutes: identify owner decisions and legal-review boundary;
- data model/API: keep public projection allowlisted and raw donor fields private;
- tests: inspect public responses, removal behavior, redaction, and retention controls.

Always say this is product guidance, not legal advice or a compliance certification.
