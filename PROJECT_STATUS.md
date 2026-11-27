# RANCAGE Project Status

**Status date:** 17 November 2026
**Repository:** `https://github.com/henxnomercy/rancage-language`
**Primary branch:** `main`
**Current frozen RANCAGE baseline:** `v0.2.0a1`
**Baseline commit:** `03c6ec15b31eeddf8210223c32ca98793abe4222`
**Historical NOVA tag:** `v0.1.0`
**Implementation language:** Python 3.10+
**Overall position:** Stage 0 is complete and frozen. Stage 1 and all subsequent implementation milestones remain unauthorized.

---

## 1. Executive Summary

RANCAGE has completed its Stage 0 language foundation and published the corresponding `v0.2.0a1` baseline to the `main` branch and Git tag. The baseline establishes a working lexer, parser, static type checker, compiler, JSON-based RANCAGE-IR, bounded reference virtual machine, and command-line workflow.

The project is now in a post-Stage-0 planning and governance phase. Work is organized into three distinct tracks:

1. **Core Language Development** — planning the next language and toolchain capabilities. Stage 1 has not started and is not authorized.
2. **Performance Research** — establishing trustworthy benchmark provenance and measurement methodology through the proposed RPR-R0 milestone. RPR-R0 has not been authorized.
3. **Strategic Development** — reconciling the long-term language identity and feature priorities with the capabilities already delivered in Stage 0.

The immediate project priorities are to maintain the frozen baseline, reconcile this status document with the actual repository, complete the RPR-R0 Charter review, and obtain explicit owner decisions before starting new work.

## 2. Version and Baseline Policy

### 2.1 Historical baseline

- `v0.1.0` is retained as the historical NOVA baseline.
- The published `v0.1.0` tag must not be modified or repurposed.
- Historical NOVA-IR compatibility is read-only; it does not redefine the current RANCAGE baseline.

### 2.2 Current RANCAGE baseline

- `v0.2.0a1` is the frozen Stage 0 RANCAGE baseline.
- Baseline commit: `03c6ec15b31eeddf8210223c32ca98793abe4222`.
- The annotated `v0.2.0a1` tag and `main` commit were pushed to `origin`.
- Stage 0 is **CLOSED / FROZEN**.
- Do not amend, rewrite, or move the frozen baseline tag. Future development must proceed through new reviewed commits and separately approved milestones.

The historical NOVA `v0.1.0` and RANCAGE `v0.2.0a1` are distinct references. The former is not the current Stage 0 baseline.

## 3. Core Language Development

### 3.1 Stage 0 — Language Foundation

**Status: COMPLETE / CLOSED / FROZEN**
**Baseline: `v0.2.0a1`**

| Milestone | Scope | Status |
|---|---|---|
| M0.1 | Lexer and AST | COMPLETE |
| M0.2 | Parser and Type Checker | COMPLETE |
| M0.3 | Compiler and IR | COMPLETE |
| M0.4 | Virtual Machine | COMPLETE |
| M0.5 | Integration and Stage 0 baseline | COMPLETE |

### 3.2 Implemented capabilities

The frozen Stage 0 baseline includes:

- Lexer, parser, AST, and static type checker.
- Functions, variables, conditions, and `while` loops.
- Static types, nullable types, and nested collection types.
- Dynamic lists and list mutation/access operations.
- Maps/dictionaries and map mutation/access operations.
- Records/record instances and field access/mutation.
- Compiler from AST to RANCAGE-IR 0.2.
- Read-only compatibility support for historical RANCAGE-IR 0.1 and NOVA-IR 0.1 inputs where documented.
- JSON-based, stack-oriented RANCAGE-IR representation.
- Bounded reference Virtual Machine implemented in Python.
- Basic runtime intrinsics, including collection, string, and character operations.
- CLI commands: `check`, `build`, `run`, `repl`, `targets`, and version reporting.
- Canonical `.cage` source and `.rcb` bytecode file extensions.
- `cage` / `cage.exe` command-line executable, with `rancage` retained as an alias.
- Golden-path integration coverage across lexer, parser, type checker, compiler, IR, and VM.

### 3.3 Runtime safety boundaries

The reference VM includes explicit runtime controls, including:

- Instruction execution budget (`MAX_STEPS`).
- Call-depth limit (`MAX_DEPTH`).
- Collection and string size limits.
- Bounded integer validation and finite floating-point checks.
- Runtime bounds checks and null handling.
- Cumulative logical allocation accounting.
- No VM instructions for direct host filesystem, network, process, or general OS access; output is exposed through an injected host callable.

**Important limitations:**

- The VM is an in-process Python runtime, not an OS-level isolated sandbox.
- Logical allocation units are deterministic accounting units; they are not measurements of physical RAM, RSS, or actual heap bytes.
- These controls do not establish hardened isolation against hostile native code or compromise of the host process.

