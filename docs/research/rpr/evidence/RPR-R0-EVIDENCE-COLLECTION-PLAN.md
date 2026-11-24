# RPR-R0 Evidence Collection Plan

**Document:** RPR-R0 Evidence Collection Plan  
**Version:** 1.0  
**Date:** 2026-11-17  
**Status:** OPERATIONAL SPECIFICATION — EXECUTION READY  
**Governing Authority:** RPR-R0 Charter Proposal v0.8 (§14), RPR-R0 Owner Decision Record (ODR-01..ODR-07)  
**Authorized External Archive Root:** `F:\Project\RANCAGE-research-evidence\RPR-R0\`  

---

## 1. Purpose & Scope Boundaries

This document defines the execution-ready operational plan for preliminary evidence collection under RPR-R0.

Following formal ratification of ODR-01 through ODR-05 in [`../decisions/RPR-R0-OWNER-DECISION-RECORD.md`](../decisions/RPR-R0-OWNER-DECISION-RECORD.md), the Evidence Collector is authorized to execute activities **ACT-01, ACT-02, ACT-03, and ACT-04**.

**Scope Boundaries:**
- **In Scope:** Discovering, retrieving, archiving, hashing, and documenting historical benchmark publications and repository sources related to `benjdd.com/languages/`, `benjdd.com/languages2/`, and `github.com/bddicken/languages`.
- **Strictly Out of Scope:**
  - Zero execution of third-party compiler drivers (`gcc`, `clang`, `rustc`, `zig`) (ACT-06 PROHIBITED; ACT-10 NOT AUTHORIZED).
  - Zero execution of foreign or compiled binaries (ACT-07 PROHIBITED).
  - Zero modification of RANCAGE Stage 0 source code, tests, or configuration (ACT-08 PROHIBITED).
  - Zero benchmark timing runs, profiling, or warmup iterations (ACT-09 PROHIBITED).
  - Zero execution of statistical pilot runs (ODR-06 isolated).
  - Zero creation of files inside the RANCAGE repository directory `F:\Project\RANCAGE\`.

---

## 2. Role Responsibilities & Operational Boundaries

| Role | Operational Scope in Evidence Collection | Explicit Prohibitions |
|---|---|---|
| **Evidence Collector** | Executes approved network fetches (ACT-01) and git clones (ACT-02). Stores artifacts in external archive (ACT-04). Computes initial `MANIFEST.sha256` (ACT-03). Maintains `SEARCH_LOG.md` adhering to 14 categories and 8 fields. | Cannot author charter text, assess exit criteria, act as sole QA verifier of gathered evidence, execute compiler drivers, run binaries, or search outside approved scope. |
| **QA Engineer** | Independently recalculates all SHA-256 digests directly from cold archive files. Checks manifest completeness and determinism. Produces QA Determinism Verification Report. | Cannot alter recorded benchmark metrics, waive hash mismatches, or collect primary evidence. |
| **Auditor** | Independently reviews `SEARCH_LOG.md` against 14 mandatory search categories (§8.1). Checks adequacy of explanations for unsuccessful searches. Examines role independence. Produces Independent Auditor Review Report. | Cannot gather primary evidence, draft proposals, execute code modifications, or execute searches (the Auditor does not act as Evidence Collector). |
| **Architect** | Performs workload-shape characterization (ODR-05). Analyzes loop structures, algorithmic complexity, and input `40` parameter bindings. Prepares technical conclusions. | Cannot collect primary evidence, conduct independent compliance audits of own work, or execute benchmarks. |
| **Owner** | Reviews final evidence packages, QA reports, and Auditor reports. Formally accepts Route A1 or Route A2 exit. Authorizes future milestone proposals. | Cannot modify raw hash logs, evidence manifests, or audit verdicts. |

---

## 3. External Archive Architecture & Storage Format

The authorized archive root is `F:\Project\RANCAGE-research-evidence\RPR-R0\` (authorized under ODR-02). All files written under ACT-04 must reside within this isolated directory tree.

```
F:\Project\RANCAGE-research-evidence\RPR-R0\
├── html\
│   ├── benjdd-languages-2026.html
│   ├── benjdd-languages-2026.headers.txt
│   ├── benjdd-languages2-2026.html
│   ├── benjdd-languages2-2026.headers.txt
│   └── wayback\
│       ├── benjdd-languages-snapshots.json
│       └── [captured historical warc / html files]
├── git\
│   └── bddicken-languages\
│       ├── .git\
│       └── [worktree / mirror files]
├── workloads\
│   ├── c\
│   ├── rust\
│   └── zig\
├── logs\
│   ├── SEARCH_LOG.md
│   └── fetch-metadata.json
└── manifests\
    └── MANIFEST.sha256
