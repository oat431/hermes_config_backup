# Release Checklist Audit Pattern

## Representative audit context

The first use of this skill reviewed a 170-line, 59-checkbox Markdown release/deployment checklist with ten lifecycle sections, a quick sanity check, a project-tier matrix, Mermaid tier routing, and links to API, frontend, microservice, and security checklists.

The target document was intentionally not edited: the user requested an audit only. A good audit report therefore stated the verdict, cited exact line ranges, separated high-priority production blockers from lower-priority improvements, and ended by explicitly stating that no changes were made.

## High-value findings to check first

1. **Traceable release identity** — version and Git tag are not enough. Look for source commit SHA, CI/build ID, immutable artifact/image digest, target environment, rollback artifact, and release/deployment record.
2. **Build once, promote the same artifact** — staging must exercise the exact artifact digest promoted to production; production should not rebuild.
3. **Supply-chain evidence** — SBOM, signature, provenance/attestation, and verification must refer to the exact artifact digest.
4. **Migration reversibility** — a down migration is not automatically safe. Check compatibility with old/new application versions and whether recovery is rollback, forward fix, restore, or another path.
5. **Rollout semantics** — separate deployment topology (rolling, blue-green, canary, recreate) from release exposure (feature flag, cohort, percentage, dark launch).
6. **SLO-based rollback** — "SLO violated" or "error budget exhausted" is too vague. Require concrete error, latency, burn-rate, business-impact, and sustained-duration criteria.
7. **Probe semantics** — startup, readiness, and liveness are different. Dependency failure often belongs in readiness, not liveness.
8. **Tier safety** — internal status, user count, and POC labels do not override high data sensitivity, public exposure, criticality, regulatory obligations, or production connectivity.
9. **Workload neutrality** — a framework-agnostic checklist should not make Kubernetes or HTTP assumptions normative when it claims to cover batch, mobile, static, or worker workloads.
10. **Evidence capture** — a checkbox without an evidence link is weak as a release gate. Prefer CI runs, scan reports, migration records, deployment IDs, dashboards, approvals, and final sign-off.

## Useful correction patterns

### Release record

```markdown
## Release Record

- Service/system:
- Change or release ID:
- Version:
- Source commit SHA:
- CI build/workflow ID:
- Artifact/image digest:
- Target environment:
- Selected tier and risk overlays:
- Rollout/exposure strategy:
- Release owner / deployer / approver:
- Rollback artifact:
- Dashboard / runbook / change record:
- Observation-window result:
- Final sign-off:
```

### Annotated tag

Prefer a deliberate, tag-specific operation over `git push --tags`:

```bash
git tag -a v1.4.0 -m "Release v1.4.0" <commit>
git push origin v1.4.0
```

### Promotion gate

```markdown
- [ ] Artifact built once by CI.
- [ ] Exact artifact digest tested in staging.
- [ ] Same digest promoted to production without rebuilding.
- [ ] Signature, provenance, and SBOM verified for that digest.
```

### Migration decision

```markdown
- [ ] Previous and new application versions are compatible with the schema during rollout.
- [ ] Lock duration, backfill plan, validation, and replication impact reviewed.
- [ ] Recovery path selected for this migration: rollback / forward fix / restore / other.
- [ ] Recovery path tested in staging or an equivalent environment.
```

### Rollback criteria

```markdown
- [ ] Abort/pause/rollback thresholds defined before deploy.
- [ ] Error rate threshold and sustained duration:
- [ ] Latency threshold and sustained duration:
- [ ] SLO burn-rate or budget-consumption threshold:
- [ ] Business-impact threshold:
- [ ] Automated or manual action for each threshold:
```

### Tier exception

```markdown
- [ ] N/A — reason:
- [ ] Exception approved by:
- [ ] Review/expiry date:
```

## Audit report shape

Use this order for a readable report:

1. File and scope.
2. Executive verdict.
3. High-priority findings table.
4. Technical corrections.
5. Tiering and exception review.
6. Missing controls.
7. Lower-priority consistency findings.
8. Recommended disposition.
9. Explicit modified/not-modified statement.

## Reference anchors

- Semantic Versioning 2.0.0: https://semver.org/
- SLSA provenance: https://slsa.dev/spec/v1.1/provenance
- DORA delivery metrics: https://dora.dev/guides/dora-metrics/
- Kubernetes probe semantics: https://kubernetes.io/docs/concepts/workloads/pods/probes/

These links are research anchors for future audits; re-check current versions when making normative claims.