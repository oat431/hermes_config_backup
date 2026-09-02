# SWEBOK and Related-BOK Artifact Audit Reference

## Source interpretation

SWEBOK, SEBoK, BABOK, PMBOK, CyBOK, and DMBoK are knowledge maps and practice frameworks. They describe processes, activities, inputs, outputs, techniques, and context—not one universal standalone-file set. An “essential document” checklist is therefore a tailored work-product model and must state its assumptions.

SWEBOK v4 has 18 knowledge areas. A practical software-project catalog usually draws most directly from Requirements, Architecture, Design, Construction, Testing, Operations, Maintenance, Configuration Management, Engineering Management, Process, Quality, Security, Professional Practice, and Economics; Computing, Mathematical, and Engineering Foundations are usually enabling knowledge rather than project deliverables.

SEBoK adds system-level concept definition, stakeholder needs, ConOps, system requirements, system architecture, interfaces, integration, verification, validation, transition, operations, maintenance, disposal, technical management, safety, and standards compliance. Use it to detect a software-only checklist that silently omits system context or retirement.

## Artifact relationship map

| Canonical concern | Common aliases or variants | Audit question |
|---|---|---|
| Need, value, and scope | Business Case, Business Objectives, BRD, Product Vision, Solution Scope | Which artifact is authoritative for the project’s why, boundaries, and outcomes? |
| Requirements governance | SRS, user stories, acceptance criteria, requirements baseline, RTM, change log | Are requirements prioritized, baselined, changed, and traced, even when the tool is the backlog? |
| Architecture decisions | SAD, Architecture Views, ADR, Design Rationale, HLD | Is there one decision history with scope and alternatives, rather than competing ADR/design records? |
| Risk and security | Risk Register, Threat Model, Security Risk Assessment, Risk Treatment Plan | Are project, product, operational, and security risks distinguished or intentionally integrated? |
| Quality and verification | Test Plan, V&V Plan, Review Records, Test Reports, Quality Reports | Are verification, validation, reviews, and testing separate concerns with clear evidence? |
| Configuration and release | SCMP, Baseline Records, Change Requests, VDD, Release Notes, SBOM | Is the release reproducible and traceable to approved configuration items? |
| Operations and support | Deployment Plan, Runbook, SLA/SLO/SLI, Incident Record, Postmortem, Maintenance Log | Does the catalog cover operation, recovery, problem management, maintenance, and retirement? |
| Data governance | Data Dictionary, Data Model, Data Lineage, Data Quality Rules, Retention Policy | Is data scope conditional on the system’s actual data responsibilities? |

Use aliases and parent/subset relationships instead of declaring every repeated label a duplicate.

## Priority calibration

A useful audit table has independent columns for:

1. **Practice:** what must be done;
2. **Artifact form:** separate document, tool-managed record, code/configuration, dashboard, generated report, or combined plan;
3. **Applicability:** universal, common, conditional, domain-specific, or not applicable;
4. **Evidence:** what proves the practice happened.

This avoids marking APIs, database schemas, SLAs, DR plans, formal V&V, SBOMs, FMEA/FTA, FCA/PCA, or safety cases as universal simply because they are important in projects where they apply.

## Common attribution traps

- ISO/IEC/IEEE 12207 and 15288 define life-cycle processes; they do not automatically mandate every named project document.
- ISO/IEC/IEEE 42010 governs architecture descriptions; it is not by itself an ADR-template standard.
- ISO/IEC 25010 defines a quality model; it does not prescribe a “solution performance report.”
- ISO/IEC 27001 governs an ISMS and control framework; it is not a direct standard for every SAST, DAST, or security-architecture report.
- ISO/IEC 5230 concerns open-source compliance; it should not be presented as the sole SBOM standard.
- ISO/IEC 40500:2012 corresponds to WCAG 2.0; cite W3C WCAG 2.1/2.2 explicitly when those versions are intended.
- NIST, GDPR, OWASP, MITRE ATT&CK, FIPS, OpenAPI, SPDX, CVE/CWE/CVSS, and vendor/framework guidance should be typed separately from ISO/IEEE standards.

Record edition, status, official URL, and last verification date for any citation whose currency matters.

## Minimum audit outputs

A reproducible report should include:

- target and source roots;
- counts by file, phase/domain, and priority;
- missing categories and whether they are truly absent or only aliased;
- priority overreach and under-classification;
- canonical artifact/alias relationships;
- link and literal-path status;
- source/standards corrections;
- profile applicability and Quick-Start parity;
- explicit confirmation that no files were edited when the audit is read-only.

## Session-derived SWEBOK evidence anchors

For SWEBOK v4 catalog audits, also check:

- Requirements baselines, backlog/release allocation, issue/TBD logs, CCB charters, and business-rules/data-dictionary artifacts: `software-engineering-note/01_Software_Requirements/05_Documenting_Requirements.md:21-25,60-99`; `.../06_Requirements_Modeling.md:263-306`; `.../10_Requirements_Management.md:53-60,226-239,295-307,400-412`.
- Vision/scope, feasibility, scope baselines, project deliverables, acquisition documents, and measurement outputs: `software-engineering-note/01_Software_Requirements/02_Business_and_User_Requirements.md:82-92,145-161`; `software-engineering-note/09_Software_Engineering_Management/06_Project_Initiation_and_Scope.md:36-55,111-163,244-258`; `.../07_Estimation_and_Planning.md:67-90`; `.../09_Software_Acquisition_Management.md:77-83,121-130,243-253`.
- User/install/training/support documents, incident/postmortems, service reports, recovery rehearsals, and retirement: `body-of-knowledge/SWEBOK/06_Software_Engineering_Operations.md:13-18,27-36`; `software-engineering-note/06_Software_Engineering_Operations/08_Service_Operations_and_Support.md:49-59,152-214,224-285`; `software-engineering-note/06_Software_Engineering_Operations/07_Capacity_and_Disaster_Recovery.md:115-129,353-365`; `body-of-knowledge/SWEBOK/10_Software_Engineering_Process.md:87-102`; `body-of-knowledge/SWEBOK/14_Software_Engineering_Professional_Practice.md:21,34`.
- Test policy/strategy, test completion summary, artifact archiving, quality gates, CAPA, and assurance evidence: `software-engineering-note/05_Software_Testing/12_Test_Process_and_Measures.md:20-52,109-142,191-202,243-251`; `software-engineering-note/09_Software_Engineering_Management/10_Quality_Planning_and_Process_Monitoring.md:17-90`; `body-of-knowledge/SWEBOK/12_Software_Quality.md:26-34,38-45`.
- Configuration status accounting and audit evidence: `body-of-knowledge/SWEBOK/08_Software_Configuration_Management.md:13-19,23-37`; `software-engineering-note/08_Software_Configuration_Management/07_SCSA_and_Status_Accounting.md:157-167`; `.../08_Configuration_Auditing.md:95-121`.

When citing standards, separate scope from artifact type: 42010 supports architecture descriptions rather than ADR file formats; 5230 is OpenChain license compliance rather than an SBOM standard; 27001 is ISMS governance rather than a direct SAST/DAST/reporting standard; 29119-3 supports test documentation; and 29148 should be cited with edition/status.

