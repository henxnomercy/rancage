# RPR-R0 Charter Proposal v0.8

**Document:** RPR-R0 Charter Proposal  
**Version:** 0.8  
**Source revision:** v0.7 with Auditor remediation and targeted Charter v0.8 corrections  
**Status:** PROPOSAL — READY FOR AUDITOR REVIEW  
**Baseline:** RANCAGE 0.2.0a1 (`03c6ec15b31eeddf8210223c32ca98793abe4222`)  
**Scope:** Pre-implementation Performance Research Foundation and Historical Benchmark Provenance  

---

## 1. Executive Summary & Purpose

RPR-R0 establishes an empirical research foundation, external archive architecture, provenance verification criteria, and statistical measurement protocol prior to any performance optimization or benchmarking of RANCAGE.

**RANCAGE must prove performance improvements rather than merely claim them.** Stage 0 remains closed and frozen. RPR-R0 authorizes zero source code changes, zero compiler modifications, zero VM optimizations, and zero timing benchmark runs.

This proposal corrects the findings identified in the independent audit of v0.7: restoring missing §17 (External References & Source Citations) and §18 (Final Document Disposition & Governance Invariant), correcting the C-10 cross-reference to §14 and §15, resolving the §8.1 Auditor role contradiction, and fixing subsection numbering and Markdown formatting.

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

## 3. Finding Identification Namespaces

To prevent ambiguity between historical RPR audit findings and Charter-specific remediation requirements, this Charter adopts two separate identifier namespaces:

| Namespace | Identifier Range | Scope |
|---|---|---|
| **Legacy RPR Audit Findings** | **L-01 through L-10** | Findings inherited from prior RPR proposal audits (e.g., Typed IR absence, BCE proof requirement, integer overflow semantics, optimization dependency order, ranking assertions, `/languages/` vs `/languages2/` conflation, input `40` attribution, archived page evidence, in-process harness implication, CI estimator unpinned, upstream `main` facts unpinned). |
| **Charter-Specific Requirements** | **C-01 through C-10** | Requirements defined and addressed within this Charter document: evidence classification, compiler optimization assessment, STATICALLY CHARACTERIZED vs WORKLOAD VALIDATED distinction, independent QA SHA-256 verification, paired measured batch definition, statistical threshold consistency, workload validation evidence, A2 search completeness and investigation log, role independence and search responsibility, separate compile-only authorization. |

All references in this Charter, finding disposition tables, and change history use the correct namespace. Legacy findings preserve their original audit meaning. Charter requirements are evaluated against the operative text of this document.

---

## 4. Role Independence & Responsibility Matrix (R0.1)

Strict role separation is mandatory. No role or agent session may evaluate, verify, or audit its own outputs.

| Role | Primary Responsibilities | Explicit Prohibitions |
|---|---|---|
| **Owner** | Reviews Charter, executes Owner Decision Register (ODR-01..ODR-07), approves exit pathways (A1/A2), authorizes subsequent milestone proposals, approves investigation scope, resolves disputed or incomplete search outcomes. | Cannot modify raw hash logs, evidence manifests, or audit verdicts. |
| **Evidence Collector** | Performs approved web and repository searches. Downloads and archives approved evidence. Records queries, URLs, dates, tools, outcomes, and limitations. Maintains the investigation log. Computes SHA-256 hashes of acquired artifacts. | Cannot author charter text, assess exit criteria, act as sole QA verifier of gathered evidence, or execute searches outside approved scope. |
| **Architect** | Drafts charter specifications, defines statistical models, characterizes workload invariants, designs technical boundaries, defines evidence requirements, analyzes collected material, prepares technical conclusions and provenance assessments. | Cannot execute benchmark timing, collect primary evidence, conduct independent compliance audits of own work, or perform search execution. |
| **Auditor** | Independently reviews the investigation log. Evaluates whether the search checklist was adequately covered. Examines source provenance and evidence consistency. Identifies omitted search paths or insufficient explanations. May request additional investigation through the authorized workflow. | Cannot gather primary evidence, draft proposals, execute code modifications, or execute searches (the Auditor does not act as the Evidence Collector). |
| **QA Engineer** | Independently recalculates SHA-256 digests from archived artifacts. Checks manifest integrity and evidence preservation. Validates test scripts and verifies determinism of tools. | Cannot alter recorded benchmark metrics or waive test pass/fail criteria. |

