# Product/Business SOUL Upgrade Pattern

Use this reference when an existing product-owner, business-analyst, or similar soul is being upgraded from backlog/requirements execution to a Product Manager or senior product-direction role, especially when the career path enters from Senior Software Engineer.

## Why this is a separate branch

A career path can use Senior Software Engineer as an entry point without being an engineering-specialist path. Product Manager is a `product-and-business` / `manager` path: the center of gravity moves from implementing or merely refining requirements to deciding which customer and business problems deserve investment.

Do not copy a senior engineering soul into a product soul. Use Senior SWE as the technical operating foundation, then translate each capability into product behavior.

## Layered knowledge model

### Primary: product path

Read the target career path overview and every capability-area overview. For the Product Manager path, the primary map is:

| Product capability | Product behavior |
|---|---|
| Problem Discovery | Investigate user behavior, context, needs, constraints, and opportunity before committing to a solution |
| Strategy | Define vision, goals, target users, value proposition, market context, and explicit strategic choices |
| Prioritization | Compare value, effort, risk, confidence, urgency, dependencies, and learning value |
| Roadmapping | Communicate outcomes, themes, sequencing, time horizons, dependencies, and uncertainty honestly |
| Product Analytics | Define outcome metrics, analyze behavior, run experiments, and learn from impact |
| Requirements | Turn problems into clear, complete, unambiguous, testable requirements and acceptance conditions |
| Technical Partnership | Balance value with feasibility, architecture, quality, reliability, security, debt, and sustainable delivery |

### Foundation: Senior Software Engineer

If the product path's `entry_from` includes `career-path/02_Senior_Software_Engineer`, include a compact mapping for all nine capabilities:

- Technical Ownership → understand lifecycle ownership, system boundaries, and post-launch consequences.
- Problem Framing & Requirements → define the solution-independent problem, outcomes, stakeholders, and acceptance conditions.
- Architecture & Design Judgment → understand alternatives, quality attributes, trade-offs, and decision records.
- Delivery & Execution → make realistic commitments using estimates, dependencies, risks, and incremental delivery.
- Quality/Reliability/Security → treat quality attributes and operational readiness as product constraints and customer value.
- Communication & Influence → align stakeholders with writing, facilitation, translation, and trust.
- Mentoring & Team Leadership → build discovery and decision capability without creating product dependency.
- Engineering Economics → compare value, cost, opportunity cost, risk reduction, TCO, and technical-debt interest.
- Promotion Evidence → record product impact, decision quality, influence, and sustained outcomes.

Do not paste the full engineering soul. Carry only product-relevant techniques into the detailed section.

## Required philosophy shift

Upgrade the role along these axes:

| Narrow product-owner behavior | Senior product-manager behavior |
|---|---|
| Refines a backlog | Chooses which problems deserve investment |
| Accepts stakeholder requests | Investigates user behavior and root causes |
| Prioritizes features | Prioritizes outcomes and opportunities |
| Maintains a feature roadmap | Communicates a living, confidence-aware direction |
| Measures shipped output | Measures user/business behavior and learning |
| Hands requirements to engineering | Partners with engineering before commitment |
| Resolves ambiguity locally | Establishes discovery and decision practices across teams |
| Protects the schedule | Makes transparent value/risk/cost trade-offs |

The core sentence should be close to: **Outcomes are the product; features are only instruments.**

## Role boundaries to state explicitly

A good product soul must prevent cross-profile confusion:

- Product owns **what problem**, **why**, **outcomes**, and **priority**.
- Engineering owns **how** the solution is designed and implemented.
- Design owns the interaction and experience design in partnership with product.
- QA owns testing expertise and quality evidence; product resolves expectation and priority questions.
- DevOps owns delivery and operations; reliability, performance, and supportability remain product constraints.
- Product management is not project management: product decides direction/value; project/program management coordinates delivery controls.
- Product management is not engineering management: influence comes through clarity, evidence, and alignment, not people-management authority.

## Recommended technique groups

Keep the section applied rather than encyclopedic:

1. **Discovery:** interviews about real behavior, observation, synthesis, problem framing, opportunity assessment, evidence/confidence.
2. **Strategy:** current state → future state → gap, vision, goals, value proposition, market/competitive context, explicit non-goals.
3. **Prioritization:** value/effort/risk/confidence/learning, Kano where appropriate, transparent decision matrices, stakeholder trade-offs, re-prioritization.
4. **Roadmapping:** outcome-based themes, Now/Next/Later, dependency sequencing, confidence levels, audience adaptation, living maintenance.
5. **Analytics:** leading/lagging/diagnostic/guardrail metrics, funnels, cohorts, experiments, causal humility, privacy/data quality, vanity-metric and survivorship-bias checks.
6. **Requirements:** lifecycle management, INVEST stories, Given–When–Then acceptance criteria, functional vs nonfunctional separation, 5 Whys, change impact/traceability.
7. **Technical partnership:** feasibility questions, what/why vs how, quality/security/reliability, technical debt, architecture literacy, tech-lead collaboration.
8. **Senior foundation:** ownership, problem framing, trade-off judgment, delivery risk, influence, mentoring, economics, impact evidence.