### 3.4 Stage 0 verification evidence

- Final Stage 0 QA suite: **74/74 tests passed**.
- Python 3.10.11: 74/74 passed.
- Python 3.11.9: 74/74 passed.
- Python 3.14.6: 74/74 passed.
- Python 3.15.2: 74/74 passed.
- Clean-checkout test run: 74/74 passed.
- Windows 10 x64: verified.
- CLI source and `.rcb` workflows were checked against the `hello`, `control_flow`, and `functions` examples.
- Linux and macOS were not verified in the Stage 0 test matrix.

These results establish the tested Python/Windows baseline. They do not establish native compilation, self-hosting, hardened OS isolation, or production support for other operating systems.

### 3.5 Stage 1 — Language Evolution

**Status: NOT STARTED / NOT AUTHORIZED**

Stage 1 does not yet have an approved feature specification or implementation sequence. The following are candidate areas for architecture research and owner prioritization, not approved tasks:

- Structured error handling, potentially using `Result[T, E]` or an equivalent design.
- A practical module system with import/export and namespace rules.
- `for` loops and range syntax.
- Expanded string APIs and standard library design.
- Enums and sum types.
- Further generic type-system capabilities.
- Improved diagnostics and source-location reporting.
- Toolchain usability and packaging improvements.

Lists, maps, records, nullable types, and the Stage 0 VM/IR foundations already exist. They must not be listed as wholly unimplemented features.

## 4. Packaging, CLI, and Publication

### 4.1 CLI and Windows preview

The project has a Windows standalone packaging path using PyInstaller one-file and one-folder builds. The supplied project status records a successful Windows x64 GitHub Actions preview artifact and maintainer smoke tests on Windows without a separate Python installation.

The recorded smoke tests covered:

- `--version`.
- Source `check` and `run`.
- Bytecode `build` and `run`.
- The three example programs: `hello`, `control_flow`, and `functions`.

These are preview workflow checks. They do not establish an installer, updater, code signing, hardened sandbox, bytecode encryption, anti-tamper, or support for other operating systems.

### 4.2 Repository publication

- Repository identity is `rancage-language`.
- The RANCAGE/CAGE identity migration was merged into `main`.
- Stage 0 commit `03c6ec15b31eeddf8210223c32ca98793abe4222` was pushed to `origin/main`.
- Annotated tag `v0.2.0a1` was pushed and its peeled commit target was verified.
- The historical `v0.1.0` tag remains unchanged.

A GitHub Release page/object is distinct from a Git tag. Its publication status is not asserted by this document.

### 4.3 Publication and security checklist

The earlier publication checklist recorded the repository rename, migration, package-author metadata update, review of reachable commit author metadata, common-secret-pattern review of the Git history bundle, removal of the obsolete `nova.cmd` launcher from the working tree, selection of the hybrid licensing model, and review of publication/security guidance.

Items requiring separate current verification before any further public-release declaration:

- GitHub private vulnerability reporting configuration.
- Final state of any remaining publication-only local changes.
- Whether a GitHub Release has been created for `v0.2.0a1`.

The Stage 0 baseline push and tag publication are complete; the older generic checklist item saying that the Stage 0 commit/push is still pending is obsolete.

## 5. Licensing Status

**Selected model: hybrid licensing.**

- RANCAGE compiler/runtime core is proprietary under the project-specific terms.
- Only files explicitly designated as SDK materials are intended to be under the MIT license.
- The current `sdk/` directory contains a draft extension contract; it is not a stable external ABI or production SDK.
- The project-specific proprietary terms are a maintainer-prepared draft and have not been reviewed by an Indonesian intellectual-property lawyer.
- The core license is intended to allow use of an unmodified official CAGE release, including commercially, to create and distribute RANCAGE programs without royalties.
- Bundling or redistributing RANCAGE Core requires separate permission.

See `LICENSE` and the applicable files under `licenses/` for the precise intended scope. Do not describe the SDK contract as stable until it has been separately reviewed and approved.

## 6. Performance Research — RANCAGE Performance Roadmap (RPR)

### 6.1 RPR proposal status

**RPR proposal v0.3: CONDITIONAL APPROVAL / DRAFT ONLY**

The proposal is a research plan, not an implementation authorization. The principal unresolved blocker is F-01/A-01: the historical benchmark source and its relationship to the published timing figures have not been pinned and independently reproduced.

The research has identified the following evidence limitations:

- Published historical numbers are not independently reproduced by RANCAGE.
- The currently discovered upstream C source on `main` is only a **CANDIDATE**, not the confirmed historical source used for publication.
- The meaning of input `40` must be established separately for each language/workload from the corresponding source and invocation. The meaning found in one C candidate must not be generalized to Rust or Zig.
- Historical source commit, source hashes, build flags, and complete commands remain unresolved unless independently established by archived evidence.
- Published timing figures must not be treated as RANCAGE targets, ranking claims, or proof of compatibility.

### 6.2 RPR-R0 — Performance Research Foundation & Benchmark Provenance

**Status: PROPOSED / NOT AUTHORIZED**

RPR-R0 is intended to establish the provenance, workload definitions, archive integrity, and measurement-method documentation needed before later performance work.

Charter history:

| Charter version | Outcome |
|---|---|
| v0.1 | Initial proposal |
| v0.2 | Expanded responsibilities, archive strategy, and A1/A2 acceptance criteria |
| v0.3 | Tightened evidence thresholds and search-completeness requirements |
| v0.4 | Added operational evidence classifications and workload-validation boundaries |
| v0.5 | Added statistical threshold and related remediation; independent review identified remaining issues |
| v0.6 | Proposed next consolidation; not yet approved or completed |

**Latest known Charter review:** v0.5 was assessed as **REVISE**. It is not ready for owner approval. The recommended v0.6 consolidation must restore and reconcile all required sections, resolve the remaining statistical and governance issues, and then undergo independent Auditor review.

Proposed RPR-R0 work packages:

1. Evidence collection infrastructure and role assignment.
2. Historical source pinning.
3. Workload-shape and source characterization.
4. Historical evidence archive and SHA-256 manifests.
5. Separate reproducibility status reporting: SOURCE PINNED, BUILD REPRODUCED, WORKLOAD VALIDATED, and TIMING REPRODUCED.
6. Statistical methodology documentation.

Proposed exit routes:

- **A1 — Historical source successfully pinned:** the core historical workloads have verified source provenance and their relationship to the publication is defensible.
- **A2 — Historical-reference-only:** if a sufficiently complete, documented search cannot recover the historical source, the owner may explicitly approve removal of compatibility claims and retention of the published numbers only as historical context.

Neither A1 nor A2 is approved yet. A2 must not be selected merely because one agent, session, or tool lacks access.

### 6.3 R0 boundaries

R0 is proposed as a read-only research and evidence-collection milestone. It does not authorize:

- Changes to RANCAGE source code or the frozen Stage 0 baseline.
- VM optimization or compiler changes.
- Typed IR implementation or Bounds Check Elimination.
- Native backend implementation or compiler rewrite.
- A RANCAGE benchmark harness.
- Benchmark timing runs.
- Runtime workload execution or build operations unless separately and explicitly authorized for a defined sub-scope.
- Statistical pilot execution.

The statistical pilot is intended to be a separate milestone requiring its own proposal, audit, QA, and owner authorization.

### 6.4 R1 and later performance phases

| Phase | Intended purpose | Status |
|---|---|---|
| R1 | Performance baseline using approved workloads and methodology | NOT STARTED / NOT AUTHORIZED |
| R2 | Profiling and bottleneck analysis | FUTURE PROPOSAL |
| R3 | Optimization research (e.g. Typed IR, bytecode optimization, BCE feasibility) | FUTURE PROPOSAL |
| R4 | Approved optimization implementation and verification | FUTURE PROPOSAL |

No optimizer, native backend, or compiler implementation technology is selected or authorized by the current RPR proposal.

## 7. Strategic Development Direction

**Status: INTERNAL REVIEW / DRAFT**
**Source document:** RANCAGE Roadmap Evaluation & Strategic Recommendations, dated 17 November 2026.

The strategic evaluation proposes five long-term identity pillars. These are strategic directions, not implemented features or approved implementation tasks.

### 7.1 Lightweight

- Small and efficient runtime.
- Low memory overhead.
- Fast startup.
- Minimal runtime dependencies.
- Standalone toolchain direction.

### 7.2 Safe — Security by Design

- Capability-based security.
- No ambient authority.
- Bounded execution and resource controls.
- Explicit host boundary.
- Safe defaults and auditable permissions.

The Stage 0 VM already has in-process execution limits and restricted host-facing instructions. A language-level capability/effect system and hardened OS isolation are not implemented.

### 7.3 Strong Language Semantics

- Static typing and explicit nullability.
- Defined error-handling semantics.
- Predictable runtime behavior.
- Reliable compiler diagnostics.
- Clear and testable language contracts.

### 7.4 Strict Multi-Target Semantic Guarantees

- One language specification across multiple execution targets.
- Backend conformance requirements.
- Explicitly isolated platform-specific behavior.
- Verifiable preservation of language semantics across backends.

No production multi-backend implementation is currently available.

### 7.5 Independent Ecosystem