Architect cannot audit own report. Evidence Collector cannot be sole QA verifier of own artifacts. Auditor does not execute searches.

---

## 5. Evidence Classification Standard

Evidence collected during RPR-R0 must be classified under three strict operational categories:

### 5.1 VERIFIED
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

### 5.2 CANDIDATE
Evidence is classified as CANDIDATE when:
- Repository or source branch is identified (e.g. upstream `bddicken/languages` branch `main`), but the exact historical commit SHA corresponding to the publication date is not cryptographically pinned.
- Workload implementation exists, but parameter binding or build configuration requires further verification.
- Artifacts cannot be used to establish baseline performance targets until elevated to VERIFIED.

### 5.3 UNRESOLVED
Evidence is classified as UNRESOLVED when:
- No matching commit, branch, or snapshot has been located.
- Published figures have no verifiable source mapping or commit traceability.
- Conflicting records exist regarding toolchain version, build flags, or input arguments.

---

## 6. Four-Status Reproducibility Model

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

## 7. Acceptance Pathways & Exit Criteria

RPR-R0 provides two defined exit pathways. Approval of the charter authorizes neither pathway automatically.

### 7.1 Route A1 — Historical Source Successfully Pinned
- **Acceptance Condition:** Core historical workloads (C, Rust, Zig) achieve `SOURCE PINNED` status with verified SHA-256 digests. Traceability to published `/languages2/` metrics is defensibly established.
- **R1 Boundary Constraint:** A successful A1 exit may support the preparation of a separate R1 proposal. **It must NOT automatically authorize R1 planning execution, benchmark runs, profiling, or implementation.** R1 requires its own independent proposal, auditor review, QA verification, and explicit Owner authorization.

### 7.2 Route A2 — Historical Reference Only
- **Acceptance Condition:** The exhaustive A2 search protocol (§8) establishes that historical source commits cannot be recovered from public repositories, archives, or web traces.
- **Consequence:** Published figures on `benjdd.com/languages2/` are designated as historical reference context only. All claims of historical compatibility are formally removed. RANCAGE benchmark efforts pivot exclusively to the documented current upstream specification (RPB-001-N).
- **Governance Requirement:** Route A2 cannot be selected merely because an agent session or tool lacks access. Selection requires an independent Auditor assessment confirming search completeness and explicit Owner acceptance.

### 7.3 Common Deliverable Artifacts
Regardless of exit route, RPR-R0 must produce:
1. `MANIFEST.sha256` covering all gathered research artifacts.
2. Complete `SEARCH_LOG.md` adhering to the checklist in §8.
3. Workload characterization report analyzing input parameter semantics.
4. Independent Auditor Review Report and QA Determinism Verification Report.

---

## 8. A2 Search Completeness Checklist & Search Log Requirements

To invoke Route A2, the Evidence Collector and Auditor must fulfill their distinct responsibilities across all 14 mandatory categories:

**Evidence Collector**
- Executes approved searches.
- Records search methods, dates, URLs, results, and limitations.
- Preserves the collected artifacts.
- Maintains the investigation log.

**Auditor**
- Independently reviews the investigation log.
- Assesses coverage of all required search categories.
- Checks the adequacy of explanations for unsuccessful searches.
- Identifies missing search paths.
- Requests additional investigation through the authorized workflow.

The Auditor must not perform the Evidence Collector's search execution responsibilities. The Auditor independently evaluates completeness without becoming the Evidence Collector.

### 8.1 Mandatory Search Target Categories
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

### 8.2 Search Log Record Schema
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

## 9. Statistical Methodology Specification

All statistical comparative analysis is proposed on the log-ratio scale to ensure symmetry, scale invariance, and statistical robustness.

### 9.1 Primary Analysis Scale: Log-Ratio
Comparative ratio definition:
$$L = \\ln(T_{\\text{candidate}} / T_{\\text{reference}})$$

Decision criteria under 95% Confidence Interval (CI):
- **Candidate Faster:** Upper bound of 95% CI < 0.
- **Candidate Slower:** Lower bound of 95% CI > 0.
- **Inconclusive:** 95% CI includes 0.

