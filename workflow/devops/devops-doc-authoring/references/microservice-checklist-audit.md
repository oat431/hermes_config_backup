# Microservice Checklist Suite Audit Reference

Use this reference when auditing the root notes of a microservice checklist folder while excluding implementation-specific overlays such as `spring-boot/`.

## Scope and inventory

- Inventory root notes and explicitly list excluded subfolders.
- Record file counts, line counts, and checklist-item counts.
- Read every in-scope note before judging the suite.
- Inspect both `[[wikilinks]]` and relative Markdown links against actual vault paths.
- Broken links are control defects: a hidden or unreachable detailed note weakens the gate.

## Canonical ownership

Prefer this division:

| Note | Canonical responsibility |
|---|---|
| `microservice-infrastructure.md` | System-level architecture and cross-cutting decisions |
| `api-gateway.md` | Gateway routing, policy, traffic, and operations |
| `authentication.md` | Identity provider, OAuth/OIDC, tokens, keys, sessions, authorization |
| `load-balancing.md` | Edge/internal traffic distribution, health, draining, failover |
| `data-messaging.md` | Data ownership, events, brokers, delivery, sagas, outbox |
| `observability.md` | Logs, metrics, traces, SLOs, alerts, telemetry operations |
| `resilience.md` | Timeouts, deadlines, retries, breakers, bulkheads, fallbacks, failure tests |
| `Microservice Launch.md` | Release gate that references applicable domain gates |

The system-level note should either be concise and link to these detailed notes or be explicitly declared the canonical full checklist. Do not let the same rule drift across multiple owners.

## Cross-note consistency matrix

Always reconcile these items:

- Gateway authentication versus service-level token validation and object/function authorization.
- JWKS discovery through issuer metadata and `jwks_uri`; do not hardcode competing endpoint paths.
- Startup, liveness, and readiness semantics.
- Retry ownership, total deadlines, cancellation, and retry amplification.
- Circuit-breaker applicability versus a blanket “every call” rule.
- Safe fallbacks for reads versus fail-closed behavior for security, payment, inventory, and compliance operations.
- At-least-once, effectively-once, and exactly-once claims, including external side effects.
- Broker HA, authentication, encryption, retention, DLQ/replay, lag, backup, and restore.
- Trace context propagation versus request IDs; use W3C `traceparent` where interoperability is required.
- Metric labels and cardinality; never put unbounded user IDs, trace IDs, raw URLs, or tenant IDs into metrics.
- Internal plaintext versus encrypted service traffic and the documented trust boundary.
- Platform-neutral requirements versus Docker Compose, Kubernetes, VM, service mesh, or managed-cloud overlays.

## Evidence and exception model

A binary checkbox is not enough for a full-scale gate. Add or record:

```markdown
- Status: Pass / Fail / N/A / Exception
- Selected option:
- Rationale:
- Evidence:
- Owner:
- Reviewed by:
- Review date:
- Exception reason:
- Exception approver:
- Exception expiry/review date:
```

Examples such as `3s` connect timeout, `30s` read timeout, `≥2` registry nodes, `5%` canary traffic, `99.9%` availability, `200ms` latency, `1 CPU`, or `512Mi` memory are starting points, not universal policies. Require measurement, an SLO, or an architecture decision.

## Security checks

- Use issuer metadata and the authoritative `jwks_uri` for OIDC key discovery.
- Require explicit JWT algorithm allowlists, issuer/audience validation, key rotation, clock-skew policy, and replay/revocation behavior.
- Prefer PKCE for user-facing authorization-code flows and exclude implicit/password grants unless an explicit approved exception exists.
- Use current password policy rather than an obsolete fixed minimum; if aligning to NIST SP 800-63B single-factor guidance, the minimum is 15 characters.
- Strip or overwrite untrusted forwarding and identity headers at trusted proxy boundaries.
- Require service-level authorization for owned resources even when the gateway performs coarse policy checks.

## Messaging and data checks

- Treat at-least-once delivery plus idempotent consumers as the normal baseline.
- Claim exactly-once only for a precisely bounded processing transaction; Kafka consume-process-produce transactions do not automatically make external side effects exactly-once.
- Require event IDs, deduplication, replay policy, schema compatibility, poison-message handling, DLQ controls, lag monitoring, and retention.
- For sagas, require timeouts, retries, idempotent compensations, stuck-saga detection, manual reconciliation, and operator visibility; sagas do not provide normal ACID isolation.
- For transactional outbox, verify relay retry, crash recovery, deduplication, outbox growth, replay, and retention.
- Treat domain events as immutable after publication, but define storage retention, compaction, redaction, and legal deletion separately.

## Observability checks

- Require correlation context where available; background/startup work may need an execution or operation ID rather than a trace ID.
- Control metric cardinality with route templates and bounded labels; use logs/traces for high-cardinality dimensions.
- Define telemetry retention, access control, PII/secrets redaction, sampling, collector availability, dropped telemetry, and cost budgets.
- Every page should have an owner, severity, escalation path, runbook, and test method.
- Test telemetry failure as well as application failure.

## Resilience checks

- Define a dependency failure matrix.
- Set one retry owner per dependency path; bound attempts and total deadline, propagate cancellation, and test multi-layer retry amplification.
- Select timeout-only, breaker, bulkhead, queue buffering, or another policy per remote dependency.
- Define fallback behavior per operation: fail closed, fail open, stale read, partial response, queue for later, or no fallback.
- Never fabricate successful business state through a fallback.
- Measure blast radius, recovery time, data loss, and manual reconciliation for representative failures.

## Platform overlays

Do not make Kubernetes mandatory in a framework-agnostic checklist. Use outcome-based controls and link conditional overlays:

- Docker Compose / single-host deployment
- Kubernetes / orchestrator deployment
- VM/systemd deployment
- Managed cloud deployment
- Service mesh deployment

For each platform, cover health, rollout, drain, capacity, config/secrets, rollback, observability, backup, and recovery using the platform’s actual mechanisms.

## Research anchors

- OAuth 2.0 Security Best Current Practice: `https://datatracker.ietf.org/doc/rfc9700/`
- JWT Best Current Practices: `https://datatracker.ietf.org/doc/html/rfc8725`
- OpenID Connect Discovery: `https://openid.net/specs/openid-connect-discovery-1_0.html`
- NIST Digital Identity Guidelines: `https://pages.nist.gov/800-63-4/sp800-63b/authenticators/`
- RabbitMQ quorum queues: `https://www.rabbitmq.com/docs/quorum-queues`
- Apache Kafka design and delivery semantics: `https://kafka.apache.org/43/design/design/`
- W3C Trace Context: `https://www.w3.org/TR/trace-context/`
- Kubernetes probes: `https://kubernetes.io/docs/concepts/workloads/pods/probes/`
- RFC 9110 HTTP semantics: `https://www.rfc-editor.org/info/rfc9110/`
- OpenTelemetry context propagation: `https://opentelemetry.io/docs/concepts/context-propagation/`
- Prometheus instrumentation/cardinality guidance: `https://prometheus.io/docs/practices/instrumentation/`
- OWASP Microservices Security Cheat Sheet: `https://cheatsheetseries.owasp.org/cheatsheets/Microservices_Security_Cheat_Sheet.html`
- AWS transactional outbox: `https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/transactional-outbox.html`
- AWS saga orchestration: `https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/saga-orchestration.html`