```

**Storage Invariants:**
1. **Cold Isolation:** The archive is physically outside `F:\Project\RANCAGE\`.
2. **Immutability:** Once acquired, files must have read-only attributes applied.
3. **Flat Manifest:** `MANIFEST.sha256` in `manifests/` must index every file relative to the archive root.

---

## 4. Operational Activity Specifications (ACT-01 through ACT-04)

### ACT-01: Web Snapshot & Public URL Fetch
- **Objective:** Acquire exact static snapshots and HTTP response metadata of historical benchmark publication pages.
- **Target URLs:**
  1. `https://benjdd.com/languages/`
  2. `https://benjdd.com/languages2/`
  3. Internet Archive / Wayback Machine API endpoints for historical captures (2024–2026 timeframe).
- **Execution Inputs:** Pinned URL list, curl / wget parameters with full header logging, TLS certificate verification enabled.
- **Expected Outputs:**
  - Raw HTML documents saved in `html/`.
  - Full HTTP response headers (status codes, Server, Date, ETag, Last-Modified, Content-Length) saved alongside HTML in `.headers.txt`.
  - WARC files where supported.
- **Evidence Requirements:** UTC timestamp of request, HTTP 200 verification, source IP/domain resolution log, cryptographic hash of raw response payload.
- **Restrictions:** Zero execution of embedded client-side scripts; zero alteration of server response payloads.

### ACT-02: Git Clone of External Benchmark Repositories
- **Objective:** Acquire full version history and source tree of upstream benchmark repository.
- **Target Repository:** `https://github.com/bddicken/languages`
- **Execution Inputs:** Upstream git URL, git clone with `--no-checkout` or full mirror parameters, git log commands.
- **Expected Outputs:**
  - Full repository clone located in `git/bddicken-languages/`.
  - Complete git commit log from initial commit to HEAD (`logs/git-commit-history.log`).
  - Inventory of all historical tags, branches, and tree hashes (`logs/git-refs.log`).
  - Public fork network inventory (`logs/git-fork-network.log`).
- **Evidence Requirements:** Full 40-character commit SHAs, git tree hashes, commit author timestamps, commit message text.
- **Restrictions:** Zero execution of repository build scripts (`Makefile`, `cargo`, `build.zig`, shell wrappers); zero invocation of host compilers; zero modification of git history.

