# Data and ML Engineer: Areas 05-07 Build Manifest

Session: 2026-08-06. Built 21 files across 3 capability areas under `career-path/09_Data_and_ML_Engineer/`.

## Area 05: Data Security and Privacy (7 files)

capability_area: `data-security-and-privacy`
source_frameworks: DMBoK v2, CyBOK v1

| File | Topic | Key frameworks |
|------|-------|---------------|
| 00_overview.md | Capability area overview | Decision flow, anti-patterns, maturity signals |
| 01_Data_Classification_and_Sensitivity.md | PII, PHI, financial data tiers | Sensitivity tier model, classification matrix, automated discovery signals |
| 02_Encryption_and_Tokenization.md | At-rest, in-transit, column-level, tokenization | Scope decision matrix, encryption vs tokenization comparison, key lifecycle |
| 03_Access_Control_for_Data.md | RLS, column masking, RBAC/ABAC | Access control models, RLS design, granularity escalation |
| 04_Privacy_Engineering.md | GDPR/CCPA, data minimization, consent | Regulation-to-engineering mapping, minimization matrix, consent architecture |
| 05_Audit_and_Lineage_for_Compliance.md | Audit logs, lineage, compliance reporting | Audit dimensions, lineage types, reporting matrix |
| 06_Secure_Data_Sharing.md | Anonymization, differential privacy, DSAs | Sharing approaches, anonymization techniques, DSA checklist |

## Area 06: ML Lifecycle and MLOps (7 files)

capability_area: `ml-lifecycle-and-mlops`
source_frameworks: SWEBOK, CyBOK

| File | Topic | Key frameworks |
|------|-------|---------------|
| 00_overview.md | Capability area overview | Lifecycle flowchart, anti-patterns, maturity signals |
| 01_Experiment_Tracking_and_Reproducibility.md | MLflow, W&B, artifact management | Tracking categories, tool comparison, reproducibility levels |
| 02_Feature_Engineering_and_Feature_Store.md | Online/offline stores, feature sharing | Store architecture, skew sources, sharing dimensions |
| 03_Model_Training_and_Evaluation.md | Metrics, cross-validation, hyperparameters | Metric-by-objective, validation strategy, tuning approaches |
| 04_Model_Serving_and_Inference.md | Batch/real-time, A/B testing, canary | Serving patterns, deployment strategies, serialization |
| 05_ML_Monitoring_and_Drift.md | Data drift, concept drift, alerting | Drift types, detection methods, alerting strategy |
| 06_Model_Governance_and_Cards.md | Model cards, fairness, approval workflows | Card sections, fairness metrics, approval stages |

## Area 07: Production Engineering (7 files)

capability_area: `production-engineering`
source_frameworks: SWEBOK

| File | Topic | Key frameworks |
|------|-------|---------------|
| 00_overview.md | Capability area overview | Decision flowchart, anti-patterns, maturity signals |
| 01_Distributed_Systems_for_Data.md | CAP, partitioning, consensus | CAP application, partitioning strategies, consistency models |
| 02_Scaling_and_Performance_Tuning.md | Query optimization, caching, resources | Bottleneck identification, query techniques, caching strategies |
| 03_Reliability_and_Fault_Tolerance.md | Idempotency, exactly-once, DLQ | Idempotency patterns, processing guarantees, failure handling |
| 04_Cost_Optimization_for_Data_Systems.md | Compute-storage separation, FinOps | Cost drivers, storage tiering, compute optimization |
| 05_CI_CD_for_Data_and_ML.md | Pipeline testing, data validation in CI | CI stages, validation checks, promotion workflow |
| 06_Operational_Runbooks_and_On_Call.md | Incident response, escalation | Runbook structure, severity levels, sustainability metrics |

## Vault anchor links used

- `[[DMBoK v2 - Overview]]`
- `[[05_Data_Security]]` (DMBOK)
- `[[CyBOK v1 - Overview]]`
- `[[SWEBOK v4 - Overview]]`
- `[[computing-foundation-note/Artificial_Intelligence/AI Overview]]`
- `[[software-engineering-note/06_Software_Engineering_Operations/Software Engineering Operations Overview]]`

## Build pattern

Initial generation via `execute_code` with full content strings per file, then two expansion passes:
1. Add "Common Pitfalls" section (4-5 bullets) before Key Takeaways on topic notes
2. Add "Common Anti-Patterns" table + "Maturity Signals" list on overview files

All 21 files verified: 100-107 lines, 0 em-dashes, flowchart syntax, no parentheses in Mermaid labels.
