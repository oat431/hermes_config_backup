# Spring Cloud Gateway Security Pitfalls

> Recurring defects found during code review of Spring Cloud Gateway + Spring Security (Boot 4.x / Security 7.x) projects. These are class-level pitfalls — they will recur across Spring Boot gateway projects. Cite these when reviewing `SecurityConfig.java`, filter classes, and rate-limiter configs.

## Pitfall 1: JWKS cache never refreshes (HIGH)

**Symptom:** After Keycloak rotates its signing keys, all new tokens are rejected with 401 until the gateway is restarted.

**Root cause:** `oauth2ResourceServer().jwt(Customizer.withDefaults())` uses the default `ReactiveJwtDecoder`, which caches the JWKS from the `jwk-set-uri` indefinitely. There is no automatic refresh on key rotation.

**Where to look:** `SecurityConfig.java`, the `oauth2ResourceServer` chain. If you see `Customizer.withDefaults()` with no explicit `ReactiveJwtDecoder` bean, this pitfall is present.

**Fix:**
```java
@Bean
public ReactiveJwtDecoder jwtDecoder() {
    return NimbusReactiveJwtDecoder
        .withJwkSetUri(jwksUri)
        .jwsAlgorithm(SignatureAlgorithm.RS256)
        .cache(Duration.ofMinutes(5))   // <-- the missing piece
        .build();
}
```

**Defect report template:** "Gate caches Keycloak JWKS on startup and never refreshes. After key rotation, all new tokens rejected until Gate restarts."

---

## Pitfall 2: CORS preflight (OPTIONS) returns 401 (HIGH)

**Symptom:** Browser cross-origin requests fail at the preflight stage. The actual authenticated request is never sent. API clients work fine (they send the token directly); only browser clients break.

**Root cause:** `SecurityConfig` configures `.anyExchange().authenticated()` without permitting `OPTIONS` preflight requests. Spring Security's authorization check runs before the CORS filter can generate a preflight response. Browsers never send `Authorization` on OPTIONS, so the preflight fails with 401.

**Where to look:** `SecurityConfig.java`, the `authorizeExchange` chain. If `HttpMethod.OPTIONS` is not in the `permitAll()` matchers, this is present. Also check `CorsConfig.java` — the `CorsWebFilter` must be ordered BEFORE the `SecurityWebFilterChain` (typically `@Order(-1)` or a dedicated `CorsWebFilter` bean).

**Fix (two options):**

Option A — permit OPTIONS:
```java
.authorizeExchange(auth -> auth
    .pathMatchers(HttpMethod.OPTIONS, "/**").permitAll()   // <-- add this
    .pathMatchers("/actuator/**", ...).permitAll()
    .anyExchange().authenticated()
)
```

Option B — order CorsWebFilter first:
```java
@Bean
@Order(-1)  // Before SecurityWebFilterChain
public CorsWebFilter corsWebFilter() { ... }
```

**Defect report template:** "CORS OPTIONS preflight requests to authenticated routes return 401. Browser clients completely blocked from calling gateway APIs."

---

## Pitfall 3: Claim-forwarding filter skips client_credentials tokens (MEDIUM)

**Symptom:** Service-to-service calls (client_credentials grant) produce no identifying headers downstream. Downstream services cannot audit or authorize the calling service.

**Root cause:** A `GlobalFilter` like `JwtClaimHeaderFilter` extracts `sub`, `email`, `realm_access.roles`, `scope` — but client_credentials tokens have no `email` claim and `sub` is the client ID (not a user). If the filter doesn't also extract `client_id` (or fall back to it), downstream gets nothing.

**Where to look:** Any `GlobalFilter` / `JwtClaimHeaderFilter` that mutates the request to inject `X-User-*` headers. Check whether it handles the case where user-specific claims are absent.

**Fix:**
```java
String clientId = jwt.getClaimAsString("client_id");
if (clientId != null) {
    builder.header("X-Client-Id", clientId);
}
// For user tokens:
String sub = jwt.getClaimAsString("sub");
if (sub != null && !sub.equals(clientId)) {
    builder.header("X-User-Id", sub);
}
```

