# RPR-R0 Charter Proposal v0.6

**Document:** RPR-R0 Charter Proposal  
**Version:** 0.6  
**Source revision:** v0.5 with Auditor remediation and Architect governance reconciliation  
**Status:** PROPOSAL — READY FOR AUDITOR REVIEW  
**Baseline:** RANCAGE 0.2.0a1 (`03c6ec15b31eeddf8210223c32ca98793abe4222`)  
**Scope:** Pre-implementation Performance Research Foundation and Historical Benchmark Provenance  

---

## 1. Executive Summary & Purpose

RPR-R0 establishes an empirical research foundation, external archive architecture, provenance verification criteria, and statistical measurement protocol prior to any performance optimization or benchmarking of RANCAGE.

**RANCAGE must prove performance improvements rather than merely claim them.** Stage 0 remains closed and frozen. RPR-R0 authorizes zero source code changes, zero compiler modifications, zero VM optimizations, and zero timing benchmark runs.

This proposal corrects prior drafting errors, eliminates contradictory authorization gates, revokes default permissions for evidence collection, restores exact statistical formulas, and reconciles governance requirements established by independent audit.

---

## 2. Baseline Project Status & Governance Boundaries

All work in RPR-R0 operates under explicit project state baselines:

| Milestone / Component | Formal Status | Operational Boundary |
|---|---|---|
| **Stage 0 (RANCAGE 0.2.0a1)** | **CLOSED / FROZEN** | Commit `03c6ec15b31eeddf8210223c32ca98793abe4222` and tag `v0.2.0a1` immutable. No code edits permitted. |
| **RPR v0.3 Proposal** | **CONDITIONAL APPROVAL / DRAFT ONLY** | Reference research document only. Authorizes no implementation or runner work. |
| **RPR v0.4 Investigation** | **INSUFFICIENT EVIDENCE** | Benchmark source provenance unverified. Published numbers remain unverified context. |
| **Finding F-01 / A-01** | **HIGH BLOCKER / OPEN** | Historical benchmark sources not pinned. Blocks baseline claims and competitive assertions. |
| **RPR-R0 Milestone** | **PROPOSED / NOT AUTHORIZED** | Requires formal Auditor review, QA determinism check, and explicit Owner approval. |
| **R1 Performance Baseline** | **NOT STARTED / NOT AUTHORIZED** | Cannot begin until R0 successfully exits via approved A1 or A2 pathway. |
| **Stage 1 Language Evolution** | **NOT STARTED / NOT AUTHORIZED** | Future language changes remain blocked. |
| **Upstream C Source (`main`)** | **CANDIDATE** | Unpinned to historical benchmark publication; subject to verification under R0. |

Governance Rules:
1. Rejection of any authorization gate creates zero implicit permission.
2. Tooling artifacts (`.roo/`, `.roomodes`) remain local and must never be committed.
3. No git commits, tags, branches, or pushes may be generated under this charter.

---

## 3. Role Independence & Responsibility Matrix (R0.1)

Strict role separation is mandatory. No role or agent session may evaluate, verify, or audit its own outputs.

| Role | Primary Responsibilities | Explicit Prohibitions |
|---|---|---|
| **Owner** | Reviews Charter, executes Owner Decision Register (ODR-01..ODR-07), approves exit pathways (A1/A2), authorizes subsequent milestone proposals. | Cannot modify raw hash logs, evidence manifests, or audit verdicts. |
| **Evidence Collector** | Executes authorized web fetches, clones upstream git repositories, computes SHA-256 hashes, maintains search logs. | Cannot author charter text, assess exit criteria, or act as sole QA verifier of gathered evidence. |
| **Architect** | Drafts charter specifications, defines statistical models, characterizes workload invariants, designs technical boundaries. | Cannot execute benchmark timing, collect primary evidence, or conduct independent compliance audits of own work. |
| **Auditor** | Independently examines archive integrity, verifies hash chains, evaluates search completeness, audits governance adherence. | Cannot gather primary evidence, draft proposals, or execute code modifications. |
| **QA Engineer** | Independently recalculates SHA-256 digests from archived artifacts, validates test scripts, verifies determinism of tools. | Cannot alter recorded benchmark metrics or waive test pass/fail criteria. |