- Independent compiler and runtime.
- Standalone toolchain.
- Standard library and module ecosystem.
- Long-term self-hosting direction.

Self-hosting and production multi-target backends remain future goals.

### 7.6 Feature priority candidates

The roadmap evaluation's original feature-gap assessment must be reconciled with Stage 0 before it is used for prioritization. In particular, lists, maps, and records are already implemented and must not be reported as missing.

Candidate areas for future design and owner prioritization include:

- Structured error handling (`Result[T, E]` or an equivalent design).
- Module/import/export system.
- `for` loops and range syntax.
- Expanded string methods and standard library.
- Enums and sum types.
- Further generic capabilities.
- Better diagnostics and source-location accuracy.
- Capability system and explicit host-boundary model.
- Backend semantic contracts.

No feature in this list is automatically approved for Stage 1.

## 8. Not Implemented or Not Yet Established

The following capabilities are not part of the frozen Stage 0 implementation or are not established as production-ready:

- Native machine-code generation.
- Self-hosting compiler.
- Production Android or iOS backend.
- Production WebAssembly backend.
- Roblox/Luau or other production backends.
- Language-level capability/effect enforcement.
- Hardened OS-level sandboxing.
- Production-grade module system and standard library.
- Mature structured error-handling system.
- `for` loop and range syntax.
- Code signing, updater, and installer.
- Bytecode encryption or anti-tamper mechanisms.
- Stable external SDK ABI.

The JSON-based IR representation is currently an explicit project format; its readability alone is not evidence of a defect or an approved reason to prioritize encryption or obfuscation.

## 9. Current Milestone and Work Status

| Track | Milestone / item | Status | Next gate |
|---|---|---|---|
| Core | Stage 0 / `v0.2.0a1` | CLOSED / FROZEN | Preserve baseline |
| Core | Stage 1 | NOT STARTED / NOT AUTHORIZED | Approved Stage 1 proposal |
| Performance | RPR proposal v0.3 | CONDITIONAL APPROVAL / DRAFT ONLY | Resolve provenance blocker and proposal review |
| Performance | Historical source investigation | INSUFFICIENT EVIDENCE | Authorized evidence collection |
| Performance | RPR-R0 Charter v0.5 | REVISE | Consolidated v0.6 and independent audit |
| Performance | RPR-R0 execution | PROPOSED / NOT AUTHORIZED | Owner approval of Charter and six decisions |
| Performance | R1 | NOT STARTED / NOT AUTHORIZED | Separate proposal and authorization |
| Performance | R2–R4 | FUTURE PROPOSAL | Depends on R1 results and owner approval |
| Strategy | Roadmap Evaluation | INTERNAL REVIEW / DRAFT | Reconcile feature status with Stage 0 |

## 10. Immediate Next Actions

1. **Consolidate project status:** verify this document against the repository and the frozen Stage 0 artifacts before treating it as authoritative.
2. **Complete RPR-R0 Charter v0.6:** restore all required sections from earlier Charter versions, correct cross-references, and resolve the outstanding statistical, workload-validation, role-separation, search-completeness, and compile-only authorization issues.
3. **Independent Charter audit:** use the RANCAGE Auditor in read-only mode. Do not ask Developer to implement anything before the Charter passes review.
4. **Owner decision:** review and explicitly approve or reject each RPR-R0 decision, including evidence-collection tooling, archive location, A1/A2 policy, benchmark warning text, workload-shape gate, and the separate statistical-pilot proposal.
5. **Only after approval:** begin the specifically authorized RPR-R0 evidence-collection scope.
6. **Keep core development planning separate:** reconcile the strategic feature list before preparing a Stage 1 proposal.

## 11. Governance and Working Rules

For implementation milestones:

**Architect → Owner Approval → Developer → Auditor → QA → Owner Sign-off**

For read-only research milestones:

**Architect → Owner Approval → Evidence Collection → Auditor → QA → Owner Sign-off**

Project rules:

- No implementation without explicit owner authorization.
- No performance claim without appropriate, reproducible evidence.
- No modification or rewriting of a frozen baseline tag.
- Every milestone must have defined scope and acceptance criteria.
- Auditor and QA findings must be independently reviewable.
- Roo Code configuration files (`.roo/` and `.roomodes`) are local tooling artifacts and must not be committed to the project repository.
- Distinguish implemented, partially implemented, proposed, research-required, and unverified capabilities.

## 12. Project Principles

RANCAGE is developed around three core principles:

**Lightweight. Safe. Strong.**

The long-term objective is an independent programming language with an efficient runtime, security designed into the language and host boundary, strong and predictable semantics, and verifiable portability across execution targets.

RANCAGE must demonstrate its quality through implementation, testing, independent review, and reproducible evidence—not unsupported claims.