### 9.2 Transformed Ratio Scale
For reporting convenience, the exponentiated ratio may be presented alongside log-ratio:
$$R = \\exp(L) = T_{\\text{candidate}} / T_{\\text{reference}}$$

Decision criteria under transformed 95% CI:
- **Candidate Faster:** Upper bound of transformed 95% CI < 1.0.
- **Candidate Slower:** Lower bound of transformed 95% CI > 1.0.
- **Inconclusive:** Transformed 95% CI includes 1.0.

### 9.3 Proposed Measurement Protocol
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

## 10. Owner Decision Register (ODR-01 through ODR-07)

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

## 11. Risk Register (11 Inherent Risks & Mitigations)

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

## 12. Charter-Specific Requirements Disposition (C-01 through C-10)

This section maps the ten Charter-specific requirements (C-01 through C-10) to their operative disposition in v0.7.

| ID | Requirement | Operative Section | Disposition |
|---|---|---|---|
| **C-01** | VERIFIED / CANDIDATE / UNRESOLVED evidence classification | §5 | **ADDRESSED.** Full classification criteria established. |
| **C-02** | Compiler Optimization Assessment taxonomy | §13 | **ADDRESSED.** Four-state taxonomy (EXPECTED / POSSIBLE / UNKNOWN / VERIFIED) defined with explicit prohibition on static-inspection-only VERIFIED status. |
| **C-03** | STATICALLY CHARACTERIZED vs WORKLOAD VALIDATED | §6 | **ADDRESSED.** Distinction defined under Four-Status Reproducibility Model. |
| **C-04** | Independent QA SHA-256 verification | §5.1, §4 | **ADDRESSED.** QA independently recalculates digests; Evidence Collector cannot be sole verifier. |
| **C-05** | Paired measured batch definition | §9.3 | **ADDRESSED.** 1 reference + 1 candidate per batch, 1 log-ratio per pair, pairing preserved. |
| **C-06** | Statistical threshold and log-ratio consistency | §9.1–9.2 | **ADDRESSED.** L<0 faster, L>0 slower, includes 0 inconclusive; R<1 / >1 / includes 1 consistent. |
| **C-07** | Evidence requirements for workload validation | §6, §13 | **ADDRESSED.** Workload invariants defined; evidence-type-per-claim matrix in §13. |
| **C-08** | A2 Search Completeness and Investigation Log | §8 | **ADDRESSED.** 14 categories and 8 search-log fields defined. |
| **C-09** | Role Independence and search responsibility | §4 | **ADDRESSED.** Auditor reviews log only; does not execute searches. |
| **C-10** | Separate Compile-only Authorization | §14, §15 | **ADDRESSED.** ODR-07 separate from evidence collection (§10); ACT-10 defined in §14; parameters defined in §15. |

---

## 13. Compiler Optimization Assessment Taxonomy

Compiler optimization assessment uses four distinct operational labels. Static source inspection must never establish VERIFIED status for actual compiler behavior.

| Label | Definition | Evidence Required |
|---|---|---|
| **EXPECTED** | Documentation, compiler specifications, or language rules indicate that an optimization should normally be applicable. | Compiler documentation or language specification citation. This is not proof of actual compiler behavior. |
| **POSSIBLE** | The source and configuration appear to permit the optimization, but there is insufficient evidence that it occurred. | Static source analysis showing syntactic/configurational permissibility. |
| **UNKNOWN** | Available evidence is insufficient to assess whether the optimization is applicable or performed. | Absence of documentation or analyzable configuration. |
| **VERIFIED** | Direct evidence from the exact compiler version, source revision, compilation configuration, and resulting compiler output demonstrates the optimization. | Exact compiler version, source revision, compilation flags, and generated assembly or IR output. |

**Evidence-Type-to-Claim Mapping:**

| Claim Type | Permitted Evidence | Insufficient Evidence |
|---|---|---|
| Static source characterization | Source file content, AST, control-flow graph | Compiler output, runtime measurements |
| Compiler optimization applicability | Compiler documentation, language specification | Source inspection alone |
| Actual compiler optimization behavior | Generated assembly, IR dump, compiler diagnostic | Static source inspection |
| Runtime workload behavior | Instrumented execution trace, profiler output | Assembly listing alone |