Architect cannot audit own report. Evidence Collector cannot be sole QA verifier of own artifacts.

---

## 4. Tooling & Permission Matrix (10 Operational Activities)

Operational activities require explicit authorization gates. Evidence collection is NOT allowed by default.

| Activity ID | Operational Activity | Default Status | Authorized Role | Prerequisite Gate |
|---|---|---|---|---|
| **ACT-01** | Web snapshot & public URL fetch | **REQUIRES OWNER APPROVAL** | Evidence Collector | ODR-01 and ODR-02 explicit Owner sign-off |
| **ACT-02** | Git clone of external benchmark repos | **REQUIRES OWNER APPROVAL** | Evidence Collector | ODR-01 and ODR-02 explicit Owner sign-off |
| **ACT-03** | SHA-256 manifest computation | **REQUIRES OWNER APPROVAL** | Evidence Collector / QA | ODR-01 and ODR-02 explicit Owner sign-off |
| **ACT-04** | File writing to external evidence archive | **REQUIRES OWNER APPROVAL** | Evidence Collector | ODR-01 and ODR-02 explicit Owner sign-off |
| **ACT-05** | Read-only inspection of RANCAGE source | **ALLOWED** | All Roles | None (read-only architectural analysis) |
| **ACT-06** | Execution of third-party compilers (C, Rust, Zig) | **PROHIBITED** | None | Prohibited under R0; blocked until future R1 |
| **ACT-07** | Execution of compiled third-party binaries | **PROHIBITED** | None | Prohibited under R0; blocked until future R1 |
| **ACT-08** | Modification of RANCAGE Stage 0 codebase/tests | **PROHIBITED** | None | Strict baseline freeze; no code changes allowed |
| **ACT-09** | Benchmark timing runs or microbenchmark execution | **PROHIBITED** | None | Prohibited under R0; requires separate future milestone |
| **ACT-10** | Foreign source compile-only syntax check | **CONDITIONAL** | Evidence Collector | Requires explicit ODR-07 Owner authorization |

Explicit Permission Boundaries:
- Charter approval is distinct from Evidence collection authorization.
- Archive creation authorization is distinct from Compile-only authorization.
- Compiler execution, assembly generation, runtime execution, and benchmark timing remain strictly separated and prohibited in R0.
- Rejection of any authorization gate creates zero implicit permission.

---

## 5. Evidence Archive Location & Storage Integrity Rules

Proposed External Archive Location:
`F:\\Project\\RANCAGE-research-evidence\\RPR-R0\\`

Storage Rules:
1. **External Boundary:** The archive must remain completely outside the primary RANCAGE repository.
2. **Repository Cleanliness:** No raw evidence files, external source snapshots, third-party source trees, or download logs may be committed into the frozen Stage 0 repository.
3. **No Premature Creation:** The archive directory is proposed only. It must NOT be created prior to explicit Owner approval of ODR-02.
4. **Deterministic Structure:**
   ```
   RPR-R0/
   ├── MANIFEST.sha256
   ├── METADATA.json
   ├── snapshots/
   │   ├── benjdd_languages.html
   │   └── benjdd_languages2.html
   ├── upstream_repos/
   │   └── bddicken_languages/
   └── logs/
       └── fetch_session.log
   ```
5. **Cryptographic Integrity:** Every payload file must have its SHA-256 digest recorded in `MANIFEST.sha256`. QA independently verifies all digests before evidence is accepted.
6. **Owner Prerogative:** The final archive location, access protocol, and retention policy require explicit Owner determination under ODR-02.

---

## 6. Evidence Classification Standard

Evidence collected during RPR-R0 must be classified under three strict operational categories:

### 6.1 VERIFIED
Evidence is classified as VERIFIED only when all of the following criteria are satisfied simultaneously:
1. Exact upstream repository URL confirmed.
2. Full 40-character Git commit SHA identified and pinned.
3. Exact source file path within the repository confirmed.
4. SHA-256 cryptographic hash calculated from actual source payload.
5. Independent QA recalculation and confirmation of the SHA-256 digest.
6. Defensible, traceable relationship established between the pinned commit and the historical publication (`benjdd.com/languages2/`).
7. Exact workload identity and parameter mapping confirmed (e.g., input parameter `40` verified from source code).
8. Zero unresolved material contradictions between source code and published execution characteristics.

