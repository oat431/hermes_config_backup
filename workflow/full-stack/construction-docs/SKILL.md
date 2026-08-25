---
name: construction-docs
description: Populate 03_construction documents (README, build scripts, dependency manifest, changelog, coding standards, code review records) from a BUILT codebase. Used AFTER the Dev persona has completed implementation and the build passes — construction docs capture the real code, not the planned code.
---

# Construction Document Population

## Trigger

User has a built, tested service and says "write the construction documents," "fill the 03_construction templates," "update the construction docs," or points at a `03_construction/` directory. The code exists, the build passes — now capture what was actually built into the spec.

## Critical Pitfall: "Update the template" vs "Fill the project docs"

> ⚠️ **This is the most common misread.** When the user says "update the construction template here: `<path>`" and the path points to `template/03_construction/`, they might mean:
> - **A) Update the TEMPLATE FILES themselves** (improve the generic starter templates)
> - **B) Fill in the PROJECT'S construction docs** using the templates as a guide
>
> **If the path is `template/03_construction/` but the user also mentioned a specific project/service, they almost certainly mean (B).** Clarify: "Do you want me to fill the construction docs for [service] at `spec/[service]/03_construction/`, or update the generic templates themselves?" When in doubt, fill the project docs first — the templates are the reference, the project docs are the deliverable.

## Workflow

### Phase 0: Verify the Build (MANDATORY — before writing any doc)

> Construction docs capture what WAS built, not what SHOULD be built. Every fact must be verifiable.

1. **Run `./gradlew build` (or equivalent) and confirm it passes.** Record the exact build output, test counts, artifact sizes.
2. **Read every source file** — the main class, config files, test files, Dockerfile, build scripts.
3. **Collect real data points:**
   - Exact dependency versions (from `build.gradle` / `package.json` / `go.mod`)
   - Test names and their purposes
   - Port numbers, JVM flags, Docker base images
   - Commit history (from `git log --oneline`)
   - Actual build output (timing, artifact sizes)

### Phase 1: Scope Determination

Not every service needs all 6 construction docs. Scope by service type:

| Service Type | 031 README | 032 Build Scripts | 033 Dep Manifest | 034 Changelog | 035 Coding Standards | 036 Code Review |
|-------------|:---:|:---:|:---:|:---:|:---:|:---:|
| **Foundation (Java)** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **Business (any stack)** | ✅ | ✅ | ✅ | ✅ | 🟡 | 🟡 |
| **Off-the-shelf (Keycloak, etc.)** | ✅ | ✅ | 🟡 | — | — | — |

Foundation services (Discover, Gate, Guard) set the standards — they get all 6 docs. Business services inherit coding standards from the platform.

#### Multi-Repo Naming Convention

When a project will be split into separate repositories (e.g., Go backend + Next.js frontend), use repo-type prefixes in the construction document filenames:

```
<doc_no>_<repo_type>_<doc_name>.md
```

Where `<repo_type>` is:
- **BE** — Backend repository (Go, Java, Node.js API, etc.)
- **FE** — Frontend repository (React, Next.js, Vue, etc.)
- **SHARED** — Conventions that apply to both repos (commit messages, coding standards)

**Example split (4 docs → 11 files):**

| Doc Type ID | BE File | FE File | SHARED File |
|:-----------:|---------|---------|-------------|
| 031 (README) | `031_BE_README.md` | `031_FE_README.md` | — |
| 032 (Build Scripts) | `032_BE_build_scripts.md` | `032_FE_build_scripts.md` | — |
| 033 (Dep Manifest) | `033_BE_dependency_manifest.md` | `033_FE_dependency_manifest.md` | — |
| 034 (Commits) | — | — | `034_SHARED_commit_messages_changelog.md` |
| 035 (Coding Standards) | `035_BE_coding_standards.md` | `035_FE_coding_standards.md` | — |
| 036 (Code Review) | `036_BE_code_review_records.md` | `036_FE_code_review_records.md` | — |

**Rules:**
- **Doc number = doctype ID**, NOT a sequential counter. Both BE and FE variants share the same number (031_BE_README + 031_FE_README, not 031_BE + 032_FE).
- Each repo's docs are self-contained — when you split repos, each takes its `BE_` or `FE_` files
- SHARED docs (commit conventions, coding standards) go into BOTH repos at split time
- The `repo_type` prefix should also appear in the frontmatter: `repo_type: "BE"` / `repo_type: "FE"` / `repo_type: "SHARED"`
- Only apply this naming to `03_construction` documents. Requirements (`01_requirement`) and design (`02_design`) docs remain unsplit — they're the shared contract.
- When the user says "only rename 03_construction," don't rename 01 or 02 docs
- Each BE/FE doc should cross-reference its counterpart (BE README links to FE README, etc.)

### Phase 2: Document Production (in priority order)

Produce docs in this order — each builds on the previous:

#### 031 — README / Developer Guide (write first, unblocks everything)

> The front door. Clone → build → run → verify in < 5 minutes.

**Must contain:**
- Service metadata table (type, technology, stack, ports, domain, database, mode)
- Architecture diagram (ASCII art showing ports and consumers)
- Quick Start with real commands that were verified to work
- Configuration reference table — every non-obvious property with its rationale
- API reference (link to 022_API_specification, not duplicate)
- Related services table
- Testing instructions with real test names and results
- Design decisions summary (link to ADRs, not duplicate)