**Assembly Evidence Rule:** Assembly evidence supports claims about generated compiler output. Runtime evidence supports claims about executed behavior. Assembly and runtime evidence are not universally interchangeable.

**Authorization Boundary:** Assembly generation requires separate explicit Owner authorization. Compile-only syntax checking does not imply permission to generate assembly or object files. No compiler execution or assembly generation is authorized by this document.

---

## 14. Tooling & Permission Matrix (10 Operational Activities)

Operational activities require explicit authorization gates. Evidence collection is NOT allowed by default.

| Activity ID | Operational Activity | Default Status | Authorized Role | Prerequisite Gate |
|---|---|---|---|---|
| **ACT-01** | Web snapshot & public URL fetch | **REQUIRES OWNER APPROVAL** | Evidence Collector | ODR-01 and ODR-02 explicit Owner sign-off |
| **ACT-02** | Git clone of external benchmark repos | **REQUIRES OWNER APPROVAL** | Evidence Collector | ODR-01 and ODR-02 explicit Owner sign-off |
| **ACT-03** | SHA-256 manifest computation | **REQUIRES OWNER APPROVAL** | Evidence Collector / QA | ODR-01 and ODR-02 explicit Owner sign-off |
| **ACT-04** | File writing to external evidence archive | **REQUIRES OWNER APPROVAL** | Evidence Collector | ODR-01 and ODR-02 explicit Owner sign-off |
| **ACT-05** | Read-only inspection of RANCAGE source | **ALLOWED** | All Roles | None (read-only architectural analysis) |
| **ACT-06** | Execution of third-party compilers (C, Rust, Zig) | **PROHIBITED** | None | Prohibited under R0; requires ODR-07 plus separate authorization |
| **ACT-07** | Execution of compiled third-party binaries | **PROHIBITED** | None | Prohibited under R0; blocked until separately authorized milestone |
| **ACT-08** | Modification of RANCAGE Stage 0 codebase/tests | **PROHIBITED** | None | Strict baseline freeze; no code changes allowed |
| **ACT-09** | Benchmark timing runs or microbenchmark execution | **PROHIBITED** | None | Prohibited under R0; requires separate future milestone |
| **ACT-10** | Foreign source compile-only syntax check | **CONDITIONAL** | Evidence Collector | Requires explicit ODR-07 Owner authorization |

Explicit Permission Boundaries:
1. Charter approval.
2. Evidence collection authorization.
3. Archive creation authorization.
4. Compile-only authorization.
5. Compiler execution.
6. Assembly generation.
7. Runtime execution.
8. Benchmark timing.

These eight permissions are distinct. Approval of one does not imply approval of another. Rejection of any authorization gate creates zero implicit permission.

---

## 15. Compile-Only Authorization Parameters

If Owner approves ODR-07, the Evidence Collector may execute third-party compiler drivers under strict compile-only constraints (ACT-10). The following parameters must be recorded before execution and are subject to Owner approval.

1. **Allowed compiler identity:** Explicit compiler family and binary path (e.g. `gcc`, `clang`, `rustc`, `zig`) named per workload.
2. **Allowed compiler version:** Exact version string pinned per compiler. Unpinned or auto-updating toolchains are prohibited.
3. **Allowed sources and commands:** Exact source file paths and exact command lines, restricted to syntax, type-checking, or AST verification (e.g. `gcc -fsyntax-only`, `clang -fsyntax-only`, `rustc --emit=metadata`).
4. **Permitted output artifacts:** Only diagnostics or metadata artifacts. Object files, machine code, assembly listings, and executables are NOT permitted outputs.
5. **Output directory:** A declared subdirectory inside the approved external archive (`logs/compile-only/`). No writes into the RANCAGE repository.
6. **Artifact preservation and hashing:** Every diagnostic artifact hashed with SHA-256 and registered in `MANIFEST.sha256`; QA recalculates independently.
7. **Prohibition on execution:** Executing any generated artifact remains prohibited without separate explicit Owner authorization (ACT-07).

Compile-only authorization does not implicitly permit assembly generation, runtime validation, benchmark execution, or performance measurement.

---

## 16. External Benchmark Metadata Handling

The historical benchmark metadata contains unresolved conflicts. This Charter does not resolve them by assumption.

### 16.1 Claim Provenance Categories