*Note:* Verbatim text matching against publication snippets is NOT required unless the publication provided complete source code and exact textual identity is functionally relevant.

### 6.2 CANDIDATE
Evidence is classified as CANDIDATE when:
- Repository or source branch is identified (e.g. upstream `bddicken/languages` branch `main`), but the exact historical commit SHA corresponding to the publication date is not cryptographically pinned.
- Workload implementation exists, but parameter binding or build configuration requires further verification.
- Artifacts cannot be used to establish baseline performance targets until elevated to VERIFIED.

### 6.3 UNRESOLVED
Evidence is classified as UNRESOLVED when:
- No matching commit, branch, or snapshot has been located.
- Published figures have no verifiable source mapping or commit traceability.
- Conflicting records exist regarding toolchain version, build flags, or input arguments.

---

## 7. Four-Status Reproducibility Model

Reproducibility must be tracked across four separate, independently reported status dimensions. No automatic sequential dependency is imposed when claim-specific evidence does not require it.

1. **SOURCE PINNED:**
   - Exact commit SHA identified and verified in upstream repository.
   - Source payload matches archived SHA-256 digest.
   - Workload code corresponds to documented implementation under investigation.

2. **BUILD REPRODUCED:**
   - Source is successfully compiled under documented toolchain version and compilation flags.
   - Zero compilation or linker errors.
   - *Note:* A build result does not prove runtime correctness or timing reproduction. A workload may be STATICALLY CHARACTERIZED without being WORKLOAD VALIDATED.

3. **WORKLOAD VALIDATED:**
   - Execution invariants, input parameter mapping (e.g. input `40`), and algorithmic complexity verified.
   - Loop bounds, recursive structures, or array update counts match analytical workload model.
   - Absence of silent compiler optimization dead-code elimination confirmed.

4. **TIMING REPRODUCED:**
   - Execution timing performed under controlled, documented hardware/OS conditions with paired batches.
   - Empirical distribution aligns with published benchmark numbers within statistical confidence bounds.
   - *Scope Invariant:* Timing reproduction is strictly OUTSIDE the scope of RPR-R0.

---

## 8. Acceptance Pathways & Exit Criteria

RPR-R0 provides two defined exit pathways. Approval of the charter authorizes neither pathway automatically.

### 8.1 Route A1 — Historical Source Successfully Pinned
- **Acceptance Condition:** Core historical workloads (C, Rust, Zig) achieve `SOURCE PINNED` status with verified SHA-256 digests. Traceability to published `/languages2/` metrics is defensibly established.
- **R1 Boundary Constraint:** A successful A1 exit may support the preparation of a separate R1 proposal. **It must NOT automatically authorize R1 planning execution, benchmark runs, profiling, or implementation.** R1 requires its own independent proposal, auditor review, QA verification, and explicit Owner authorization.

### 8.2 Route A2 — Historical Reference Only
- **Acceptance Condition:** The exhaustive A2 search protocol (§9) establishes that historical source commits cannot be recovered from public repositories, archives, or web traces.
- **Consequence:** Published figures on `benjdd.com/languages2/` are designated as historical reference context only. All claims of historical compatibility are formally removed. RANCAGE benchmark efforts pivot exclusively to the documented current upstream specification (RPB-001-N).
- **Governance Requirement:** Route A2 cannot be selected merely because an agent session or tool lacks access. Selection requires an independent Auditor assessment confirming search completeness and explicit Owner acceptance.

### 8.3 Common Deliverable Artifacts
Regardless of exit route, RPR-R0 must produce:
1. `MANIFEST.sha256` covering all gathered research artifacts.
2. Complete `SEARCH_LOG.md` adhering to the checklist in §9.
3. Workload characterization report analyzing input parameter semantics.
4. Independent Auditor Review Report and QA Determinism Verification Report.

---

## 9. A2 Search Completeness Checklist & Search Log Requirements

To invoke Route A2, the Evidence Collector and Auditor must exhaustively execute and verify searches across all 14 mandatory categories:

### 9.1 Mandatory Search Target Categories
1. **Repository URLs:** Primary upstream repositories, known mirrors, author personal repositories, and forks.
2. **Branches and Tags:** All active, historical, and archived branches and tags in the repository network.
3. **Full Git Commit History:** Complete commit logs, commit messages, and tree hashes from root to HEAD.
4. **Source Implementations:** C, Rust, and Zig source files across all historical directory layouts.
5. **README & Specifications:** Workload documentation, specifications, and explanatory notes across revisions.
6. **Changelogs & Release Notes:** Project release notes, tagged version changelogs, and author announcements.
7. **Build Scripts:** Makefiles, shell scripts, cargo configurations, build.zig, or compiler driver scripts.
8. **Runner & Harness Scripts:** In-process harness drivers, execution scripts, and timing wrappers.
9. **Hyperfine Invocations:** Command-line invocations, argument strings, shell wrappers, and parameter flags.
10. **Warmup Configurations:** Recorded warmup iteration counts, cache preparation steps, and shell options.
11. **Historical Publication Pages:** Current and historical versions of `benjdd.com/languages/` and `benjdd.com/languages2/`.
12. **HTML / WARC Snapshots:** Complete page source, DOM structure, and associated stylesheet or script metadata.
13. **Internet Archive / Wayback Machine:** Historical crawls of publication URLs covering the 2024–2026 timeframe.
14. **External Discussions & Issues:** Issue tracker threads, pull request reviews, forum posts, and external commentary.

### 9.2 Search Log Record Schema
Every entry in `SEARCH_LOG.md` must record all eight fields:
1. `Item searched` (exact target, URL, commit query, or filename).
2. `Search date` (UTC timestamp).
3. `Tool / access method` (git command, web fetch, archive query, or manual browser).
4. `Result` (FOUND, NOT_FOUND, or PARTIAL).
5. `Artifact location and hash` (if found, path and SHA-256 digest).
6. `Reason when not found` (exact technical explanation).
7. `Alternative methods considered` (subsequent search attempts).
8. `Relationship to target workload` (functional mapping to historical published numbers).

*Rule:* An unavailable tool, connection timeout, or failed session cannot establish that source is unrecoverable.

---

## 10. Statistical Methodology Specification

All statistical comparative analysis is proposed on the log-ratio scale to ensure symmetry, scale invariance, and statistical robustness.

### 10.1 Primary Analysis Scale: Log-Ratio
Comparative ratio definition:
$$L = \ln(T_{\text{candidate}} / T_{\text{reference}})$$

Decision criteria under 95% Confidence Interval (CI):
- **Candidate Faster:** Upper bound of 95% CI < 0.
- **Candidate Slower:** Lower bound of 95% CI > 0.
- **Inconclusive:** 95% CI includes 0.

### 10.2 Transformed Ratio Scale
For reporting convenience, the exponentiated ratio may be presented alongside log-ratio:
$$R = \exp(L) = T_{\text{candidate}} / T_{\text{reference}}$$

Decision criteria under transformed 95% CI:
- **Candidate Faster:** Upper bound of transformed 95% CI < 1.0.
- **Candidate Slower:** Lower bound of transformed 95% CI > 1.0.
- **Inconclusive:** Transformed 95% CI includes 1.0.

### 10.3 Proposed Measurement Protocol
- **Warmup:** 5 warmup iterations per implementation prior to data collection.
- **Batches:** 30 paired measured batches.
- **Pairing:** Exactly 1 reference measurement and 1 candidate measurement per batch.
- **Ratio Calculation:** Exactly 1 log-ratio $L$ calculated per candidate per batch.
- **Execution Order:** Rotated or randomized execution order between batches to eliminate thermal or order bias.
- **Confidence Interval Estimation:** Paired bootstrap percentile 95% CI.
- **Bootstrap Parameters:** 10,000 resamples.
- **RNG Seed:** Fixed seed `20261117` for deterministic verification.
- **Pairing Preservation:** Resampling must strictly preserve reference/candidate pairing within each batch. For multi-candidate comparisons, same-batch relationships across all candidates must be maintained.

*Governance Boundary:* This protocol is **PROPOSED / NOT VALIDATED**. No pilot execution is authorized under RPR-R0. A statistical pilot requires a separate proposal, audit review, and Owner authorization.

