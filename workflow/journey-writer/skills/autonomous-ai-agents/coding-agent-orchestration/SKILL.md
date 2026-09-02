---
name: coding-agent-orchestration
description: "Use when orchestrating Hermes profiles and coding agents."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [windows, linux, macos]
metadata:
  hermes:
    tags: [orchestration, coding-agents, harnesses, multi-model, worktrees, profiles]
    related_skills: [claude-code, codex, opencode, skill-library-maintenance]
---

# Hermes Commander + Coding Harness Orchestration

## Overview

Use Hermes as the **commander** and coding harnesses as bounded **hands**. Hermes owns the mission, routing, durable context, profile coordination, safety gates, and final verification. Claude Code, Codex, OpenCode, and other coding agents own repository manipulation: reading code, editing files, running tests, and returning a diff.

Do not move the user's Hermes personas into a harness. `product-owner`, `full-stack`, `qa`, `security-engineer`, `ui-ux`, and `devops` remain domain experts in Hermes. Their decisions become a focused implementation packet for the selected harness. The harness receives the context it needs for the current repository task, not the entire Hermes soul, memory, or fleet.

The four layers are deliberately separate:

| Layer | Owns | Does not own |
|---|---|---|
| **Hermes commander** | Mission, routing, coordination, approvals, evidence-based reporting | Blindly editing a large repository when a harness is better suited |
| **Specialist profiles** | Requirements, architecture, QA, security, UX, infrastructure decisions | Replacing the implementation worker by default |
| **Coding harness** | Repository inspection, edits, tests, local diff, bounded repair loops | Unapproved push, deploy, publication, or architecture changes |
| **LLM provider/model** | Reasoning and tool-call generation for the harness | Workflow ownership, repository policy, or user approval |

For the current provider/harness landscape and official links, load `references/harness-landscape.md`. Its facts are version-sensitive; re-check upstream documentation before relying on a command or capability.

## When to Use

Use this skill when:

- a specification or implementation brief is ready to become repository changes;
- the user asks Hermes to use Claude Code, Codex, OpenCode, or another coding agent;
- a task needs a provider-agnostic coding worker or a vendor-native worker;
- multiple specialists must contribute before implementation;
- parallel implementation or review requires isolated worktrees;
- a harness must implement, test, review, or repair code under Hermes supervision.

Do not use this as a substitute for requirements elicitation, architecture design, or security expertise. Route those decisions to the appropriate Hermes profile first, then return here for execution orchestration.

## Commander Workflow

### 1. Classify the mission

Resolve which stage the user is actually requesting:

- **Design stage:** requirements, architecture, API, schema, UX, threat model, or test strategy. Use the relevant specialist; do not launch a write-capable harness merely to discover the design.
- **Implementation stage:** the design is sufficiently settled and repository changes are wanted. Build an implementation packet before launching a worker.
- **Review stage:** inspect an existing diff or PR. Prefer read-only review first; do not let a reviewer silently rewrite code.
- **Repair stage:** fix specific verified findings. Constrain the worker to the reported issues and re-run the same verification gates.

**Done when:** the requested stage and the allowed side effects are explicit.

### 2. Coordinate domain experts

Keep personas in Hermes and ask only the profiles relevant to the change:

| Concern | Profile | Expected output |
|---|---|---|
| Scope, value, prioritization | `product-owner` | Goal, non-goals, user stories, MVP boundary |
| Architecture, API, database, code design | `full-stack` | Design decisions, contracts, affected components |
| Acceptance behavior and regression risk | `qa` | Test strategy, cases, edge conditions, exit criteria |
| Threats, trust boundaries, secrets, abuse cases | `security-engineer` | Threat findings, security requirements, review gates |
| Interaction and visual behavior | `ui-ux` | User flows, states, accessibility and UI constraints |
| CI/CD, deployment, infrastructure | `devops` | Environment, pipeline, rollout and rollback constraints |

Do not ask every profile for a review by default. Select the smallest set that covers the risk. The commander consolidates their outputs and resolves contradictions before handing work to a harness.

**Done when:** decisions are consolidated into one coherent brief, with unresolved questions surfaced instead of silently guessed.