| Category | Meaning |
|---|---|
| **Publication-stated** | Explicitly stated on the published benchmark page. |
| **Repository-indicated** | Indicated by an upstream repository file or documentation. |
| **Prior-investigation-reported** | Reported by earlier internal investigation records. |
| **Unverified** | No direct supporting evidence located. |

### 16.2 Recorded Observations (Unresolved)

| Observation | Category | Source |
|---|---|---|
| `/languages/` uses `/usr/bin/time`, three runs with lowest retained, M3 MacBook Pro 16 GB | Publication-stated / Prior-investigation-reported | `benjdd.com/languages/`; RPR v0.3 §2.1 |
| `/languages2/` uses Hyperfine, three runs, mean ± standard deviation and min–max range, M3 MacBook Pro 16 GB | Publication-stated / Prior-investigation-reported | `benjdd.com/languages2/`; RPR v0.3 §2.2 |
| `/languages2/` hardware/OS described as x86_64 Linux | Prior-investigation-reported (conflicting) | Not established in RPR v0.3 §2.2 |
| `Input value of 40 given to each` | Publication-stated | Both pages; per-workload binding unverified |
| Toolchain: Zig 0.13.0, Rust/Cargo 1.82.0, Apple Clang 16.0.0 | Publication-stated / Prior-investigation-reported | RPR v0.3 §2.2 |
| Hyperfine `--warmup` used; warmup count and full command unpinned | Publication-stated (partial) | RPR v0.3 §2.2 |

### 16.3 Unresolved Status Rule

The historical environment metadata is hereby marked **UNRESOLVED**.

1. This Charter does not select Linux or M3 Mac as the definitive historical environment.
2. Both observations are recorded with their respective sources.
3. The evidence is insufficient because no archived page snapshot, HTTP capture, or WARC record is currently pinned for either claim.
4. Disputed environment metadata must NOT be used as a verified benchmark condition in any report, ranking, or claim.
5. Historical timing values must NOT be altered based on environment assumptions.
6. The separation between `/languages/` and `/languages2/` datasets is preserved; they must never be merged.
7. Resolution of this conflict is an R0 evidence-collection deliverable, not a Charter presupposition.

---

## 17. External References & Source Citations

The following external and internal references form the documented foundation of this Charter:

### 17.1 Historical Benchmark Publication (`/languages/`)
- **URL:** `https://benjdd.com/languages/`
- **Directly Documented Statements:** Initial benchmark comparison page; timing performed via `/usr/bin/time`, lowest of 3 runs recorded; execution platform identified as Apple M3 MacBook Pro 16 GB.
- **Previously Reported Observations:** Prior investigations (RPR v0.3 §2.1) documented this page as historical context only, not the origin of tabular performance metrics in RPR.
- **Unverified Claims:** Exact historical source commits, compiler driver flags, and execution environment isolation remain unverified.
- **Outstanding Evidence Requirements:** Pinned commit SHA, toolchain version lock, build script verification, and reproducible timing methodology.

### 17.2 Hyperfine Comparative Benchmark Publication (`/languages2/`)
- **URL:** `https://benjdd.com/languages2/`
- **Directly Documented Statements:** Source of external comparative metrics; timing performed using Hyperfine; records 3 runs with mean, standard deviation, and min-max range; benchmark input stated as `40`.
- **Previously Reported Observations:** RPR v0.3 §2.2 documented this page as the sole source of historical performance numbers. Conflicting observations exist regarding platform metadata: publication text notes M3 MacBook Pro, while prior investigation notes reported x86_64 Linux.
- **Unverified Claims:** Hardware/OS target platform, exact Hyperfine flags (including `--warmup` iterations), compiler flags for C, Rust, and Zig, and per-workload input parameter binding remain unverified external claims.
- **Outstanding Evidence Requirements:** Archived HTTP capture/WARC snapshot, exact commit SHA mapping, hardware topology confirmation, and independent verification.

### 17.3 Upstream Benchmark Repository
- **URL:** `https://github.com/bddicken/languages`
- **Directly Documented Statements:** Public GitHub repository containing benchmark source implementations across various languages.
- **Previously Reported Observations:** Branch `main` contains current workload code; parameter `40` observed in source files.
- **Unverified Claims:** Upstream `main` commits are not cryptographically pinned to the published results on `benjdd.com/languages2/`. Upstream source code is classified as CANDIDATE, not VERIFIED.
- **Outstanding Evidence Requirements:** Cryptographic pinning of the exact historical commit matching the publication date, SHA-256 source payload verification, and independent QA recalculation.