---

## 11. Owner Decision Register (ODR-01 through ODR-07)

The Owner Decision Register contains seven formal decision gates. Rejection of any gate creates zero implicit permission.

### ODR-01: Evidence Collection Authorization
- **Question:** Shall the Evidence Collector be authorized to execute ACT-01 through ACT-04 to gather external benchmark sources?
- **Options:** Approve | Reject | Defer
- **Consequences of Approval:** Authorizes network retrieval, repo cloning, and manifest generation into the approved archive location.
- **Consequences of Rejection:** External evidence gathering remains prohibited; R0 cannot proceed with empirical data collection.

### ODR-02: Archive Location & Storage Format
- **Question:** Shall the proposed external archive directory `F:\\Project\\RANCAGE-research-evidence\\RPR-R0\\` be adopted as the official storage location?
- **Options:** Approve | Reject | Designate Alternative
- **Consequences of Approval:** Formalizes external archive directory path and immutable storage structure.
- **Consequences of Rejection:** Archive cannot be instantiated; alternative location must be proposed and reviewed.

### ODR-03: Contingency Adoption of Pathway A2
- **Question:** In the event that historical source commits are unrecoverable after exhaustive search, shall Route A2 (Historical Reference Only) be authorized as an approved fallback?
- **Options:** Approve A1 + A2 Contingency | A1-Only (Require source pinning)
- **Consequences of Approval:** Allows project to decouple from unpinned historical numbers upon verified completion of the A2 checklist.
- **Consequences of Rejection:** Project must remain blocked until exact historical source commits are recovered or project is cancelled.

### ODR-04: Benchmark Warning Remediation
- **Question:** Shall explicit warning banners be mandated on all documentation referencing `benjdd.com/languages2/` metrics indicating they are unverified external figures?
- **Options:** Approve | Reject
- **Consequences of Approval:** Mandates immediate placement of disclaimer notices preventing misinterpretation of published numbers as RANCAGE performance targets.
- **Consequences of Rejection:** External numbers remain unannotated, retaining risk of improper performance claims.

### ODR-05: Mandatory Workload-Shape Characterization
- **Question:** Shall workload algorithmic characterization (loop structure, memory access, input `40` binding) be required before any build reproduction?
- **Options:** Approve | Reject
- **Consequences of Approval:** Guarantees deep algorithmic analysis before compiler execution; prevents benchmarking mismatched workloads.
- **Consequences of Rejection:** Workloads might be compiled without verified equivalence.

### ODR-06: Statistical Pilot Milestone Separation
- **Question:** Shall statistical pilot execution be formally isolated as a separate future milestone requiring its own charter and authorization?
- **Options:** Approve | Reject
- **Consequences of Approval:** Prevents unauthorized execution of benchmark timing runs during preliminary research.
- **Consequences of Rejection:** Risk of uncoordinated or invalid timing runs conducted under preliminary charters.

### ODR-07: Separate Compile-Only Toolchain Authorization
- **Question:** Shall the Evidence Collector be granted conditional permission (ACT-10) to run third-party compilers solely for syntax and AST validation without binary execution?
- **Options:** Approve | Reject
- **Consequences of Approval:** Permits checking whether archived source compiles under targeted flags, strictly forbidding execution.
- **Consequences of Rejection:** Third-party compiler invocation strictly prohibited; source verification remains entirely visual/textual.

*Exclusion Notice:* Decisions regarding Typed IR implementation, Cranelift feasibility study, and Four Measurement Modes adoption are excluded from this charter as premature.

---

## 12. Risk Register (11 Inherent Risks & Mitigations)

