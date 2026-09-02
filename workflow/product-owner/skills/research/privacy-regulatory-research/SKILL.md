---
name: privacy-regulatory-research
description: "Use for privacy research. Build sourced checklists."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [privacy, regulatory, legal-research, data-protection, product, compliance]
    related_skills: []
---

# Privacy and Regulatory Research for Product Decisions

## Overview

Use this class-level skill when a product, feature, integration, or hosted service raises privacy or data-protection questions. The deliverable is decision-ready product guidance grounded in current primary sources: a cautious bottom line, a processing map, purpose-by-purpose legal-basis analysis, and an implementation checklist. Do not present the result as definitive legal advice.

Research must distinguish what the law says from what the product should do conservatively. Public, pseudonymous, normalized, hashed, or user-supplied identifiers may remain personal data when they can be linked to a person or combined with other records.

For a Thai PDPA public-identifier/scoreboard pattern, load the source-specific knowledge bank at `references/thai-pdpa-youtube-scoreboard.md`; for an owner-facing MUST DO/MUST NOT DO handoff and cross-document release-gate pattern, also load `references/thai-pdpa-owner-readiness.md`. Treat both files' links and section notes as starting points and re-check current regulator pages before relying on them.

## When to Use

- A user asks whether names, handles, IDs, aliases, donations, scores, or logs are personal data.
- A product publicly displays an identifier, ranking, profile, contribution, or behavior-derived score.
- Data is imported from a platform, payment/donation service, API, chatbot, or other third party.
- A developer, agency, cloud host, or SaaS provider stores or processes data for an owner.
- The user needs lawful-basis, consent, privacy-notice, rights, deletion, retention, breach, transfer, or controller/processor guidance.

Do not use this as a substitute for jurisdiction-specific counsel on high-risk processing, sensitive data, children, regulated sectors, employment, health, finance, or disputed legal interpretation. Escalate those issues explicitly instead of hiding uncertainty.

## Research Workflow

### 1. Define the processing before researching the law

Write a compact fact pattern:

- jurisdiction(s), location of controller/processor, and location of data subjects;
- product purpose and whether the feature is optional or necessary;
- each data source and whether it is collected directly or from another source;
- each data field, including derived scores, normalized values, IDs, logs, and backups;
- every operation: collect, observe, match, infer, store, use, disclose, publish, export, and delete;
- audiences/recipients, subprocessors, hosting regions, and public visibility;
- expected scale, monitoring frequency, minors, and sensitive-data risk.

Do not jump from “the user entered a command” to “consent exists.” A command can be an input mechanism, but consent still needs a clear purpose, timing, voluntariness, and evidence.

### 2. Use a primary-source hierarchy

Search in this order:

1. statute, regulation, official gazette, and regulator guidance;
2. official regulator translations, FAQs, templates, and enforcement/consultation pages;
3. reputable secondary commentary for orientation and issue spotting;
4. vendor/platform privacy notices for factual data-flow details, never as the legal basis for the customer’s separate processing.

For every material conclusion, record the exact section/clause, official URL, document title, and whether the translation is unofficial. Where a translated text says that the local-language gazette controls, say so. If an official page or vendor policy cannot be retrieved, do not fill the gap with assumptions; report the limitation and use the statute or another primary source.

### 3. Classify identifiers conservatively

Ask whether the field relates to a natural person and enables direct or indirect identification in context. Analyze combinations, not isolated strings:

- public display names, handles, aliases, and usernames can identify an account or person;
- a stable provider ID is usually an identifier even if never displayed;
- normalization, tokenization, hashing, or pseudonymization usually reduces exposure but does not itself anonymize data;
- donation, purchase, participation, ranking, location, and behavioral data become personal when linked to an identifier;
- a brand or organization name may not relate to a natural person, but chat authors, operators, and linked accounts can still be in scope;
- inferential or derived data deserves the same analysis as source data;
- classify possible sensitive-data leakage separately, especially where messages or transactions reveal health, religion, politics, sexuality, criminal history, or similar traits.

### 4. Separate the purpose-by-purpose legal-basis analysis

Create a table with: purpose, fields, operation, legal basis candidate, necessity, balancing/consent evidence, recipients, retention, and risk.

Do not use one vague basis for the entire system. At minimum separate:

- account/member registration;
- internal scoring or service delivery;
- third-party matching or reconciliation;
- public display or search indexing;
- abuse prevention and security logs;
- billing, tax, or legal records;
- analytics or product improvement.

For consent, verify: prior or contemporaneous timing; specific purpose; plain, accessible, distinguishable presentation; affirmative and freely given choice; no unrelated service bundling; recorded notice/version/time; and withdrawal that is as easy as giving consent. Public visibility should normally have its own opt-in when it is optional.

For legitimate interests, document the three-part assessment: legitimate purpose, necessity, and balancing against the person’s rights/expectations. Public availability of a handle is evidence for expectations, not a blanket permission to republish or link it. A technical exact-match rule is not a legal basis.

### 5. Treat public display and matching as high-attention operations

A public leaderboard, profile, alert, or ranking is a disclosure/publication, not merely internal storage. State exactly what the audience sees and what it can infer. A score may reveal donations, spending, loyalty, or behavior even when the amount is hidden.

Prefer, in order:

1. a member-chosen public alias;
2. an explicit public-visibility choice with private mode available;
3. the minimum public fields, such as alias/handle plus a coarse score or tier;
4. no raw donor name, message, payment identifier, or internal ID in the public response.

