# Common Compliance Gaps in Software Document Templates

> Identified during the first audit of the user's 357-template library (July 2026). These patterns are likely to recur in any BOK-derived template library.

---

## Gap 1: Missing Acceptance Criteria in SRS

**Standard:** ISO/IEC/IEEE 29148:2018
**Template:** SRS (Software Requirements Specification)
**Issue:** 29148 requires well-formed requirements with acceptance criteria per requirement. Templates often list acceptance criteria as a field in the attributes table but don't provide explicit guidance on writing testable acceptance criteria (Given/When/Then format).
**Fix:** Add an "Acceptance Criteria Format" subsection under Functional Requirements with Given/When/Then examples.

---

## Gap 2: Missing CCB in SCMP

**Standard:** IEEE 828-2012
**Template:** SCMP (Software Configuration Management Plan)
**Issue:** IEEE 828 requires a Configuration Control Board (CCB) with defined membership, charter, and decision authority. Templates often have a change control flowchart but no CCB.
**Fix:** Add a "Configuration Control Board" section defining: membership, meeting frequency, decision authority levels, escalation path.

---

## Gap 3: Missing Release Management in SCMP

**Standard:** IEEE 828-2012
**Template:** SCMP
**Issue:** Release Management and Delivery is one of the 5 required CM processes but is often missing.
**Fix:** Add "Release Management and Delivery" section covering: release packaging, version tagging, delivery handoff, release notes generation.

---

## Gap 4: Missing Suspension/Resumption in Test Plan

**Standard:** ISO/IEC/IEEE 29119-3
**Template:** Test Plan
**Issue:** 29119-3 requires explicit suspension criteria (when to halt testing) and resumption requirements (what must be true to resume). Often missing entirely.
**Fix:** Add "Suspension and Resumption Criteria" section. Example: "If >5 critical defects found in 1 hour, suspend testing. Resume only after critical defects are resolved and regression suite passes."

---

## Gap 5: Missing Integrity Levels in V&V Plan

**Standard:** IEEE 1012-2017
**Template:** V&V Plan
**Issue:** IEEE 1012 requires identifying the Software/System Integrity Level (1-4), which determines which V&V tasks are mandatory. Without this, appropriate rigor cannot be demonstrated.
**Fix:** Add "Software/System Integrity Level" section at the top. Define level (1-4) with rationale. Map required V&V tasks to the integrity level.

---

## Gap 6: Missing SQA Independence in SQAP

**Standard:** IEEE 730-2014
**Template:** SQAP
**Issue:** IEEE 730 requires that SQA be organizationally independent from development. Templates rarely address this.
**Fix:** Add "SQA Independence" statement specifying: who QA reports to, organizational separation from development, escalation authority for non-compliance.

---

## Gap 7: Incorrect Standard Designation (20000-1)

**Issue:** Templates cite `ISO/IEC/IEEE 20000-1` but IEEE was never a co-author. The correct designation is `ISO/IEC 20000-1`.
**Fix:** Global find-and-replace `ISO/IEC/IEEE 20000-1` → `ISO/IEC 20000-1`.

---

## Gap 8: Outdated ISO 27001 Version

**Issue:** Templates reference ISO/IEC 27001 without specifying version, or may reference the 2013 structure (14 domains, 114 controls). The 2022 revision restructured Annex A to 4 themes with 93 controls.
**Fix:** Add `:2022` to all ISO 27001 references. Verify control mappings against the 4-theme structure: Organizational (37), People (8), Physical (14), Technological (34).

---

## Gap 9: 42010 "Compliance" with 4+1 Views

**Standard:** ISO/IEC/IEEE 42010:2022
**Template:** SAD (Software Architecture Document)
**Issue:** 42010 does NOT mandate the 4+1 View Model. It requires stakeholder→concern→viewpoint→view mapping. Templates that use 4+1 without explicit stakeholder/concern mapping are not formally compliant.
**Fix:** This is a design decision, not necessarily a defect. For formal 42010 compliance: add "Stakeholders and Concerns" section, rename views as explicit viewpoints, add "View Correspondences" section.

---

## Bonus: Superseded Standards to Watch For

| Old Standard | Current Standard | Notes |
|---|---|---|
| IEEE 830-1998 | ISO/IEC/IEEE 29148:2018 | SRS standard |
| IEEE 829-2008 | ISO/IEC/IEEE 29119-3:2013 | Test documentation |
| ISO 31000:2009 | ISO 31000:2018 | Risk management |
| ISO/IEC 27001:2013 | ISO/IEC 27001:2022 | ISMS (Annex A restructured) |
| ISO/IEC 25010:2011 | ISO/IEC 25010:2023 | SQuaRE quality model |
| ISO/IEC/IEEE 15288:2015 | ISO/IEC/IEEE 15288:2023 | System lifecycle processes |
| ISO/IEC 15504 | ISO/IEC 33000 series | Process assessment (SPICE) |
| IEEE 1012-2012 | IEEE 1012-2017 | V&V |
