# Template Field Guide — 01_requirement Documents

Maps each major section of the `01_requirement` templates to the interview question(s) that should populate it.

## 011_business_objective.md

| Section | Question(s) to Ask |
|---------|-------------------|
| 1. Executive Summary — Purpose | "Why are you building this? What's the single biggest problem it solves?" |
| 1. Executive Summary — Target Completion | "What's your timeline?" |
| 2. Strategic Alignment | Derived from the Why + Who answers. Map objectives to strategic themes. |
| 3. Business Objectives (SMART) | Specific/Measurable: "What does success look like for [component]?" Time-Bound: from timeline answer. |
| 4. KPI Framework | "How will you know it's working? What metrics matter?" — can often be derived from objectives. |
| 5. Baseline/Target Measurements | "What's the current state?" (usually zero for greenfield). Targets from objectives. |
| 6. Objective Dependencies | Derived from the architectural decisions — which services depend on which. |
| 7. Risk to Objectives | "What could go wrong?" — ask about resource constraints, learning curves, external dependencies. |
| Appendix B: Technology Decisions | "What language/framework? What deployment approach?" |

## 012_user_stories.md

| Section | Question(s) to Ask |
|---------|-------------------|
| 3. Epic Overview | Derived from the scope decision (MVP vs full). |
| 4. Personas | "Who are the users?" plus inferred roles (Platform Admin, Service Developer, End User). |
| 5. User Stories | Drill into each epic: "What exactly does [Service X] need to do? Walk me through the flow." |
| 6. Estimation Summary | Story points assigned by PO. Use Fibonacci (1,2,3,5,8,13). |
| 7. Story Map | Organize stories into milestones (M1: deploy, M2: functional, M3: hardened). |

## 013_acceptance_criteria.md

| Section | Question(s) to Ask |
|---------|-------------------|
| 3. Acceptance Criteria by Requirement | For each user story: "What are the edge cases? What happens when it fails? What does the happy path look like?" |
| Non-Functional ACs | "What performance SLAs matter? What security checks are non-negotiable?" |
| 5. Traceability | Cross-reference each AC back to the user story and objective. |

## 014_stakeholder_analysis.md

| Section | Question(s) to Ask |
|---------|-------------------|
| 2.1 Influence/Interest Matrix | Derived from persona roles and project context. Often self-evident for personal projects. |
| 3.1 Concerns by Stakeholder | "For each persona, what are they most worried about?" |
| 3.2 Stakeholder Conflicts | "Are there any conflicting priorities?" (e.g., speed vs completeness) |
| 4.1 Impact of Project | "How does this change things for each stakeholder?" |

## Key Elicitation Pattern

For **architectural decisions** (language, framework, deployment), the question format is:
> "For [component], do you have a preference, or should I recommend based on your constraints? [Choice 1], [Choice 2], [Choice 3]"

For **scope decisions**, the question format is:
> "What's the MINIMUM set of [things] needed for Phase 1? [Option A: bare minimum], [Option B: moderate], [Option C: everything]"

For **behavioral decisions**, the question format is:
> "When [scenario], what should happen? [Option A: tight coupling], [Option B: loose coupling], [Option C: manual]"

## Document Structure Decision (multi-service projects)

**When to ask:** After writing the platform `011_business_objective.md` and BEFORE writing any `012_user_stories.md`.

**Question format:**
> "Should each service get its own deep-dive documents, with the platform doc as an umbrella linking to them? Or should everything live in one monolithic platform doc?"

**Lead with:** The umbrella + deep-dive pattern. It's the right default for any project with 2+ discrete services.

**When the user picks umbrella + deep-dive:**
- Platform `012_user_stories.md` → thin consolidation (story map, cross-service dependencies, links)
- Each service gets `011_business_objective.md`, `012_user_stories.md`, `013_acceptance_criteria.md`
- Story points and milestones are consolidated at the platform level
- Each service doc must be self-contained for an AI persona to consume independently

**When the user picks monolithic:**
- All stories, ACs, and objectives live in one `012_user_stories.md` and `013_acceptance_criteria.md`
- Acceptable for single-service projects or when all services are tightly coupled
- Harder for AI personas to consume (must read everything)
