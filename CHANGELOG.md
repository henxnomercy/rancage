# Changelog

## 0.1.0-alpha.1 — Clean-slate Stage 0 baseline

- Published the first clean-slate snapshot in the new `henxnomercy/rancage`
  repository with one root commit and no imported predecessor history.
- Reset the public package/release sequence to `0.1.0a1` (Python package and
  CLI version output); published the annotated Git tag
  `v0.1.0-alpha.1`.
- Published the completed and frozen Stage 0 language foundation while
  retaining the RANCAGE 0.1 syntax and semantics baseline.
- Included the lexer, parser, AST, static type checker, compiler, JSON-based
  RANCAGE-IR, bounded Python reference VM, CLI, examples, documentation, and
  tests.
- Removed acceptance of the obsolete NOVA-IR legacy format. The VM accepts
  the supported RANCAGE-IR format versions documented by the implementation
  and tests.
- Included the Windows standalone packaging pipeline and its bundle smoke
  tests.
- Verified the clean-slate test suite at 134/134 passing.

## Historical pre-clean-slate notes

The predecessor repository used the labels `v0.1.0` and `v0.2.0a1` /
`0.2.0-alpha.1` for earlier development history, including Windows standalone
packaging work. Those labels belong to the privately retained predecessor
repository; they are not releases or tags in this clean-slate repository and
do not define its current version sequence.