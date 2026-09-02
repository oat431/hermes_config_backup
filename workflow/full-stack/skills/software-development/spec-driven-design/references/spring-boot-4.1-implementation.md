# Spring Boot 4.1 / Java 25 — Implementation Patterns

> Discovered during Flowero Discover (Eureka Server) implementation, 2026-07-23, and Flowero Gate adaptation, 2026-07-24.
> These patterns apply to all Panomete foundation services: Flowero Discover, Flowero Gate, and any future Spring Boot 4.1 services.

---

## 1. Build Configuration (Verified Working)

```groovy
plugins {
    id 'java'
    id 'org.springframework.boot' version '4.1.0'
    id 'io.spring.dependency-management' version '1.1.7'
}

java {
    toolchain {
        languageVersion = JavaLanguageVersion.of(25)
    }
}

ext {
    set('springCloudVersion', "2025.1.2")  // Oakwood release train
}

dependencies {
    implementation 'org.springframework.boot:spring-boot-starter-actuator'
    // Eureka: spring-cloud-starter-netflix-eureka-server
    // Gateway: spring-cloud-gateway-server-webflux (renamed in Oakwood)
    testImplementation 'org.springframework.boot:spring-boot-starter-test'
}

dependencyManagement {
    imports {
        mavenBom "org.springframework.cloud:spring-cloud-dependencies:${springCloudVersion}"
    }
}
```

| Artifact | Version | Notes |
|----------|---------|-------|
| Spring Boot | 4.1.0 | Latest GA |
| Spring Cloud | 2025.1.2 | Oakwood release train |
| Java | 25 (LTS) | GraalVM 25 works; Eclipse Temurin 25 also OK |
| Gradle | 9.5.1 | Wrapper included in project |

---

## 2. TestRestTemplate → RestTemplate (Boot 4.1 Breaking Change)

`TestRestTemplate` (from `org.springframework.boot.test.web.client`) is **not available** in Spring Boot 4.1.x with only `spring-boot-starter-test`. Use plain `RestTemplate` instead:

```java
// ❌ DOES NOT COMPILE in Boot 4.1:
import org.springframework.boot.test.web.client.TestRestTemplate;
@Autowired private TestRestTemplate restTemplate;

// ✅ WORKS:
import org.springframework.web.client.RestTemplate;

@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
class MyServiceTest {

    @LocalServerPort
    private int port;

    private RestTemplate restTemplate;

    @BeforeEach
    void setUp() {
        restTemplate = new RestTemplate();
    }

    private String url(String path) {
        return "http://localhost:" + port + path;
    }

    @Test
    void healthCheck() {
        ResponseEntity<String> resp = restTemplate.getForEntity(
            url("/actuator/health"), String.class);
        assertThat(resp.getBody()).contains("\"status\":\"UP\"");
    }
}
```

---

## 3. Eureka Dual-Port via Docker Mapping

ADR-D005 specifies separate ports for Eureka (8999 BE, 3999 FE), but Eureka serves both API and dashboard from a single embedded server. Solution: **Docker port mapping**.

```yaml
# docker-compose fragment
services:
  flowero-discover:
    ports:
      - "8999:8999"   # BE: REST API for service registration
      - "3999:8999"    # FE: Dashboard (maps to same Eureka server)
```

Nginx routes `discovery.panomete.com` → `flowero-discover:3999`, services call `flowero-discover:8999`. Both hit the same Eureka instance on internal port 8999.

---

## 4. Eureka Standalone Configuration

```yaml
server:
  port: 8999

eureka:
  instance:
    hostname: flowero-discover
  client:
    register-with-eureka: false
    fetch-registry: false
  server:
    enable-self-preservation: true       # Homelab: keep registry on transient hiccups
    eviction-interval-timer-in-ms: 5000  # Check for dead instances every 5s
    renewal-percent-threshold: 0.85      # Self-preservation below 85% heartbeats
    wait-time-in-ms-when-sync-empty: 0   # Don't wait to serve empty registry

management:
  endpoints:
    web:
      exposure:
        include: health,info
```

---

## 5. Known Cosmetic Shutdown Noise (Harmless)

These log messages appear during Eureka Server shutdown and are **harmless**:

```
INFO  o.s.c.n.e.s.EurekaServiceRegistry : Unregistering application FLOWERO-DISCOVER with eureka with status DOWN
ERROR c.n.d.s.t.j.EurekaJersey3ClientImpl : Cannot clean connections
    java.lang.IllegalStateException: Client instance has been closed.
```

- **"Unregistering"**: Spring Cloud lifecycle always tries to unregister on shutdown. With `register-with-eureka: false`, no instance was ever registered — this is a no-op log.
- **"Cannot clean connections"**: Jersey 3 client's `ConnectionCleanerTask` runs after the client is closed. Harmless race condition on shutdown.

Do NOT add error-suppression config for these — they're benign and only appear during graceful shutdown.

---

