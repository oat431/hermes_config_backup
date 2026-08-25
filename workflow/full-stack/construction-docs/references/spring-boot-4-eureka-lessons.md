# Spring Boot 4.1 / Eureka — Technical Lessons (2026-07-23)

> Captured from the Flowero Discover implementation session. Reference for future Java foundation services.

---

## TestRestTemplate in Spring Boot 4.1

**Problem:** `org.springframework.boot.test.web.client.TestRestTemplate` fails to resolve in Eureka Server integration tests:

```
error: package org.springframework.boot.test.web.client does not exist
import org.springframework.boot.test.web.client.TestRestTemplate;
```

**Root Cause:** Spring Boot 4.1's `TestRestTemplate` lives in `spring-boot-test` (included in `spring-boot-starter-test`), but the auto-configuration for the test web environment needs `spring-boot-starter-web` on the classpath. Eureka Server pulls in its own embedded Tomcat but doesn't depend on the web starter.

**Fix:** Use plain `org.springframework.web.client.RestTemplate` instead. It's pulled in transitively by Eureka's dependencies and works without extra configuration:

```java
// ✅ Works — plain RestTemplate
import org.springframework.web.client.RestTemplate;

private RestTemplate restTemplate;

@BeforeEach
void setUp() {
    restTemplate = new RestTemplate();
}

// ❌ Broken in Boot 4.1 Eureka tests
import org.springframework.boot.test.web.client.TestRestTemplate;
```

---

## Eureka Naming Normalization

Eureka transforms `spring.application.name` according to these rules:

| Input | Eureka App Name |
|-------|----------------|
| `flowero-discover` | `FLOWERO-DISCOVER` |
| `flowero_discover` | `FLOWERO_DISCOVER` |
| `cute-gufo` | `CUTE-GUFO` |

**Rules:**
1. Uppercase everything
2. Preserve hyphens and underscores as-is
3. Strip leading/trailing whitespace

When writing tests that query `/eureka/apps` and check for specific app names, **use the uppercased form**.

---

## Dual-Port Eureka in Docker

Eureka Server serves both REST API and HTML dashboard from a single embedded server on one port. The "dual port" convention (ADR-D005: 8999 BE + 3999 FE) is achieved purely through Docker port mapping:

```yaml
ports:
  - "8999:8999"   # BE: REST API for service registration/discovery
  - "3999:8999"    # FE: Dashboard maps to same Eureka server
```

Nginx proxies `discovery.panomete.com` → `flowero-discover:3999`, which Docker maps to internal `:8999`. No second embedded server, no Spring Boot management port trick, no redirect proxy.

---

## Gradle + GraalVM Java 25 on Windows

When `JAVA_HOME` is set to a GraalVM path using MSYS-style paths (e.g., `export JAVA_HOME="/c/Program Files/graalvm-25"`), Gradle may warn:

```
Directory 'C:\c\Program Files\graalvm-25' used for java installations does not exist
```

**Impact:** Cosmetic only. Gradle's Java toolchain auto-detection finds JDK 25 from the toolchain specification in `build.gradle`:

```groovy
java {
    toolchain {
        languageVersion = JavaLanguageVersion.of(25)
    }
}
```

The build succeeds despite the `JAVA_HOME` warning. To suppress it, set `JAVA_HOME` using the Windows path format: `C:\Program Files\graalvm-25`.

---

## Eureka Shutdown Noise

On context close, Eureka always logs:

```
Unregistering application FLOWERO-DISCOVER with eureka with status DOWN
```

This happens even in standalone mode (`register-with-eureka: false`). The `EurekaServiceRegistry` lifecycle bean calls `unregister()` on shutdown as a safety measure — it's a no-op when the `DiscoveryClient` never registered. Harmless.

The Jersey 3 connection cleaner also throws a shutdown `IllegalStateException`:

```
ERROR c.n.d.s.t.j.EurekaJersey3ClientImpl : Cannot clean connections
java.lang.IllegalStateException: Client instance has been closed.
```

This is a race between the connection cleaner thread and the graceful shutdown. Known cosmetic issue in `eureka-client-jersey3-2.0.6`. No fix needed — tests pass and the server shuts down cleanly.

---

## Spring Cloud BOM Version Management

The Spring Cloud BOM (`spring-cloud-dependencies:2025.1.2`) manages all transitive versions. The build only declares top-level starters:

```groovy
dependencies {
    implementation 'org.springframework.cloud:spring-cloud-starter-netflix-eureka-server'
    implementation 'org.springframework.boot:spring-boot-starter-actuator'
}
```

**Rule:** Never pin individual Netflix Eureka, Jersey, or Jackson versions. The BOM aligns them. Pinning sub-dependencies breaks compatibility.