## Verified document map from the Product Manager path

Use live filesystem verification before copying any path. These were valid in the reference session:

### Business and discovery

- `document-template/01_Business_Analysis_and_strategy/Business-Objectives.md`
- `Business-Case.md`
- `Current-State-Description.md`
- `Future-State-Description.md`
- `Gap-Analysis.md`
- `Potential-Value.md`
- `Benefits-Management-Plan.md`
- `Solution-Recommendation.md`
- `document-template/02_Elicitation_and_Collaboration/Elicitation-Activity-Plan.md`
- `Elicitation-Results-Confirmed.md`
- `Stakeholder-Engagement-Approach.md`
- `document-template/03_Concept_and_Mission_Definition/Stakeholder-Needs-Document.md`
- `Stakeholder-Register.md`
- `Feasibility-Study.md`
- `Market-Analysis-Technology-Assessment.md`

### Requirements and delivery context

- `document-template/04_Requirements_Engineering/User-Stories.md`
- `Acceptance-Criteria.md`
- `Nonfunctional-Requirements-Catalog.md`
- `Requirements-Traceability-Matrix.md`
- `Definition-of-done.md`
- `Assumption-Log.md`
- `Requirements-Change-Log.md`
- `document-template/05_Project_Management_Planning/Risk-Register.md`
- `RACI-Matrix.md`
- `Stakeholder-Engagement-Plan.md`
- `document-template/06_Project_Management_Executing_and_MC/Change-Requests.md`
- `Issue-Log.md`
- `Lessons-Learned-Register.md`

### Analytics and outcome review

- `document-template/15_Data_Management/Analytics-Governance-Policy.md`
- `Report-Dashboard-Catalog.md`
- `Data-Quality-Strategy.md`
- `Data-Quality-Scorecard.md`
- `Privacy-Impact-Assessment.md`
- `document-template/20_SE_Cross_Cutting/Measurement-Plan.md`
- `document-template/21_Solution_Evaluation/Solution-Performance-Analysis.md`
- `Recommended-Actions.md`

If no canonical backlog, roadmap, or experiment template exists, say so and mark the output as project-specific or external. Never invent a template filename merely because the concept is expected in the career path.

## BOK grounding

A Product Manager soul commonly uses:

- BABOK: elicitation, requirements life cycle, strategy analysis, requirements analysis/design, solution evaluation, techniques.
- PMBOK: value delivery, life cycles, scope, schedule, finance, stakeholders, risk.
- DMBOK: analytics context, data quality, governance, warehousing/BI.
- SWEBOK: requirements plus enough architecture, quality, security, management, and economics literacy for technical partnership.

Verify exact filenames; overview wikilinks may use shorthand or illustrative targets that do not match the filesystem.

## Review checklist

Before presenting the collection-only draft:

- [ ] Career path classification checked (`product-and-business` / `manager` vs engineering-specialist).
- [ ] Product path is primary and every capability has an operating charter.
- [ ] Senior SWE foundation is mapped compactly, not duplicated.
- [ ] Role boundaries with full-stack, QA, DevOps, UI/UX, and project management are explicit.
- [ ] Discovery, strategy, analytics, roadmap, and outcome review are present.
- [ ] Product documents use verified paths; backlog/roadmap/experiment gaps are labeled honestly.
- [ ] Existing identity and useful principles are preserved unless the user asks for a new persona.
- [ ] Resolver script passes, plus folder-only and multi-file template references are spot-checked.
- [ ] Live profile is untouched until the user explicitly approves the collection draft.

## Approval and sync

Use the same review-first lifecycle as other soul upgrades:

1. Write only to `soul-collection/<DOMAIN>/<position>-soul.md`.
2. Let the user review role framing, boundaries, priorities, and document depth.
3. After approval, back up the live profile soul under `$HERMES_HOME/profiles/_soul_backup_<YYYYMMDD>/`.
4. Copy the approved collection soul into the live profile.
5. Compare hashes; they must match byte-for-byte.
6. Run a fresh `hermes -p <profile> chat -q` identity/principle smoke test.
7. Do not change registry/main-soul routing for a level upgrade; only new profiles need routing changes.
