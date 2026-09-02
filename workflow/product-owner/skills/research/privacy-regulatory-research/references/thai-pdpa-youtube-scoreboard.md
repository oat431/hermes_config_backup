# Thai PDPA: small public YouTube viewer scoreboard

Session-specific knowledge bank. Re-check the linked regulator pages and the Thai text before using this for a new matter. The English PDFs are unofficial translations; the Thai Government Gazette text controls.

## Core statutory hooks

- **Sections 5–6, Personal Data Protection Act B.E. 2562 (2019):** the Act covers a controller/processor in Thailand regardless of where processing occurs, and can cover an overseas provider offering services to or monitoring people in Thailand. Personal Data is information relating to a natural person that enables direct or indirect identification. Controller/Processor roles depend on decision-making versus acting on instructions.
- **Sections 19–22:** consent is generally required unless another statutory basis applies; consent must be prior/contemporaneous, specific, informed, distinguishable, plain-language, freely given, and easy to withdraw. Use data for the notified purpose and only to the necessary extent.
- **Section 23:** pre-collection notice should cover purposes, whether provision is required, data categories, retention, recipients, controller/DPO contacts, and data-subject rights.
- **Section 24:** non-consent bases include contract, legal obligation, public interest, and legitimate interests not overridden by the data subject’s fundamental rights. Consent is not automatically required for every activity, but public display should conservatively be treated as a separate optional purpose.
- **Section 25:** collection from another source generally triggers notice without delay and no later than 30 days, or at first communication/before first disclosure where applicable; consent or a Section 24/26 exception must be assessed. An upstream platform’s notice does not automatically cover the downstream channel owner’s matching/publication purpose.
- **Section 27:** use/disclosure needs consent or an applicable Section 24/26 basis. Publishing a handle and score is a disclosure, not merely internal storage.
- **Sections 30–36:** access/copy (generally within 30 days), portability in limited cases, objection, erasure/anonymization, restriction, and accuracy/correction rights.
- **Section 33:** erasure may apply when data is no longer necessary, consent is withdrawn without another legal basis, a valid objection succeeds, or processing was unlawful. Exceptions exist. If data was made public, the controller has additional duties concerning the public disclosure and other controllers.
- **Section 37:** appropriate security, controls against unauthorized use/disclosure, a deletion/destruction system, and breach notification without delay and where feasible within 72 hours unless unlikely to risk rights/freedoms; high-risk breaches also require notice to data subjects.
- **Sections 39–41:** controller records, processor records/duties, written processor agreement, and DPO triggers. Small-enterprise record exemptions are narrow and do not remove general PDPA duties.

## Product conclusions for the scoreboard

1. A YouTube display name or unique handle is likely Personal Data when linked to a chat author/account. Public visibility is not a blanket PDPA exemption.
2. Normalizing a handle (strip `@`, trim, case-fold) does not anonymize it. A hash/token also remains linked/pseudonymous data if the system can reverse or match it.
3. An EasyDonate donor name is likely Personal Data when it is a real name or recognizable alias. Matching it to a registered handle creates a stronger identity link. A donation amount, event, or score is Personal Data when associated with that link.
4. Exact string equality is not proof of identity: donor aliases can collide, be mistyped, impersonate another person, or become stale. Use the registered YouTube/channel ID privately where possible, handle ambiguity manually, and provide correction.
5. Recommended basis for public handle + score: separate, explicit opt-in consent with private registration/scoring available. Consent text should say what is displayed, where, why, that it is optional, and how to withdraw/remove.
6. Internal scoring/matching may potentially use a separate consent, contract, or documented legitimate-interest basis depending on facts. A technical matching rule is not itself a lawful basis.
7. Do not publicly display the original EasyDonate donor name, raw donor message, payment identifiers, or exact donation amount unless separately justified. Points can still reveal donation/participation behavior.
8. Keep the subscriber-observation table separate from members; do not award points or publish from it. Prefer short-lived observations or aggregate counts.
9. Delete unmatched donor names after a defined short reconciliation window. Retain only the minimum internal event/points record after matching. Define periods for members, public projections, consent evidence, logs, exports, and backups; no single universal PDPA period applies here.
10. Build hide/withdraw/remove/correct/access routes, and propagate removal to public projections, caches, logs, exports, and backups. The PDPC’s 2024 erasure notification describes a 90-day maximum where a valid request is not subject to an exception; operational removal should be much faster.

## Controller/processor model

- The channel owner normally determines the purposes of registration, scoring, matching, and public display and is therefore likely the Controller.
- A developer/host is likely a Processor only if it acts on the owner’s instructions and does not reuse data for its own purposes. If it chooses purposes, combines data across channels, profiles users, or independently reuses data, assess separate/joint controller status.
- The Section 40 agreement should cover instructions, fields, no independent reuse, access/security, subprocessors/cloud regions, rights assistance, breach escalation, retention/backup deletion, return/destruction, and transfer rules. The developer should notify the owner immediately of incidents; do not wait for the owner’s 72-hour deadline.
- If hosting is outside Thailand, assess Section 28 international-transfer requirements. Consider Section 5 territorial scope for both Thai and overseas providers.

## Official sources

- PDPC English Act page: https://www.pdpc.or.th/en/23134/
- Official PDPC English Act PDF: https://www.pdpc.or.th/wp-content/uploads/2023/12/2_Personal-Data-Protection-Act-2019.pdf
- MDES government Act page/PDF: https://mdes.go.th/law/detail/3577-Personal-Data-Protection-Act-B-E--2562--2019-
- PDPC consent guidance (Thai): https://www.pdpc.or.th/14/
- PDPC English subordinate-legislation index: https://www.pdpc.or.th/en/notifications-of-the-personal-data-protection-committee/
- Security Measures (PDPC page): https://www.pdpc.or.th/en/22758/
- Security PDF: https://www.pdpc.or.th/wp-content/uploads/2022/06/4.-Security-Measures-of-Data-Controllers.pdf
- Breach notification criteria (PDPC page): https://www.pdpc.or.th/en/22783/
- Breach PDF: https://www.pdpc.or.th/wp-content/uploads/2022/12/9.-Criteria-and-Procedures-for-Notifying-Personal-Data-Breach.pdf
- Small-enterprise record exemption: https://www.pdpc.or.th/en/22752/
- Processor processing records: https://www.pdpc.or.th/en/22763/
- Erasure/destruction/de-identification (2024): https://www.pdpc.or.th/en/22864/
- PDPC privacy notice page: https://www.pdpc.or.th/privacy/
- PDPC consultation: https://consult.pdpc.or.th/
- EasyDonate privacy policy to review for vendor data flows: https://easydonate.app/privacy-policy

## Research limitation from the source session

EasyDonate’s privacy page was Cloudflare-protected in the research environment. The product conclusions above rely on Thai PDPA definitions and official PDPC sources, not on unverified claims about EasyDonate’s current terms or API behavior.