**Stack-specific sections:**
- **Java/Gradle:** `./gradlew build`, `./gradlew bootRun`, Docker with JVM flags
- **Node.js:** `npm install`, `npm run dev`, Docker with `node:20-alpine`
- **Go:** `go build`, `go test ./...`, Docker with `golang:alpine` or scratch

#### 032 — Build Scripts

> Every command that transforms source → artifact. The build pipeline IS the quality gate.

**Must contain:**
- Build pipeline diagram (Mermaid flowchart)
- Command table (build, test, package, run, clean, dependency-check)
- Gradle build phases (from actual `./gradlew build` output)
- Docker multi-stage build walkthrough
- JVM flags table (if Java)
- Docker Compose fragment
- **Verbatim build output** — paste the actual `BUILD SUCCESSFUL` output with test counts

#### 033 — Dependency Manifest

> Every dependency with version, license, and purpose.

**Must contain:**
- Dependency overview table (counts: direct, test, transitive)
- Production dependency table (from `build.gradle` dependencies block)
- Test dependency table
- Key transitive dependencies (the ones that matter)
- BOM/dependency management strategy explanation
- Justification for what's NOT included (no DB driver, no cache client — why?)
- Platform-level shared dependencies (what other services provide)

#### 034 — Commit Messages / Changelog

> Human-readable history derived from Conventional Commits.

**Must contain:**
- Commit format with real service scopes
- Changelog from `0.0.1` → current version with every commit summarized
- Tooling reference (git-cliff, standard-version, commitlint)

#### 035 — Coding Standards

> The rules the code actually follows. Standards without enforcement are suggestions.

**Must contain:**
- Language-specific rules (naming, style, frameworks)
- Test conventions (naming, assertions, patterns)
- Configuration conventions (YAML structure, property ordering)
- Project structure diagram (from actual `tree` output)
- Good vs Bad code examples (from the actual codebase)
- Linting status (what's configured, what's recommended)

#### 036 — Code Review Records

> Traceability for review decisions and lessons learned.

**Must contain:**
- Review process flowchart
- Review checklist (10 items, stack-agnostic)
- At least one review record for the initial implementation
- Findings with severity (🔴 Critical / 🟡 Important / 🟢 Nit)
- Lessons learned section

### Phase 3: Cross-Reference

After writing all docs, verify cross-references:
- Every document's "Related Documents" section links to siblings
- ADR references point to the actual `021_architecture_decision_records.md`
- API references link to `022_API_specification.md`
- Build script references link to `032_build_scripts.md`

## Document Quality Standards

- **Version:** Set to `0.1`, status to `Draft`/`Active`, author to `Dev Persona`
- **Frontmatter:** Include `project_name`, `project_id`, `parent_platform`, `classification`
- **Real data only:** Every table cell populated from actual code/build output — no placeholders
- **Tables over prose:** Configuration, dependencies, and commands go in tables — scannable
- **Code blocks:** Always show real, verified commands and their real output
- **Diagram:** Every 03x doc should have at least one Mermaid diagram

## Pitfalls

- **Writing from requirements instead of code**: Construction docs capture the REAL artifact. If the README says port 8999 but the code says 8080, the code wins. Always verify against actual files.
- **Placeholder values**: Never leave `[Project Name]`, `[X.Y]`, `[YYYY-MM-DD]` in construction docs. Every field must be filled with real data.
- **Generic API references**: Don't say "See the API docs" — link to the specific `022_API_specification.md` in the same spec directory.
- **Template vs project confusion**: Covered in the Critical Pitfall above. When the user points at a path and says "update the construction template," check whether they mean the `template/` directory or the project's `spec/` directory.
- **Spring Boot 4.1 TestRestTemplate**: `TestRestTemplate` from `spring-boot-starter-test` may not resolve in Boot 4.1 Eureka Server tests because the test web environment needs `spring-boot-starter-web` on the classpath. Eureka Server brings its own embedded container but doesn't pull in the web starter. **Fall back to plain `org.springframework.web.client.RestTemplate`** for integration tests — works reliably without extra dependencies.
- **Eureka naming normalization**: `spring.application.name` gets uppercased by Eureka, and hyphens/underscores are preserved. `flowero-discover` → `FLOWERO-DISCOVER`. When writing tests that check app names in Eureka responses, use the uppercased form.
- **Dual-port Eureka in Docker**: Eureka serves both REST API and dashboard from one port (8999). The "dual port" convention (8999 API + 3999 dashboard) is achieved by Docker port mapping: `-p 3999:8999`. No second embedded server needed.
- **GraalVM Java 25 + Gradle**: If `JAVA_HOME` is set to a GraalVM path with a prefix issue (e.g., `/c/Program Files/graalvm-25` resolving to `C:\\c\\Program Files\\...`), Gradle's toolchain auto-detection still finds the JDK. The warning is cosmetic — the build succeeds.
- **Spring Boot 4.1 `@Value` default removal**: When removing a default from `@Value("${prop:default}")`, every test context loading the production config fails with `PlaceholderResolutionException`. The `build` step in Phase 0 catches this — search all `src/test/resources/application.*` files and add the now-required property. This error often masks a deeper `clientRegistrationRepository cannot be null` if `SecurityConfig` uses `.oauth2Login()`. See `spec-driven-design` skill reference `spring-boot-4.1-implementation.md` §9 and §11 for the full debugging chain and OAuth2 client test config pattern.

## Reference Files

- `references/spring-boot-4-eureka-lessons.md` — Technical findings from Spring Boot 4.1 / Eureka Server implementation: TestRestTemplate workaround, Eureka naming normalization, dual-port Docker pattern, Gradle+GraalVM path quirk, shutdown noise, BOM version management.
