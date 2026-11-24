# RANCAGE Roadmap

## Published baseline

### v0.1.0-alpha.1 — Clean-slate Stage 0 baseline

- Published in the new `henxnomercy/rancage` repository as a single root
  commit; predecessor Git history was not imported.
- Contains the completed and frozen Stage 0 language foundation.
- Uses Python package version `0.1.0a1`; the CLI reports
  `RANCAGE 0.1.0a1`.
- Preserves the RANCAGE 0.1 language syntax and semantics baseline.
- Includes the Python reference compiler, RANCAGE-IR compiler, bounded VM,
  CLI, examples, documentation, and 134-test suite.
- Includes the Windows standalone packaging pipeline; this is a packaged
  Python application, not a native compiler or self-hosted toolchain.

## Current development status

Stage 0 is **COMPLETE / CLOSED / FROZEN**.
Stage 1 is **NOT STARTED / NOT AUTHORIZED**.
The RANCAGE Performance Roadmap (RPR) and its RPR-R0 foundation remain
**PROPOSED / NOT AUTHORIZED**.

No later version number or implementation milestone is committed by this
roadmap. Future work requires a separate proposal, acceptance criteria,
independent review, QA, and explicit owner authorization.

## Future planning candidates — not approved or version-assigned

### Language evolution

Candidate areas for design and owner prioritization include:

- Structured error handling, potentially using `Result[T, E]` or an
  equivalent design.
- A practical module/import/export system and namespace rules.
- `for` loops and range syntax.
- Expanded string APIs and standard library design.
- Enums and sum types.
- Further generic type-system capabilities.
- Improved diagnostics and source-location reporting.
- Toolchain usability and packaging improvements.

Lists, maps, records, nullable types, and the Stage 0 VM/IR foundations are
already implemented and must not be listed as wholly missing features.

### Performance research

RPR-R0 is proposed as a read-only research and evidence-collection milestone.
It is not authorized. Its purpose, acceptance gates, and outstanding Charter
review issues are recorded in `PROJECT_STATUS.md` and the RPR documents.
No optimization implementation, benchmark timing run, native backend, or
compiler rewrite is authorized by the current status.

### Distribution and platform research

The Windows standalone packaging path exists. Further distribution hardening,
other operating-system packages, WebAssembly, Android integration, and native
backends require platform-specific feasibility work and independent build and
conformance evidence before support is claimed.

### Long-term — self-hosting

- Mature the language enough to express compiler data structures and
  algorithms.
- Design and implement a RANCAGE compiler in RANCAGE only after the required
  language features and validation gates are approved.
- Bootstrap using the existing Python reference compiler, then compare outputs
  and run conformance tests.

## Release rule

A planned target is not a supported target. Each platform must build and pass
its own smoke/conformance tests before it is advertised as supported. Every
new release version must be explicitly assigned and approved; version numbers
must not be inferred from this roadmap.