| Risk ID | Risk Summary | Severity | Mitigation Strategy |
|---|---|---|---|
| **R-01** | Historical commit hash deleted or purged from upstream git history. | HIGH | Execute immediate search across public forks; fall back to Route A2 if unrecoverable. |
| **R-02** | Input parameter `40` represents different workload scales across languages. | HIGH | Mandatory workload-shape verification (ODR-05) prior to any comparative assertion. |
| **R-03** | Premature VM optimization corrupting Stage 0 language semantics. | CRITICAL | Code modification strictly prohibited (ACT-08); Stage 0 codebase remains frozen. |
| **R-04** | Undocumented host compiler or kernel upgrades skewing results. | MEDIUM | Mandatory recording of toolchain versions, OS patch level, and CPU topology in `METADATA.json`. |
| **R-05** | Silent cryptographic bit-rot or payload mutation in evidence archive. | HIGH | Independent QA recalculation and continuous verification against `MANIFEST.sha256`. |
| **R-06** | Accidental conflation of `/languages/` (M3 Mac) and `/languages2/` (Linux) data. | HIGH | Strict document separation; `/languages2/` recognized as sole source of historical comparison table. |
| **R-07** | Execution of untrusted foreign benchmark binaries on development host. | CRITICAL | ACT-07 strictly prohibited; zero binary execution permitted under RPR-R0. |
| **R-08** | Incomplete search logging leading to premature invocation of Route A2. | MEDIUM | Mandatory execution of 14-point search checklist; independent Auditor validation required. |
| **R-09** | Role contamination (e.g., collector auditing own evidence). | HIGH | Strict separation enforced: Evidence Collector cannot act as sole QA verifier or Auditor. |
| **R-10** | Microbenchmark timing noise obscuring true execution differences. | MEDIUM | Paired batching (30 batches), 5 warmups, log-ratio analysis, bootstrap 10,000 resamples. |
| **R-11** | Ambiguity between compile-only syntax checks and full compilation. | MEDIUM | ODR-07 explicitly defines command boundaries; binary generation/execution blocked. |

---

## 13. Audit Findings Disposition (F-01 through F-10)

This charter explicitly addresses all findings from prior architectural and independent audits:

| Finding ID | Finding Title | Severity | Operative Charter Disposition |
|---|---|---|---|
| **F-01 / A-01** | Historical benchmark sources not pinned | HIGH BLOCKER | **OPEN / PRIMARY MISSION.** Published `/languages2/` metrics remain unverified external figures. No baseline or ranking claims permitted until pinned under Route A1 or formally decoupled under Route A2. |
| **F-02** | Absence of intermediate Typed IR milestone | HIGH | **ADDRESSED.** RPR architecture preserves Typed IR as a standalone design phase (R3); implementation is excluded from R0 and Stage 0. |
| **F-03** | Bounds Check Elimination lacks formal safety proof | HIGH | **ADDRESSED.** BCE remains blocked by default. Any future compiler optimization proposal requires formal mathematical invariant proofs and explicit Owner authorization. |
| **F-04 / A-02** | Integer overflow semantic variance across targets | HIGH | **OPEN PENDING R0 EVIDENCE.** Evidence Collector must document bit-width, arithmetic overflow behavior, and intermediate value ranges for all candidate workloads. Equivalence cannot be assumed. |
| **F-05 / N-5** | Incomplete environmental telemetry and statistical protocol | MEDIUM | **ADDRESSED.** Environmental telemetry codified in `METADATA.json`. Statistical protocol standardized on log-ratio analysis ($L = \\ln(T_{\\text{cand}}/T_{\\text{ref}})$) with 95% bootstrap CI. |
| **F-06** | Ambiguous timing boundaries and runtime metrics | MEDIUM | **ADDRESSED.** Timing boundaries formally defined across measurement modes; all timing measurement is explicitly excluded from R0. |
| **F-07** | Unclear optimization dependency order | MEDIUM | **ADDRESSED.** Strict milestone sequence enforced. Compiler and VM optimization proposals cannot be introduced prior to verified empirical baselines. |
| **F-08 / N-7** | Unclear toolchain policy and external compiler dependency | MEDIUM | **ADDRESSED.** Python remains sole canonical implementation. Third-party compilers (Cranelift, GCC, Clang, Rustc) are prohibited in R0 except for conditional compile-only syntax checks under ODR-07. |
| **F-09 / N-3** | Array layout assumptions without legacy workload proof | MEDIUM | **SCOPED.** Array allocation characteristics evaluated as part of workload-shape validation (ODR-05). Stage 0 list semantics remain untouched. |
| **F-10** | Competitive ranking asserted before local baseline | LOW | **ADDRESSED.** All competitive ranking claims are strictly prohibited. Published external numbers are contextual references only. |