### ACT-03: SHA-256 Manifest Computation
- **Objective:** Compute deterministic cryptographic fingerprints for all gathered research assets.
- **Execution Inputs:** All files deposited into `F:\Project\RANCAGE-research-evidence\RPR-R0\`.
- **Expected Outputs:** `manifests/MANIFEST.sha256` generated strictly in the standard format:
  ```
  <64-hex-character-sha256>  <relative-path-from-archive-root>
  ```
- **Evidence Requirements:**
  - Generated using SHA-256 algorithm without salt.
  - Sorted lexicographically by relative path for deterministic diffing.
  - Must cover 100% of acquired files (zero omissions).
  - Subject to mandatory independent recalculation by QA Engineer before audit submission.
- **Restrictions:** Hashes must never be hand-edited or fabricated.

### ACT-04: File Writing to External Evidence Archive
- **Objective:** Safely persist research artifacts into the approved external storage location.
- **Execution Inputs:** File payloads produced by ACT-01, ACT-02, ACT-03, and `SEARCH_LOG.md`.
- **Expected Outputs:** Verified files written to `F:\Project\RANCAGE-research-evidence\RPR-R0\`.
- **Evidence Requirements:** Path verification ensuring all write targets reside inside the approved archive root.
- **Restrictions:** Absolute prohibition against writing into `F:\Project\RANCAGE\` or modifying Stage 0 repository files.

---

## 5. Explicit Prohibitions & Inactive Permissions

To ensure strict compliance with project governance, the following activities remain completely prohibited during evidence collection:

- **ACT-06 (Compiler Execution):** PROHIBITED. No compiler drivers may be run.
- **ACT-07 (Binary Execution):** PROHIBITED. No compiled or downloaded foreign binaries may be executed.
- **ACT-08 (Codebase Modification):** PROHIBITED. Stage 0 RANCAGE files remain frozen.
- **ACT-09 (Timing Runs):** PROHIBITED. No benchmark execution or timing measurement is authorized.
- **ACT-10 (Compile-Only Check):** NOT AUTHORIZED. ODR-07 is deferred by Owner; no syntax-only compiler validation may occur.
- **Statistical Pilot:** NOT AUTHORIZED. ODR-06 isolates the pilot to a separate future milestone.

---

## 6. A2 Search Completeness Checklist & Search Log Requirements

The Evidence Collector must exhaustively search and document all 14 categories defined in Charter §8.1:

### 6.1 Mandatory Search Categories
1. **Repository URLs:** Upstream repositories, official mirrors, author personal repositories, forks.
2. **Branches and Tags:** All active, historical, and archived branches/tags across the repository network.
3. **Full Git Commit History:** Complete commit logs, tree hashes, commit messages from root to HEAD.
4. **Source Implementations:** C, Rust, and Zig source files across all historical directory structures.
5. **README & Specifications:** Workload documentation, specifications, and explanatory notes across revisions.
6. **Changelogs & Release Notes:** Project release notes, tagged version changelogs, author announcements.
7. **Build Scripts:** Makefiles, shell scripts, cargo configurations, build.zig, or compiler driver scripts.
8. **Runner & Harness Scripts:** In-process harness drivers, execution scripts, and timing wrappers.
9. **Hyperfine Invocations:** Command-line invocations, argument strings, shell wrappers, parameter flags.
10. **Warmup Configurations:** Recorded warmup iteration counts, cache preparation steps, shell options.
11. **Historical Publication Pages:** Current and historical versions of `benjdd.com/languages/` and `benjdd.com/languages2/`.
12. **HTML / WARC Snapshots:** Complete page source, DOM structure, and associated stylesheet or script metadata.
13. **Internet Archive / Wayback Machine:** Historical crawls of publication URLs covering the 2024–2026 timeframe.
14. **External Discussions & Issues:** Issue tracker threads, pull request reviews, forum posts, and external commentary.

### 6.2 Search Log Record Schema (`SEARCH_LOG.md`)
Every entry in `logs/SEARCH_LOG.md` must record all eight mandatory fields:
1. `Item searched` (exact target, URL, commit query, or filename).
2. `Search date` (UTC timestamp).
3. `Tool / access method` (git command, web fetch, archive query, or manual browser).
4. `Result` (FOUND, NOT_FOUND, or PARTIAL).
5. `Artifact location and hash` (if found, relative path and SHA-256 digest).
6. `Reason when not found` (exact technical explanation).
7. `Alternative methods considered` (subsequent search attempts).
8. `Relationship to target workload` (functional mapping to historical published numbers).

*Rule:* An unavailable tool, connection timeout, or failed session cannot establish that source is unrecoverable.

---

## 7. Evidence Handoff & Independent Verification Sequence

```
[Evidence Collector]
  │  Executes ACT-01, ACT-02, ACT-04
  │  Maintains SEARCH_LOG.md (14 categories)
  │  Generates initial MANIFEST.sha256 (ACT-03)
  ▼
[QA Engineer]
  │  Independently recalculates SHA-256 digests from cold archive files
  │  Verifies MANIFEST.sha256 determinism & completeness
  │  Produces: QA Determinism Verification Report
  ▼
[Auditor]
  │  Audits SEARCH_LOG.md coverage across all 14 categories
  │  Verifies role separation & absence of execution violations
  │  Produces: Independent Auditor Review Report
  ▼
[Architect]
  │  Performs Workload-Shape Characterization (ODR-05)
  │  Evaluates input '40' binding and algorithmic equivalence
  │  Assigns Provenance Status (VERIFIED / CANDIDATE / UNRESOLVED)
  │  Produces: Workload Characterization & Provenance Report
  ▼
[Owner]
  │  Reviews verified evidence and independent reports
  │  Evaluates Route A1 criteria (Source Pinned) vs Route A2 criteria (Exhaustive search)
  │  Formally ratifies RPR-R0 Milestone Exit
```

---

## 8. Preservation of Unresolved Issues & Historical Contradictions

1. **Historical Commit Provenance (Finding F-01 / A-01):**
   - The historical commit SHA for the published C, Rust, and Zig figures remains **UNRESOLVED / CANDIDATE**.
   - Branch `main` of `bddicken/languages` must NOT be assumed to match published figures without cryptographic proof.
2. **Hardware / OS Environment Contradiction:**
   - `/languages/` records Apple M3 MacBook Pro 16 GB (`/usr/bin/time`).
   - `/languages2/` text states M3 MacBook Pro; prior internal notes reported x86_64 Linux.
   - This conflict is marked **UNRESOLVED**. The Evidence Collector must capture facts from publication snapshots and Wayback records without selecting either platform by assumption.
3. **Input Parameter Binding:**
   - The attribution of input parameter `40` to all language workloads remains an unverified publication assertion until confirmed in source files.

---

## 9. Execution Readiness & Handoff Sign-Off

This Evidence Collection Plan is complete, internally consistent, and fully aligned with Charter Proposal v0.8 and the Owner Decision Record.

Upon authorization from the repository Owner, the Evidence Collector may initiate ACT-01 through ACT-04.

---

**RANCAGE must prove performance improvements rather than merely claim them.**