## 6. Windows / MSYS JAVA_HOME Path Mangling

On Windows with Git Bash/MSYS, `JAVA_HOME="/c/Program Files/graalvm-25"` gets mangled to `C:\c\Program Files\graalvm-25` (double `c\`). Gradle's Java toolchain auto-detection still works — the warning is cosmetic:

```
Directory 'C:\c\Program Files\graalvm-25' used for java installations does not exist
```

**Fix**: Use Windows-native path with proper escaping:
```bash
export JAVA_HOME="C:/Program Files/graalvm-25"   # forward slashes work
```
Or just ignore — the Gradle toolchain finds Java 25 regardless.

---

## 7. Multi-Stage Docker Build (Java 25)

```dockerfile
FROM eclipse-temurin:25-jdk-noble AS build
WORKDIR /app
COPY gradlew gradlew.bat ./
COPY gradle/ gradle/
COPY build.gradle settings.gradle ./
RUN chmod +x gradlew && ./gradlew dependencies --no-daemon -q || true
COPY src/ src/
RUN ./gradlew bootJar --no-daemon

FROM eclipse-temurin:25-jre-noble
WORKDIR /app
RUN groupadd -r flowero && useradd -r -g flowero flowero
COPY --from=build /app/build/libs/*.jar app.jar
EXPOSE 8999 3999
USER flowero
ENTRYPOINT ["java", "-Xms128m", "-Xmx192m", "-XX:+UseZGC", "-jar", "app.jar"]
```

JVM flags per platform SAD resource allocation:
- Flowero Discover: `-Xms128m -Xmx192m` (256 MB total)
- Flowero Gate: `-Xmx384m` (512 MB total)
- Flowero Guard (Keycloak): `-Xmx768m` (1 GB total)

---

## 8. Eureka Server Test Suite Pattern

Six-test pattern for verifying an Eureka server:

| Test | What It Verifies |
|------|-----------------|
| `contextLoads()` | Spring context starts without error |
| `actuatorHealthReturnsUp()` | Health endpoint returns `{"status":"UP"}` |
| `eurekaDashboardIsReachable()` | Dashboard HTML contains "Instances currently registered with Eureka" |
| `eurekaAppsEndpointReturnsEmptyRegistry()` | `/eureka/apps` returns valid XML (no `Accept` header) |
| `eurekaAppsEndpointReturnsJsonWithAcceptHeader()` | `/eureka/apps` returns JSON with `Accept: application/json` |
| `doesNotRegisterWithItself()` | Response does NOT contain the server's own app name |

All use `@SpringBootTest(webEnvironment = RANDOM_PORT)` + manual `RestTemplate`.

---

## 9. OAuth2 Client Test Configuration (Spring Security 7 + Boot 4.1)

> **Discovered during Flowero Gate adaptation, 2026-07-24.**

### The Problem Chain

When a `SecurityWebFilterChain` uses **both** `.oauth2ResourceServer()` (JWT validation) **and** `.oauth2Login()` (browser login flow), Spring Security 7 requires a `ReactiveClientRegistrationRepository` bean for the OAuth2 client portion. This triggers a cascade in tests:

1. **`PlaceholderResolutionException`** — if any `@Value` property used by `SecurityConfig` has no default and no test value
2. **`clientRegistrationRepository cannot be null`** — once the placeholder is resolved, the OAuth2 client auto-config demands a client registration
3. **`ClientRegistrations.java:289` / `ConnectException`** — if `issuer-uri` is set in the provider config, Spring Boot's `OAuth2ClientPropertiesMapper` calls `ClientRegistrations.fromIssuerLocation()` which **fetches the OIDC discovery document over HTTP** — fails when no auth server is running during tests

### The Fix: Explicit Provider Endpoints (No `issuer-uri`)

In the test `application.yaml`, configure the OAuth2 client provider with **explicit endpoint URIs** and **omit `issuer-uri`**. When `issuer-uri` is absent, Spring Boot builds the `ClientRegistration` from the explicit URIs without any HTTP fetch:

```yaml
# ✅ test/src/resources/application.yaml
spring:
  security:
    oauth2:
      resourceserver:
        jwt:
          issuer-uri: http://localhost:9000/realms/panomete
          jwk-set-uri: http://localhost:9000/realms/panomete/protocol/openid-connect/certs
      client:
        registration:
          keycloak:
            client-id: flowero-gateway
            client-secret: test-secret-do-not-use-in-prod
            authorization-grant-type: authorization_code
            redirect-uri: "{baseUrl}/login/oauth2/code/{registrationId}"
            scope: openid,profile,email
        provider:
          keycloak:
            # ⚠️ NO issuer-uri — use explicit endpoints to avoid OIDC metadata fetch
            authorization-uri: http://localhost:9000/realms/panomete/protocol/openid-connect/auth
            token-uri: http://localhost:9000/realms/panomete/protocol/openid-connect/token
            user-info-uri: http://localhost:9000/realms/panomete/protocol/openid-connect/userinfo
            jwk-set-uri: http://localhost:9000/realms/panomete/protocol/openid-connect/certs
            user-name-attribute: preferred_username
```

### Why NOT `OAuth2ClientAutoConfiguration` Exclusion?

Excluding `ReactiveOAuth2ClientAutoConfiguration` removes the `ReactiveClientRegistrationRepository` bean entirely, but the production `SecurityConfig` still calls `.oauth2Login()` — which requires it. The chain then fails with `clientRegistrationRepository cannot be null`. Excluding the auto-config only works if the test also replaces the `SecurityWebFilterChain` (via `@Primary` `TestSecurityConfig`).

### TestSecurityConfig Pattern (for non-security tests)

For tests that don't need OAuth2 login (route tests, filter tests, context loads), use a permissive `@TestConfiguration`:

```java
@TestConfiguration
public class TestSecurityConfig {
    @Bean
    @Primary
    SecurityWebFilterChain testSecurityFilterChain(ServerHttpSecurity http) {
        return http
            .csrf(csrf -> csrf.disable())
            .authorizeExchange(auth -> auth.anyExchange().permitAll())
            .oauth2ResourceServer(oauth2 -> oauth2.jwt(Customizer.withDefaults()))
            .build();
        // Note: no .oauth2Login() — avoids clientRegistrationRepository requirement
    }
}
```

Import it in tests that don't verify auth enforcement: `@Import(TestSecurityConfig.class)`.

### Key Insight

`ClientRegistrations.fromIssuerLocation(issuer)` triggers an HTTP GET to `{issuer}/.well-known/openid-configuration`. Setting `issuer-uri` in `spring.security.oauth2.client.provider` activates this path. **Omit `issuer-uri` and set the individual endpoint URIs directly** to bypass the fetch — Spring Boot's `OAuth2ClientPropertiesMapper` falls through to `ClientRegistration.withRegistrationId()` when `issuer-uri` is null.

---

## 10. CORS Wildcard Patterns (`addAllowedOriginPattern` vs `setAllowedOrigins`)

> **Discovered during Flowero Gate CORS fix, 2026-07-24.**

### The Problem

Spring's `CorsConfiguration.setAllowedOrigins()` does **NOT** support wildcard subdomain patterns like `https://*.panomete.com`. Passing such a value results in a literal string match — no wildcard expansion occurs.

```java
// ❌ Does NOT work as expected — "*.panomete.com" is treated as a literal string
config.setAllowedOrigins(List.of("https://*.panomete.com"));
```

### The Fix

Use `CorsConfiguration.addAllowedOriginPattern()` which supports Spring's glob-style `*` origin patterns:

```java
// ✅ Works — wildcard subdomain matching
@Value("${cors.allowed-origins:https://*.panomete.com}")
private String allowedOriginsRaw;

@Bean
public CorsConfigurationSource corsConfigurationSource() {
    CorsConfiguration config = new CorsConfiguration();
    Arrays.stream(allowedOriginsRaw.split(","))
            .map(String::trim)
            .forEach(config::addAllowedOriginPattern);  // ← key difference
    config.setAllowCredentials(true);
    config.setAllowedMethods(List.of("GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"));
    // ...
}
```

### Caveat: `addAllowedOriginPattern` + `allowCredentials(true)`

When `allowCredentials` is true, Spring rejects the literal `*` pattern (matching all origins). Domain-scoped patterns like `https://*.panomete.com` are fine — only bare `*` is blocked:

```
IllegalArgumentException: When allowCredentials is true,
    allowedOrigins cannot contain the special value "*"
```

Use a scoped wildcard like `https://*.panomete.com` instead of `*`.

---

## 11. `@Value` Default Removal — Test Cascade Failure

> **Discovered during Flowero Gate Fix 7, 2026-07-24.**

### The Pattern

When you remove a default from `@Value("${prop:someDefault}")` → `@Value("${prop}")`, the change appears trivial — but every `@SpringBootTest` that loads the production configuration will fail with `PlaceholderResolutionException`. The Spring context cannot start, and ALL tests in the class fail — not just the ones using the property.

### Checklist When Removing a `@Value` Default

1. Search all `src/test/resources/application.*` files for the now-required property
2. Add the property to each test config
3. Run `./gradlew test` before declaring the change complete
4. If the property lives in `SecurityConfig` (which depends on `ReactiveClientRegistrationRepository` and `OAuth2ClientAutoConfiguration`), verify the full chain — the placeholder error will mask the `clientRegistrationRepository cannot be null` error underneath

### Recommended: Keep a Sensible Default

Unless the property must be explicitly set in every environment, keep a platform-level default:

```java
// Safer — test contexts work without extra config
@Value("${app.post-login-redirect-url:https://panomete.com}")

// Riskier — requires every test config to supply the value
@Value("${app.post-login-redirect-url}")
```
