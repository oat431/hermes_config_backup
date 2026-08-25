# Spec Migration & Code Review — Reference

Concrete patterns from the Panomete Platform session where specs were migrated
from Java 21 / Boot 3.x / Maven to Java 25 / Boot 4.1 / Gradle, and an existing
flowerogate project was reviewed against the specs.

---

## Spec Version Migration

### Finding all references

```bash
# Wide-net grep across the entire spec tree
grep -rn -i "Java 21\|Spring Boot 3\b\|Boot 3\.x\|Spring Cloud 2023\|temurin.*21\|JDK 21\|JRE 21\|java-version.*21\|eclipse-temurin:21\|21-jdk\|21-jre\|mvnw\|./mvnw\|pom\.xml" \
  "<spec-root>" --include="*.md"
```

This catches references in: business objectives, user stories, ADRs, SAD
component tables, architecture overviews, READMEs, CI/CD configs.

### Files that need updating (priority order)

1. **ADR entry** — full rewrite with Context/Decision/Consequences, not just the
   index line. Example: ADR-004 went from a one-liner ("unchanged from v0.1") to
   a full entry documenting Java 25 LTS rationale, Boot 4.1 reactive-first
   design, and Cloud 2025.1 (Oakwood) artifact rename.

2. **SAD component tables** — each service's "Language / Stack" row. In the
   Panomete SAD, this appeared on both the Discover and Gate component rows.

3. **Requirement docs** (011, 012) — the technology overview table.

4. **Architecture overview** (029) — technology stack table row.

5. **Platform README** — foundation language row.

6. **CI/CD configs** (051) — the most changes:
   - `actions/setup-java` java-version
   - `cache: maven` → `cache: gradle`
   - Build commands: `./mvnw compile` → `./gradlew compileJava`
   - Lint: `./mvnw checkstyle:check spotbugs:check` → `./gradlew checkstyleMain`
   - Package: `./mvnw package -DskipTests` → `./gradlew bootJar`
   - Local run: `./mvnw spring-boot:run` → `./gradlew bootRun`
   - Dockerfile base: `maven:3.9-eclipse-temurin-21` → `eclipse-temurin:25-jdk-alpine`
   - Dockerfile artifact: `/target/*.jar` → `/build/build/libs/*.jar`
   - Repo structure: `pom.xml` → `build.gradle`, `mvnw` → `gradlew`

### What NOT to change

- **Historical meeting minutes** (MM01, MM02, MM03) — these record what was
  decided at the time. A line like "pom.xml / build.gradle" in a TODO item is
  a historical record, not a living instruction.
- **Frontmatter dates** on unchanged docs — don't bump last_updated if the doc
  content didn't change.

### Final sweep

```bash
grep -rn -i "<old-patterns>" "<spec-root>" --include="*.md" | grep -vi "spotbugs"
```

The only acceptable stragglers are in historical meeting minutes.

---

## Existing-Code-vs-Spec Gap Analysis

### Reading order for a Spring Boot gateway project

1. `README.md` + `AGENTS.md` — architecture overview, constraints, conventions
2. `build.gradle` — versions, dependencies (reveals the actual Java/Boot/Cloud versions)
3. `application.yaml` — base config: routes, security, redis, eureka, actuator
4. `application-prod.yaml` — env-var-driven overrides (reveals real deployment config)
5. `application-dev.yaml` — local dev config (reveals expected local infra)
6. `docker-compose.yml` — port bindings, env vars, network config, resource limits
7. `Dockerfile` — base image, build steps, JVM args, healthcheck
8. `SecurityConfig.java` — auth chain, permitAll paths, OAuth2 login flow
9. Custom filters — `JwtClaimHeaderFilter`, `TraceIdFilter`, rate limiter
10. `RateLimiterConfig.java` — key resolvers, fail-open/fail-closed strategy

### Gap categories

| Category | Criteria | Example |
|----------|----------|---------|
| 🔴 Must-fix | Blocks deployment or contradicts architecture | Wrong realm name, `host.docker.internal`, wrong routes, missing `db-network` |
| 🟡 Nice-to-have | Non-blocking but should align eventually | CORS origins, hardcoded redirect URLs, management port inconsistency |
| ✅ Aligned | Matches or exceeds spec requirements | JWT validation, claim headers, rate limiting, structured logging |

### Key lesson: ask before assuming direction

When the existing code uses a NEWER version than the specs say:

```
Spec:  Java 21 / Spring Boot 3.x
Code:  Java 25 / Spring Boot 4.1
```

**Do NOT assume** the code should be downgraded. The user may have intentionally
upgraded and just forgot to update the specs. Present both options:

1. Downgrade code to match specs (safer, but discards working code)
2. Upgrade specs to match code (keeps code, updates all docs)

The user will often choose option 2 with a response like "yes, I forgot to tell
you." Then execute the spec migration (see above).
