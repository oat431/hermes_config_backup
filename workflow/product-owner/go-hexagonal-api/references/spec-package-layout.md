# Spec package layout for a Go API service

User convention: **self-contained spec folder per service**, at `<repo>/.agents/spec/`,
numbered subfolders mirroring the master templates at `F:\projects\project_spec\template\`.

## Doc map (proven for a Go REST+gRPC + Mongo + JWT service)
| # | File | Purpose |
|---|------|---------|
| 000 | `000_spec_index.md` | Doc map, reading order, **assumptions table (A1..An)** — code comments reference A-numbers; status checkboxes |
| 011 | `01_requirement/011_business_objective.md` | Map evaluation criteria (or business goals) → SMART objectives; risk table |
| 012 | `01_requirement/012_user_stories.md` | INVEST stories grouped in epics; points; sequencing note |
| 013 | `01_requirement/013_acceptance_criteria.md` | Given–When–Then per FR, each AC unit-testable; trace to test plan |
| 015 | `01_requirement/015_definition_of_done.md` | Submission checklist incl. bonus verification + quality gates |
| 022 | `02_design/022_API_specification.md` | Full REST contract: endpoints, request/response JSON, error envelope, error codes, operational behaviors; gRPC proto block |
| 023 | `02_design/023_database_schema_DDL.md` | Collection/document schema, indexes, repository ops |
| 025 | `02_design/025_software_architecture_document.md` | Hexagonal package tree, component table, mermaid flow, **ADR table** |
| 031 | `03_construction/031_README_developer_guide.md` | The deliverable README itself (copied to repo root): setup, JWT guide, sample requests, assumptions table |
| 041 | `04_testing/041_test_plan.md` | Level strategy, mocking decision, TC↔AC trace, smoke section |

## Rules observed
- Framework/stack choices land in the ADR table (025) BEFORE implementation — the user explicitly corrects silent defaults.
- The assumptions table (000) is the single source of truth; code comments cite A-numbers; docs get synced to the final implementation (including the module name) before the final commit.
- Spec statuses tick ✅ after live verification, not after code compiles.
- For interview challenges: keep docs lean (no enterprise ceremony); objectives = evaluation criteria mapped to gates.