**Defect report template:** "`JwtClaimHeaderFilter` does not forward claims for client_credentials tokens. Downstream services cannot identify the calling service."

---

## Pitfall 4: Rate-limit counters lost on cache restart (MEDIUM)

**Symptom:** After the rate-limiter cache (Valkey/Redis) restarts, all rate-limit counters reset. Clients that were throttled can immediately resume full rates.

**Root cause:** Spring Cloud Gateway's `RequestRateLimiter` stores counters in Redis, but the Redis/Valkey instance has no persistence configured (no RDB `save`, no AOF `appendonly`). On restart, the keyspace is wiped.

**Where to look:** The Valkey/Redis container config (`docker-compose.yml`). Check for `save`, `appendonly`, or `--appendonly yes` in the command/args. Also check whether the gateway has a fail-open circuit around the rate-limiter (`ResilientRedisRateLimiter`-style wrapper).

**Fix (container side):**
```yaml
# docker-compose.yml for valkey/redis
command: ["valkey-server", "--appendonly", "yes", "--save", "60", "1000"]
```

**Defect report template:** "Rate limit counters reset when Valkey container restarts. Rate-limited clients can immediately resume full request rates."

---

## Pitfall 5: TraceIdFilter overwrites upstream trace IDs (MEDIUM)

**Symptom:** Distributed tracing breaks. The trace ID from Nginx/Cloudflare is overwritten at the gateway, so downstream services show a different trace ID than the edge logs.

**Root cause:** A `TraceIdFilter` (custom `GlobalFilter`) unconditionally generates a new trace ID without checking for an existing `X-Request-Id` or `X-B3-TraceId` header from upstream.

**Where to look:** Any `TraceIdFilter` / `GlobalFilter` that calls `UUID.randomUUID()` or `MDC.put("traceId", ...)`. Check for a pre-existing-header guard.

**Fix:**
```java
String existing = exchange.getRequest().getHeaders().getFirst("X-Request-Id");
String traceId = (existing != null) ? existing : UUID.randomUUID().toString();
builder.header("X-Request-Id", traceId);
```

---

## Pitfall 6: Missing security headers (MEDIUM)

**Symptom:** No `X-Content-Type-Options`, `X-Frame-Options`, `X-XSS-Protection`, `Strict-Transport-Security`, `Content-Security-Policy`, `Referrer-Policy` in responses.

**Root cause:** `SecurityConfig` doesn't configure `.headers(headers -> headers.contentTypeOptions(...).frameOptions(...).httpStrictTransportSecurity(...))`. Spring Security's defaults changed across major versions; Boot 4 / Security 7 does not add all of these by default.

**Where to look:** `SecurityConfig.java` — the `SecurityWebFilterChain` bean. If there's no `.headers(...)` block, this is present.

**Fix:**
```java
.headers(headers -> headers
    .contentTypeOptions(Customizer.withDefaults())
    .frameOptions(frame -> frame.mode(SameOrigin))
    .httpStrictTransportSecurity(hsts -> hsts.includeSubdomains(true).maxAge(31536000))
    .referrerPolicy(referrer -> referrer.policy(ReferrerPolicy.STRICT_ORIGIN_WHEN_CROSS_ORIGIN))
)
```

---

## How to use this file during a review

1. Open the project's `SecurityConfig` (or equivalent) first. Match it against Pitfalls 1, 2, 6.
2. Open all `filter/` classes. Match against Pitfalls 3, 5.
3. Open `RateLimiterConfig` / `CorsConfig` and the compose file. Match against Pitfalls 2, 4.
4. For each pitfall that matches, file a defect in `043_defect_report.md` using the template wording, customized with the project's actual class names and endpoint paths.
5. Cross-reference against the project's ADRs — if an ADR says "JWT local validation with zero per-request latency" but Pitfall 1 is present, the code does not honor the ADR. That strengthens the defect severity.

These pitfalls are not exhaustive — each new project will surface project-specific defects too. But checking these six first covers the most common Spring Cloud Gateway security gaps.