### 17.4 Internal RANCAGE Project Specifications
- **`PROJECT_STATUS.md`:** Governs Stage 0 freeze, current status baselines, and milestone definitions.
- **`AGENTS.md`:** Defines agent role separation, non-negotiable governance invariants, and change control rules.
- **`SPEC.md`:** Defines RANCAGE language foundation, primitive types, AST, and IR 0.1/0.2 specification.
- **`ROADMAP.md`:** Defines release rules, version roadmap, and pre-implementation boundaries.
- **`IMPLEMENTATION_DECISION.md`:** Documents Python reference implementation architecture and standalone distribution rules.

*Citation Invariant:* No external web page snapshot, HTTP response, or WARC archive is currently pinned or archived within this repository. All external benchmark numbers remain unverified external claims until resolved through the R0 research workflow. Historical source provenance (F-01 / A-01) remains UNRESOLVED.

---

## 18. Final Document Disposition & Governance Invariant

### 18.1 Governance Invariants
1. **Proposal Nature:** This Charter is a specification and research proposal; it does NOT constitute an active execution authorization.
2. **Review Status:** `READY FOR AUDITOR REVIEW` does not signify Owner approval. Formal review and audit sign-off are external prerequisites.
3. **Evidence Collection Gate:** `APPROVED FOR OWNER REVIEW` does not authorize evidence collection. Evidence collection requires explicit Owner sign-off on ODR-01 and ODR-02.
4. **Milestone Boundaries:** Successful completion of RPR-R0 does not automatically authorize R1. R1 and Stage 1 remain separately unauthorized and require independent proposals, auditor review, and Owner authorization.
5. **Stage 0 Baseline Freeze:** The Stage 0 codebase (RANCAGE 0.2.0a1, commit `03c6ec15b31eeddf8210223c32ca98793abe4222`, tag `v0.2.0a1`) is CLOSED / FROZEN. This Charter itself is not part of the frozen Stage 0 code baseline.
6. **Provenance Blocker:** Historical benchmark provenance (Finding F-01 / A-01) remains OPEN and HIGH BLOCKER until physical evidence resolves it.
7. **Owner Authority:** Final milestone acceptance and authorization decisions belong exclusively to the Owner.

### 18.2 Document Disposition Classification
This Charter must be classified under exactly one formal disposition at any time. Hybrid verdicts are strictly prohibited:

| Disposition | Operational Meaning |
|---|---|
| `APPROVED FOR OWNER REVIEW` | The Charter document is complete, internally consistent, validated against all governance invariants, and formally submitted for Owner review. |
| `NEEDS REVISION` | The Charter contains structural, semantic, or governance defects that must be remediated prior to Owner consideration. |
| `BLOCKED` | The Charter cannot proceed due to unresolved external blockers, governance contradictions, or policy conflicts. |

### 18.3 Current Document Status
**Status:** `PROPOSAL — READY FOR AUDITOR REVIEW`

No independent Auditor approval is claimed, assumed, or implied by the authorship of this proposal. Formal audit review and QA determinism verification must be conducted independently.

### 18.4 Document Revision History

| Version | Date | Author | Summary of Changes |
|---|---|---|---|
| 0.6 | 2026-11-16 | Architect | Initial Charter proposal draft; audited with findings (NEEDS REVISION). |
| 0.7 | 2026-11-17 | Developer | Targeted remediation: L/C namespaces, C-02 taxonomy, §16 metadata UNRESOLVED handling; audited with findings (NEEDS REVISION due to missing §17/§18 and §8.1 role contradiction). |
| 0.8 | 2026-11-17 | Architect | Final remediation: Restored §17 (External References & Source Citations) and §18 (Final Document Disposition & Governance Invariant); corrected C-10 cross-reference (§14, §15); resolved §8.1 Auditor search-execution contradiction; fixed §5 numbering (5.1, 5.2, 5.3) and §6 Markdown bold tags. |

---

**RANCAGE must prove performance improvements rather than merely claim them.**
