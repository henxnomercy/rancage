# RPR-R0 Owner Decision Record

**Document:** RPR-R0 Owner Decision Record  
**Version:** 1.0  
**Date:** 2026-11-17  
**Status:** OFFICIAL RECORD — RATIFIED BY OWNER  
**Baseline:** RANCAGE 0.2.0a1 (`03c6ec15b31eeddf8210223c32ca98793abe4222`)  
**Governing Charter:** RPR-R0 Charter Proposal v0.8 (`RPR-R0-CHARTER-PROPOSAL-v0.8.md`)  
**Authorized External Archive:** `F:\Project\RANCAGE-research-evidence\RPR-R0\`  

---

## 1. Executive Summary & Governing Authority

This document constitutes the formal, ratified Owner Decision Record for the RPR-R0 Performance Research Foundation milestone.

The repository Owner has formally reviewed [`RPR-R0-CHARTER-PROPOSAL-v0.8.md`](../charters/RPR-R0-CHARTER-PROPOSAL-v0.8.md), following independent audit approval by the RANCAGE Auditor (`APPROVED FOR OWNER REVIEW`), and has executed the seven formal decision gates specified in Section 10 (Owner Decision Register, ODR-01 through ODR-07).

**Core Governance Invariants:**
1. **Stage 0 Baseline Freeze:** The Stage 0 codebase at commit `03c6ec15b31eeddf8210223c32ca98793abe4222` and release tag `v0.2.0a1` remains CLOSED / FROZEN. Zero code modifications, VM optimizations, compiler alterations, or repository commits are authorized.
2. **Non-Implicit Authorization:** Approval of specific preliminary research activities creates zero implicit permission for subsequent phases. Every permission boundary remains strictly enforced.
3. **Evidence Precedes Claims:** **RANCAGE must prove performance improvements rather than merely claim them.** Historical benchmark figures published on `benjdd.com/languages2/` remain unverified external claims until resolved by empirical evidence.
4. **Milestone Isolation:** RPR-R0 completion does not authorize R1 (Local Reference Baseline) or Stage 1 (Language Evolution).

---

## 2. Ratified Decision Register (ODR-01 through ODR-07)

| Decision Gate | Subject Matter | Operative Clause | Owner Decision | Summary of Operative Scope |
|---|---|---|---|---|
| **ODR-01** | Evidence Collection Authorization | Charter §10, §14 | **APPROVED** | Authorizes Evidence Collector to execute ACT-01 through ACT-04 strictly within defined boundaries. |
| **ODR-02** | External Archive Location | Charter §10, §14 | **APPROVED** | Formally adopts `F:\Project\RANCAGE-research-evidence\RPR-R0\` as the immutable external storage root. |
| **ODR-03** | Contingency Adoption of Pathway A2 | Charter §7, §8, §10 | **APPROVED** | Authorizes Route A1 as primary target and Route A2 as official contingency fallback upon verified search exhaustion. |
| **ODR-04** | Benchmark Warning Remediation | Charter §10, §16, §17 | **APPROVED** | Mandates disclaimer banners on all references to `benjdd.com/languages2/` metrics; unverified numbers barred from baseline targets. |
| **ODR-05** | Mandatory Workload-Shape Characterization | Charter §6, §10, §13 | **APPROVED** | Mandates algorithmic workload characterization (input `40` binding, recursion vs loop bounds) prior to any compiler assessment. |
| **ODR-06** | Statistical Pilot Milestone Separation | Charter §9, §10 | **APPROVED** | Formally isolates statistical pilot to a separate future milestone; statistical pilot execution is **NOT AUTHORIZED**. |
| **ODR-07** | Separate Compile-Only Authorization | Charter §10, §14, §15 | **DEFERRED** | Third-party compiler invocation (ACT-10) is **NOT AUTHORIZED**; compiler execution remains strictly prohibited. |

---

## 3. Detailed Decision Specifications & Consequences

### ODR-01: Evidence Collection Authorization
- **Question:** Shall the Evidence Collector be authorized to execute ACT-01 through ACT-04 to gather external benchmark sources?
- **Owner Decision:** **APPROVED.**
- **Operative Boundaries:**
  - Authorizes web fetching and static snapshotting of publication URLs (ACT-01).
  - Authorizes cloning of external benchmark git repositories into the designated external archive (ACT-02).
  - Authorizes computation of `MANIFEST.sha256` by Evidence Collector with independent QA verification (ACT-03).
  - Authorizes file writing strictly within the external evidence archive (ACT-04).
- **Prohibitions:** Does NOT authorize execution of third-party compiler drivers (ACT-06), execution of foreign binaries (ACT-07), modification of the RANCAGE codebase (ACT-08), benchmark timing measurements (ACT-09), or third-party compile-only syntax checks (ACT-10).

### ODR-02: External Archive Location & Storage Format
- **Question:** Shall the proposed external archive directory `F:\Project\RANCAGE-research-evidence\RPR-R0\` be adopted as the official storage location?
- **Owner Decision:** **APPROVED.**
- **Operative Boundaries:**
  - Designates `F:\Project\RANCAGE-research-evidence\RPR-R0\` as the sole authorized evidence root.
  - Zero evidence files, git clones, raw snapshots, or manifests may be stored inside `F:\Project\RANCAGE\`.
  - Directory structure must follow the layout defined in [`RPR-R0-EVIDENCE-COLLECTION-PLAN.md`](../evidence/RPR-R0-EVIDENCE-COLLECTION-PLAN.md).

### ODR-03: Contingency Adoption of Pathway A2
- **Question:** In the event that historical source commits are unrecoverable after exhaustive search, shall Route A2 (Historical Reference Only) be authorized as an approved fallback?
- **Owner Decision:** **APPROVED (A1 Primary + A2 Contingency).**
- **Operative Boundaries:**
  - The primary objective remains Route A1 (Historical Source Pinned for C, Rust, Zig).
  - If exhaustive search across all 14 mandatory categories (§8.1) fails to recover exact historical commits, the project is authorized to decouple from unpinned historical numbers.
  - Route A2 invocation requires independent Auditor assessment confirming search log completeness and explicit Owner acceptance.
  - Route A2 cannot be selected automatically due to tool limitations or network timeouts.

### ODR-04: Benchmark Warning Remediation
- **Question:** Shall explicit warning banners be mandated on all documentation referencing `benjdd.com/languages2/` metrics indicating they are unverified external figures?
- **Owner Decision:** **APPROVED.**
- **Operative Boundaries:**
  - All RANCAGE documentation, proposals, and roadmaps referencing historical figures must display prominent disclaimer banners.
  - Historical numbers must never be quoted as RANCAGE performance targets or competitive baselines until cryptographically verified under Route A1.

### ODR-05: Mandatory Workload-Shape Characterization
- **Question:** Shall workload algorithmic characterization (loop structure, memory access, input `40` binding) be required before any build reproduction?
- **Owner Decision:** **APPROVED.**
- **Operative Boundaries:**
  - Workload semantics must be analytically modeled and confirmed before any build or optimization assessment.
  - Establishes mathematical invariants for Fibonacci, binary trees, matrix operations, or whatever workloads are identified.
  - Guards against benchmarking syntactically identical but algorithmically mismatched implementations.

### ODR-06: Statistical Pilot Milestone Separation
- **Question:** Shall statistical pilot execution be formally isolated as a separate future milestone requiring its own charter and authorization?
- **Owner Decision:** **APPROVED.**
- **Operative Boundaries:**
  - The statistical methodology specified in Charter §9 (log-ratio scale, paired bootstrap 10,000 resamples, seed `20261117`) remains **PROPOSED / NOT VALIDATED**.
  - Zero benchmark timing runs, zero warmup cycles, and zero microbenchmark executions are permitted under RPR-R0.
  - A statistical pilot requires an independent proposal, auditor review, and separate explicit Owner authorization.

### ODR-07: Separate Compile-Only Toolchain Authorization
- **Question:** Shall the Evidence Collector be granted conditional permission (ACT-10) to run third-party compilers solely for syntax and AST validation without binary execution?
- **Owner Decision:** **DEFERRED.**
- **Operative Boundaries:**
  - Permission ACT-10 is **NOT AUTHORIZED**.
  - The Evidence Collector and all other roles are strictly prohibited from executing third-party compiler drivers (`gcc`, `clang`, `rustc`, `zig`) on host systems during RPR-R0.
  - Source verification in RPR-R0 remains visual, textual, and analytical.
  - If syntax validation becomes necessary, a separate formal request with pinned compiler versions and explicit command lines must be submitted to the Owner.

---

## 4. Operative Permissions Matrix (ACT-01 through ACT-10)

Following the ratification of ODR-01 through ODR-07, the operational activities defined in Charter Section 14 stand as follows:

| Activity ID | Operational Activity Description | Baseline Charter Status | Ratified Status | Authorized Role | Prerequisite Gate Satisfied |
|---|---|---|---|---|---|
| **ACT-01** | Web snapshot & public URL fetch | REQUIRES OWNER APPROVAL | **AUTHORIZED** | Evidence Collector | ODR-01, ODR-02 APPROVED |
| **ACT-02** | Git clone of external benchmark repos | REQUIRES OWNER APPROVAL | **AUTHORIZED** | Evidence Collector | ODR-01, ODR-02 APPROVED |
| **ACT-03** | SHA-256 manifest computation | REQUIRES OWNER APPROVAL | **AUTHORIZED** | Evidence Collector / QA | ODR-01, ODR-02 APPROVED |
| **ACT-04** | File writing to external evidence archive | REQUIRES OWNER APPROVAL | **AUTHORIZED** | Evidence Collector | ODR-01, ODR-02 APPROVED |
| **ACT-05** | Read-only inspection of RANCAGE source | ALLOWED | **ALLOWED** | All Roles | General architectural analysis |
| **ACT-06** | Execution of third-party compilers | PROHIBITED | **PROHIBITED** | None | Strictly barred under R0 |
| **ACT-07** | Execution of compiled third-party binaries | PROHIBITED | **PROHIBITED** | None | Strictly barred under R0 |
| **ACT-08** | Modification of RANCAGE Stage 0 codebase | PROHIBITED | **PROHIBITED** | None | Stage 0 CLOSED / FROZEN |
| **ACT-09** | Benchmark timing runs or microbenchmarks | PROHIBITED | **PROHIBITED** | None | Strictly barred under R0 |
| **ACT-10** | Foreign source compile-only syntax check | CONDITIONAL | **NOT AUTHORIZED** | None | ODR-07 DEFERRED by Owner |

---

## 5. Non-Implicit Permission & Governance Invariants

1. **Explicit Gate Requirement:** Approval of ACT-01 through ACT-04 authorizes ONLY network retrieval, repository cloning, hash calculation, and external file storage. It confers zero permission for compiler invocation, binary execution, or code alteration.
2. **Rejection / Deferral Enforcement:** Deferral of ODR-07 strictly enforces the prohibition on ACT-10. Rejection or deferral creates zero implicit authorization.
3. **Repository Cleanliness:** The active workspace `F:\Project\RANCAGE\` must remain free of downloaded external source files, foreign git clones, build artifacts, or temporary fetch logs.
4. **Historical Discrepancy Integrity:** The contradiction between Apple M3 MacBook Pro and x86_64 Linux hardware metadata on `/languages2/` is recognized as **UNRESOLVED**. Neither environment may be assumed or asserted as verified fact.
5. **Finding F-01 / A-01 Status:** Historical source provenance remains **OPEN / HIGH BLOCKER** until cryptographically established under Route A1 or formally closed under Route A2.

---

## 6. Execution Prerequisite & Operational Next Steps

1. **Operational Plan Ratification:** Evidence collection must proceed strictly according to [`RPR-R0-EVIDENCE-COLLECTION-PLAN.md`](../evidence/RPR-R0-EVIDENCE-COLLECTION-PLAN.md).
2. **Role Activation:** The Owner delegates evidence gathering execution to the Evidence Collector role.
3. **Audit Handoff:** Upon completion of ACT-01 through ACT-04, the evidence package must be submitted to the QA Engineer for deterministic hash verification, followed by the RANCAGE Auditor for completeness review.

---

**Ratified by Repository Owner — 2026-11-17**  
*RANCAGE must prove performance improvements rather than merely claim them.*