Use a private stable provider ID for matching where possible. Treat exact string matching as a heuristic: names can collide, a donor can enter another person’s handle, and handles can change. Provide a correction/manual-review path and avoid awarding or publishing an ambiguous match.

### 6. Build the notice and rights path into the product

A useful notice should identify the controller and contact channel; purposes and bases; data categories; sources; whether fields are optional; recipients; hosting/transfer locations; retention; and the available access, correction, objection, restriction, withdrawal, and erasure paths.

If data comes from another source, check the jurisdiction’s special notice deadline and any first-contact/first-disclosure rule. Do not assume the upstream platform’s notice covers a downstream owner’s new matching or publication purpose.

Provide a low-friction privacy control: hide/remove command or form, account-based authentication, correction/false-match appeal, and a channel-independent contact route. Define what happens to the public projection, caches, exports, logs, and backups. Explain lawful exceptions without making removal unnecessarily difficult.

### 7. Assign controller/processor roles from facts

The party deciding why and how processing occurs is generally the Controller. A developer/host is a Processor only when operating on the controller’s instructions and not reusing the data for its own purposes. If the developer decides purposes, combines data across customers, profiles users, or independently determines material means, analyze separate or joint-controller status.

For a processor arrangement, require a written data-processing agreement covering: instructions and permitted purposes; fields; confidentiality; least privilege; security; subprocessors; hosting/transfer locations; rights assistance; breach escalation; audit/cooperation; retention; backup deletion; return/destruction; and no independent reuse. Contract wording cannot override the actual relationship.

### 8. Specify retention and security instead of saying “keep only as long as necessary”

Set a field-level schedule for raw events, names, IDs, member records, public projections, consent evidence, support tickets, logs, exports, and backups. Explain the period in the notice and trigger deletion when the purpose ends, consent is withdrawn without another basis, the data is stale, or a request succeeds. A small-business or record-keeping exemption is not a general exemption from privacy duties.

Use risk-appropriate organizational, technical, and physical measures: role-based access, least privilege, authentication, encryption in transit and at rest, secret management, no sensitive data in logs, audit trails, isolated public/read-only projections, backup expiry, access review, and incident playbooks. Include the controller’s breach deadline and the processor’s faster internal escalation target.

### 9. Produce a cautious, usable deliverable

Lead with three to five outcome bullets. Then provide:

1. a data-classification table;
2. a purpose/legal-basis table with uncertainty labels;
3. a product/privacy checklist grouped by priority;
4. controller/processor and vendor-contract actions;
5. retention/security/breach actions;
6. official source links with section numbers;
7. a short “not legal advice / local-language text controls” caveat;
8. research limitations, including inaccessible or unverified vendor pages.

Use “likely,” “conservative approach,” “depends on facts,” and “confirm with local counsel” where appropriate. Do not claim a vendor’s terms, a current law, or an API behavior without a source.

## Common Pitfalls

1. **“It is public, so it is not Personal Data.”** Public visibility does not eliminate identifiability or the need for a lawful basis for a new disclosure.
2. **“Normalization/hash = anonymization.”** If the system can link the value back to a member, it remains personal or pseudonymous data.
3. **“The registration command is consent.”** It is not enough unless the specific processing, optionality, timing, and withdrawal path are clear.
4. **Bundling public display with service access.** Keep optional publication separate so consent is freely given.
5. **Relying on the upstream platform’s notice.** The owner needs a downstream notice for its own matching, scoring, and publication.
6. **Assuming exact matching proves identity.** Handle/name collisions, impersonation, stale names, and false attribution require validation and correction.
7. **Calling the developer a processor by contract alone.** Actual purposes and independent reuse determine roles.
8. **Treating a small-enterprise exemption as a full exemption.** Check its exact scope and continue to implement notice, security, rights, and deletion.
9. **No fixed retention schedule.** “Until no longer needed” is not an operational deletion control; set triggers and periods by field.
10. **Ignoring secondary disclosure.** Public scores, rankings, and tiers can reveal sensitive behavior even when raw amounts or names are hidden.
11. **Relying on an unofficial translation without warning.** Cite the official page, identify the translation status, and state that the local-language source controls.

## Verification Checklist

- [ ] Jurisdictions, roles, subjects, sources, fields, operations, recipients, and hosting regions are documented.
- [ ] Public, normalized, pseudonymous, and derived identifiers were analyzed for indirect identification.
- [ ] Each distinct purpose has a candidate legal basis and a necessity/risk explanation.
- [ ] Public display is separately opted in where optional, or a legitimate-interest assessment is documented.
- [ ] Third-party-source notice timing and upstream/downstream responsibility are addressed.
- [ ] Notice includes purposes, fields, sources, recipients, retention, contacts, rights, and consequences of non-provision.
- [ ] Hide, withdraw, correct, access, and erasure workflows are usable and authenticated without demanding unnecessary real-world identity.
- [ ] Raw donor names/messages/payment details are minimized and have a deletion trigger.
- [ ] Public projections, caches, exports, logs, and backups are included in deletion design.
- [ ] Controller–processor agreement covers instructions, security, subprocessors, transfers, rights, breach, retention, and no reuse.
- [ ] Security controls and breach escalation are proportionate and testable.
- [ ] Official sources, exact sections, retrieval date, translation caveats, and unresolved issues are listed.
- [ ] The final response says “not legal advice” and does not overstate an unsettled interpretation.