---

## 14. Compile-Only Syntax Check Operational Boundaries

If Owner approves ODR-07, the Evidence Collector is authorized to execute third-party compiler drivers under strict compile-only constraints (ACT-10).

Operational Rules:
1. **Permitted Flags:** Invocations must restrict compiler behavior to syntax, type-checking, or AST verification (e.g. `gcc -fsyntax-only`, `clang -fsyntax-only`, `rustc --emit=metadata -Zno-codegen`, or `zig build-obj` without emitting executables).
2. **Prohibited Flags:** Any flag generating executable binary objects, machine code, or assembly output for execution is strictly forbidden.
3. **Prohibited Execution:** Direct execution of compiled artifacts (e.g. `./a.out`, `./benchmark`) is prohibited under any circumstances (ACT-07).
4. **Toolchain Logging:** Every invocation must log exact compiler version (`--version`), host environment, input file SHA-256, and complete terminal output in `METADATA.json`.

---

## 15. Milestone Sequence & Verification Gates

RPR-R0 enforces a strict six-stage governance sequence:

1. **Charter Review:** Architectural and compliance review of this proposal.
2. **Explicit Owner Approval:** Formal execution of the Owner Decision Register (ODR-01..ODR-07).
3. **Evidence Collection:** Authorized execution of ACT-01 through ACT-04 into the external archive.
4. **Auditor Review:** Independent audit verifying provenance, archive integrity, and A1/A2 criteria.
5. **QA Verification:** Independent recalculation of all cryptographic digests and deterministic validation.
6. **Owner Final Sign-off:** Formal acceptance of RPR-R0 completion and determination of next milestones.

*Rule:* Approval of the charter alone activates zero evidence collection. Evidence collection requires explicit approval of ODR-01 and ODR-02.

---

## 16. Technical Scope Restrictions & Non-Authorization Invariants

To safeguard language integrity and baseline stability, RPR-R0 explicitly does NOT authorize:
- Any modification to RANCAGE Stage 0 source code or frozen test suites.
- Virtual machine optimizations, instruction reordering, or bytecode layout changes in `src/rancage/vm.py`.
- Compiler changes or AST restructuring in `src/rancage/compiler.py` or `src/rancage/typesys.py`.
- Implementation of intermediate Typed IR or Bounds Check Elimination (BCE).
- Native backend implementation, code generation, or LLVM/Cranelift integrations.
- Implementation of an in-process benchmark harness or CLI timing commands.
- Benchmark timing measurements, microbenchmark profiling, or ranking assertions.
- Implementation of Stage 1 language evolution features.
- Execution or authorization of the R1 performance baseline milestone.
- Modification of local tooling configuration files (`.roo/`, `.roomodes`).
- Creation of git commits, tags, branches, or remote pushes.

---

## 17. External References & Source Citations

1. **Historical Benchmark Publication:** `https://benjdd.com/languages/`  
   Historical context only (`/usr/bin/time`, lowest of 3 runs, M3 Mac). Not used as the quantitative basis for performance comparisons.
2. **Hyperfine Comparative Benchmark Publication:** `https://benjdd.com/languages2/`  
   Source of external comparative metrics (mean, stddev, range, 3 runs, x86_64 Linux). All figures remain unverified external claims.
3. **Upstream Benchmark Repository:** `https://github.com/bddicken/languages`  
   Branch `main` represents a CANDIDATE implementation pending cryptographic source pinning.
4. **RANCAGE Project Specifications:**
   - `PROJECT_STATUS.md` — Project Status Baseline
   - `AGENTS.md` — Agent Invariants and Governance Workflow
   - `SPEC.md` — Language Foundation Specification
   - `ROADMAP.md` — Project Roadmap and Release Rules

---

## 18. Final Document Disposition & Governance Invariant

- **Document State:** PROPOSAL — READY FOR AUDITOR REVIEW.
- **Auditor Sign-off Status:** No independent Auditor approval is claimed or implied by the authorship of this proposal. Formal review by the RANCAGE Auditor is an external requirement.
- **Closing Principle:** **RANCAGE must prove performance improvements rather than merely claim them.**

