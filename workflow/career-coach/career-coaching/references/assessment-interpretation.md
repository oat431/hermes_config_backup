# Assessment Interpretation Protocol

How to intake, interpret, and file personality/values test results for coaching. Standing rules live in SKILL.md ("Personality & Values Assessment Coaching"); this file is the depth.

## Intake

1. Read the user's raw-results note first. openpsychometrics IPIP-BFFM exports embed the score graphic as a remote URL `BIG5-graphic.php?EXT=&EST=&AGR=&CSN=&IIM=` — **the query params ARE the raw scores**, in order: Extraversion, Emotional Stability, Agreeableness, Conscientiousness, Intellect/Openness. Parse the params; do not eyeball the bars.
2. Percentiles exist only inside the graphic: `vision_analyze` the image URL and transcribe the factor / label / raw / percentile table exactly.
3. Record instrument + item count — short (50-item) vs long form sets the noise band below.

## Confidence caveats (state in every interpretation)

- 50-item short form ⇒ ~±10 percentile noise per trait; treat only far-out scores (≈ ≥90 or ≤10) as real signal.
- Percentile base = self-selected online test-takers, not the user's national working population.
- Single sitting, single mood; schedule the next data point (~6 months, or after a major load/life change) instead of over-analyzing one sitting.
- Self-report: it measures the self described that day, not a fixed trait.

## Interpretation order

1. Profile shape first (flat + one spike vs broad spread) — that is the headline.
2. Per trait: score → behavioral cross-check from the master profile → label **corroborated / under-captured / contradicted**.
3. Under-capture pattern: pragmatic, artifact-first users score low on imagination/aesthetic items despite high intellectual curiosity — trust the behavior, name the scale artifact explicitly.
4. Any trait ≥70 or ≤30 percentile gets a shadow + countermeasure row in the analysis and in the tracker.

## Career-mapping rules

- High stability + high conscientiousness + mid agreeableness ⇒ senior IC track (SE → Staff, SRE/Platform, Architect); route to EM/PM only with social-energy evidence, not extrapolation.
- Mid openness entering a fast-moving field (AI/ML roles): coach a visible vetting ritual (timeboxed experiment → evidence → adopt, stated out loud) so pragmatism does not read as resistance on a new team.
- Mid agreeableness + high stability ⇒ build two direct-disagreement stories for the conflict dimension; stability is a negotiation asset (hold anchors calmly, use silence).

## Vault output layout

`interview-preparation/personality_test/`
- `draft/` — user's raw export, untouched
- `summary/00-Index.md` — index, standing rules (mirror-not-map, evidence outranks scores), assessments-taken table
- `summary/01-<Test>-Results.md` — scores table, honest per-trait read, behavioral cross-checks, caveats
- `summary/02-Career-Implications.md` — path fit, interview coaching rules, trait-shadow watch-outs table, role-window specifics

Action items flow from `02` into the career improvement tracker via wikilinks — never duplicated as free text.

## Recommendation queue

1. IPIP-BFFM (openpsychometrics.org/tests/IPIP-BFFM/) — first assessment.
2. Moral Foundations (moralfoundations.org/questionnaires/) — values follow-up; if the official site serves unscored items, score them from the user's raw answers yourself.
3. Any other instrument (facet-level Big Five, compass variants): verify the host live first. University-hosted mirrors and old mirror paths go dark without notice — when no live host exists, say skip; never send the user to a dead link.