### 3. Build the implementation packet

Give the harness a bounded, repository-native packet containing:

1. **Objective** — what outcome must exist.
2. **Non-goals** — what must not change.
3. **Repository context** — absolute/approved workdir, branch or base revision, relevant project rules, and required package/runtime commands.
4. **Design decisions** — approved architecture and alternatives rejected.
5. **Contracts** — API, data model, events, interfaces, file formats, or UI states.
6. **Acceptance criteria** — observable Given/When/Then behavior.
7. **Test plan** — tests to add or update, plus lint/typecheck/build commands.
8. **Security constraints** — secret handling, authorization, input validation, dependency restrictions, and prohibited operations.
9. **Execution boundaries** — worktree requirement, permitted files, whether commits are forbidden, and whether network access is needed.
10. **Output contract** — changed files, commands run, actual results, remaining risks, and final `git diff` summary.

Prefer a file reference such as `SPEC.md` or `IMPLEMENTATION.md` when the packet is large. Do not paste secrets, `.env` contents, tokens, or private credentials into the prompt.

**Done when:** another agent could implement the task without inventing missing architecture or scope.

### 4. Select the hands

Choose the harness by workflow need, not brand loyalty:

- **OpenCode:** default choice when provider flexibility, local models, MCP, skills, primary agents, or subagents matter.
- **Claude Code:** choose for Anthropic-native workflows, long autonomous implementation loops, Claude worktrees, or Claude-specific features.
- **Codex:** choose for OpenAI/Codex-native implementation, PR work, or an existing Codex OAuth workflow.
- **Aider:** choose for focused patching, git-aware pair programming, repository-map work, scripting, or broad LiteLLM model access.
- **OpenHands:** choose when an SDK, programmable agent, custom tools, sandboxed/cloud execution, or a reusable coding-agent platform is needed.
- **Goose:** choose when MCP extensions, multi-model operation, or subscription-backed ACP providers are central.
- **Pi:** choose when a small, highly extensible coding-agent kernel and custom providers/tools are preferred.
- **Qwen Code, Crush, and similar tools:** evaluate for a specific need; do not present them as interchangeable defaults without checking current maturity, provider support, licensing, and Windows behavior.
- **Parallel-agent managers:** use only when their lifecycle and maintenance status are verified. Do not build a new workflow around a tool whose upstream status has changed.

The harness is replaceable. Keep the implementation packet and verification contract independent of the chosen worker.

**Done when:** the selected harness has a verified invocation path, authentication path, workdir, permission mode, and stop condition.

### 5. Isolate and launch

Before a write-capable worker starts:

1. Resolve and verify the repository workdir.
2. Inspect `git status`; preserve or explicitly account for pre-existing changes.
3. Use a dedicated branch/worktree for parallel or risky work.
4. Load repository rules (`AGENTS.md`, `CLAUDE.md`, project instructions) through the harness where supported.
5. Use the narrowest permission mode that can complete the task.
6. State explicitly: implement the packet, run the required checks, do not push/deploy, and do not broaden scope.
7. Set a bounded timeout, turn limit, budget, or equivalent when the harness supports it.

Use one worktree per concurrent worker. Never let two agents write to the same working directory unless the workflow explicitly serializes them.

**Done when:** the worker is running in the intended workdir with the intended permissions and the starting repository state is recorded.

### 6. Monitor without taking ownership away

For short bounded tasks, use the harness's non-interactive/print mode. For iterative work, use its PTY/background mode and monitor output through the process handle or session log.

When a worker asks a question:

- answer only from the approved packet and repository evidence;
- route a new product, architecture, security, or scope decision back to the relevant Hermes profile;
- do not invent an answer merely to keep the worker moving.

If the worker reports completion, treat that as a handoff—not proof. Continue to verification.

**Done when:** the worker has exited cleanly or is stopped for a documented reason, and its output is available for inspection.

### 7. Verify the actual artifact

Hermes must independently inspect the result:

