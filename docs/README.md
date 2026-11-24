# RANCAGE Documentation Index

This directory contains the full documentation set for the RANCAGE project.
All paths are relative to the repository root.

## Structure Overview

| Category | Contents |
|---|---|
| `architecture/` | Milestone Stage 0 design documents (M0.2–M0.5). Describes lexer, parser, type system, compiler, and virtual machine implementation. |
| `audits/sh01/WP-A/` | Independent Stage 0 audit work package A: provenance, reconciliation, remediation, formalization, and closure reports. |
| `internal/` | Operational guides (e.g., GitHub upload guide in Indonesian). |
| `project/` | Build and packaging instructions (PyInstaller Windows), standalone usage, and the closed Stage 0 proposal. |
| `releases/` | Release checklist for stable tagging. |
| `research/` | Unapproved proposals, charters, decisions, and feasibility studies. These documents represent ideas under review and are not commitments. |

## Architecture (`architecture/`)

- [M0.2-ARCHITECTURE.md](architecture/M0.2-ARCHITECTURE.md) — Lexer, parser, and AST.
- [M0.3-ARCHITECTURE.md](architecture/M0.3-ARCHITECTURE.md) — Type system and checker.
- [M0.4-ARCHITECTURE.md](architecture/M0.4-ARCHITECTURE.md) — Compiler and RANCAGE-IR 0.2.
- [M0.5-ARCHITECTURE.md](architecture/M0.5-ARCHITECTURE.md) — Virtual machine and execution boundaries.

## Audits (`audits/sh01/WP-A/`)

- [PROVENANCE.md](audits/sh01/WP-A/PROVENANCE.md) — Audit scope and source preservation.
- [SH-01-WP-A-AST-RECONCILIATION.md](audits/sh01/WP-A/SH-01-WP-A-AST-RECONCILIATION.md) — AST reconciliation.
- [SH-01-WP-A-REMEDIATION.md](audits/sh01/WP-A/SH-01-WP-A-REMEDIATION.md) — Remediation actions.
- [SH-01-WP-A-I4-FORMALIZATION.md](audits/sh01/WP-A/SH-01-WP-A-I4-FORMALIZATION.md) — Formalization of finding I4.
- [SH-01-WP-A-CLOSURE.md](audits/sh01/WP-A/SH-01-WP-A-CLOSURE.md) — Work package closure.

## Internal (`internal/`)

- [GITHUB_UPLOAD_GUIDE_ID.md](internal/GITHUB_UPLOAD_GUIDE_ID.md) — GitHub upload guide (Indonesian).

## Project (`project/`)

- [BUILDING-STANDALONE.md](project/BUILDING-STANDALONE.md) — PyInstaller Windows x64 build procedure.
- [README-STANDALONE.md](project/README-STANDALONE.md) — Standalone bundle usage.
- [history/STAGE-0-PROPOSAL.md](project/history/STAGE-0-PROPOSAL.md) — Closed Stage 0 proposal.

## Releases (`releases/`)

- [RELEASE-CHECKLIST.md](releases/RELEASE-CHECKLIST.md) — Pre-tag checklist.

## Research (`research/`)

**⚠️ These documents are under review and not approved for implementation.**

- [ROADMAP-EVALUATION.md](research/roadmap/ROADMAP-EVALUATION.md) — Roadmap alternatives.
- [SELF-HOSTING-FEASIBILITY.md](research/feasibility/SELF-HOSTING-FEASIBILITY.md) — Self-hosting feasibility study.
- [RPR-PROPOSAL.md](research/rpr/proposals/RPR-PROPOSAL.md) — RPR proposal (initial revision).
- [RPR-PROPOSAL-v0.2.md](research/rpr/proposals/RPR-PROPOSAL-v0.2.md) — RPR revision 0.2.
- [RPR-PROPOSAL-v0.3.md](research/rpr/proposals/RPR-PROPOSAL-v0.3.md) — RPR revision 0.3.
- [RPR-R0-CHARTER-PROPOSAL-v0.6.md](research/rpr/charters/RPR-R0-CHARTER-PROPOSAL-v0.6.md) — RPR-R0 charter rev. 0.6.
- [RPR-R0-CHARTER-PROPOSAL-v0.7.md](research/rpr/charters/RPR-R0-CHARTER-PROPOSAL-v0.7.md) — RPR-R0 charter rev. 0.7.
- [RPR-R0-CHARTER-PROPOSAL-v0.8.md](research/rpr/charters/RPR-R0-CHARTER-PROPOSAL-v0.8.md) — RPR-R0 charter rev. 0.8.
- [IMPLEMENTATION_DECISION.md](research/rpr/decisions/IMPLEMENTATION_DECISION.md) — Implementation decision record.
- [RPR-R0-OWNER-DECISION-RECORD.md](research/rpr/decisions/RPR-R0-OWNER-DECISION-RECORD.md) — Owner decision record for RPR-R0.
- [RPR-R0-EVIDENCE-COLLECTION-PLAN.md](research/rpr/evidence/RPR-R0-EVIDENCE-COLLECTION-PLAN.md) — RPR-R0 evidence collection plan (proposed, not authorized).

## Lokal only — not distributed

The following files are operator-local working context and are excluded from this index and from version control:

- `.roo/`
- `.roomodes`
- `AGENTS.md`
- `AI-HANDOFF.md`

These files exist on disk but are ignored by `.gitignore` and are not part of the distributed repository.

## Root-level normative documents

The following documents live at the repository root and are the normative reference for the project:

- [SPEC.md](../SPEC.md) — Grammar, types, semantics, RANCAGE-IR 0.2, VM boundaries.
- [ROADMAP.md](../ROADMAP.md) — Approved milestones and priorities.
- [PROJECT_STATUS.md](../PROJECT_STATUS.md) — Current status, baselines, and evidence.
- [CHANGELOG.md](../CHANGELOG.md) — Per-version change history.
- [SECURITY.md](../SECURITY.md) — Threat model and reporting.
- [CONTRIBUTING.md](../CONTRIBUTING.md) — Workflow and quality gates.
- [DEPENDENCIES.md](../DEPENDENCIES.md) — Runtime and build dependencies.
- [THIRD-PARTY-NOTICES.md](../THIRD-PARTY-NOTICES.md) — Third-party attributions.
- [LICENSE](../LICENSE) — Project license.
- [README.md](../README.md) — Repository entry point.