1. Read `git status` and the complete changed-file list.
2. Inspect the diff; check for unrelated edits, generated secrets, accidental deletions, and scope creep.
3. Read the relevant changed files rather than trusting the worker's summary.
4. Run the project's required tests, lint, typecheck, build, and security checks.
5. Compare behavior against every acceptance criterion.
6. Check that tests exercise the new behavior and important failure paths.
7. Route independent review to `qa`, `security-engineer`, `full-stack`, or a separate reviewer context when risk warrants it.
8. Record actual command output and distinguish baseline failures from regressions.

No agent should be the sole verifier of its own implementation. A clean prose report is not a passing test result.

**Done when:** every requested criterion and verification command has an observable result, every changed file is accounted for, and remaining risks are stated.

### 8. Repair narrowly, then re-verify

If verification finds issues, send the worker only the concrete findings and the relevant diff/context. Instruct it to fix the findings without unrelated refactoring or feature expansion. Re-run the full verification cycle after each repair cycle.

Stop and escalate when:

- the fix requires a new product or architecture decision;
- the worker changes scope repeatedly;
- verification still fails after a bounded number of repair cycles;
- the repository contains unexpected destructive or sensitive changes.

**Done when:** the repair passes the same gates that originally failed, or the unresolved failure is explicitly escalated.

### 9. Gate external actions

Local edits, tests, and diff inspection are distinct from actions that leave the machine. Ask before:

- committing when the user did not explicitly request it;
- pushing branches or tags;
- creating or commenting on PRs/issues;
- deploying, publishing, sending messages, or changing external infrastructure.

Before requesting approval, report the exact branch, files, tests, risks, and proposed external action.

## Model and Provider Selection

A harness and a model provider are different choices. Select the workflow first, then select the model based on task complexity, tool-use reliability, context needs, privacy, latency, and cost.

- Use a strong reasoning/coding model for architecture-sensitive changes, migrations, concurrency, authentication, and broad refactors.
- Use a cheaper capable model for bounded documentation, repetitive test expansion, or mechanical edits after the design is fixed.
- Use local models only after checking tool-calling quality, context size, repository scale, and test reliability.
- Keep the packet provider-neutral unless a provider-specific feature is intentional.
- Never assume that a harness's support for a provider means every model from that provider supports tools, long context, structured output, or code editing equally well.

## Common Pitfalls

1. **Moving personas into the harness.** Keep Hermes profiles as domain experts; pass their decisions as a scoped packet.
2. **Confusing harness with provider.** OpenCode, Claude Code, Codex, and Aider are execution runtimes; Anthropic, OpenAI, OpenRouter, local servers, and similar services provide models.
3. **Launching before design convergence.** If requirements, contracts, or security boundaries are unresolved, return to the appropriate specialist instead of asking the coder to guess.
4. **Two workers sharing one worktree.** Use separate worktrees or serialize writes.
5. **Unbounded autonomy.** Set workdir, permissions, timeout/turn/budget limits, non-goals, and a stop condition.
6. **Trusting a completion claim.** Inspect the files, diff, and real command output yourself.
7. **Letting the worker commit or deploy by default.** Keep external side effects behind the approval gate.
8. **Using a vendor-native worker when provider flexibility is the main requirement.** Consider OpenCode, Aider, Goose, or Pi instead.
9. **Treating current feature matrices as permanent.** Re-check official docs, especially provider lists, subscription authentication, CLI flags, and project maintenance status.
10. **Reviewing only the happy path.** Require acceptance tests, failure-path tests, security checks, and regression comparison.

## Verification Checklist

- [ ] Mission stage classified: design, implementation, review, or repair
- [ ] Relevant Hermes specialists consulted; unresolved decisions are explicit
- [ ] Implementation packet contains objective, non-goals, contracts, acceptance criteria, tests, boundaries, and output contract
- [ ] Harness and model/provider selected for the task rather than assumed
- [ ] Workdir, git state, branch/worktree, permissions, and stop condition verified
- [ ] No secrets or private credentials entered into the packet
- [ ] Worker output monitored and completion report treated as unverified
- [ ] Actual changed files and diff inspected
- [ ] Tests/lint/typecheck/build/security checks run with real output
- [ ] Acceptance criteria and scope compliance checked
- [ ] Independent review used when risk warrants it
- [ ] External actions held for explicit approval
- [ ] Remaining risks and exact next action reported
