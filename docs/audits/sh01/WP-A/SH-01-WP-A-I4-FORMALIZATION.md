# RANCAGE — SH-01 WP-A I4 Formalization

**Invariant:** I4 — Unique Field Name per RecordInit  
**Work Package:** WP-A — AST Inventory & Kind Registry Reconciliation  
**Current WP-A outcome:** CLOSED — ACCEPTED (based on the final independent-audit result reported in the conversation)  
**Provenance:** Persisted from I4 formalization content supplied in the ChatGPT conversation. This file was reconstructed from that supplied content; it has not been independently compared with the Windows workspace or repository files.

---

## 1. Formal Definition: Invariant I4 (Unique Field Name per RecordInit)

**I4 — Unique Field Name per RecordInit**

For every `RecordInit` node \(R\), let \(F_R\) be the collection of its direct `FieldInit` children. Let:

\[
N(F_R) = \{f.name \mid f \in F_R\}
\]

be the set of field names defined in those children.

The invariant \(I4\) requires that the cardinality of \(N(F_R)\) is equal to the cardinality of \(F_R\).

### Mathematical Formulation

\[
\forall R \in \text{Nodes},\; \text{kind}(R)=K21
\implies
\left|\{f.name \mid f \in \text{children}(R)\}\right|
=
|\text{children}(R)|
\]

This formulation assumes that I1 establishes that every direct child of a `RecordInit` relevant to this invariant is a `FieldInit`. The collection \(F_R\) is understood as the direct-child collection, with multiplicity preserved for counting; it must not be reduced to a set before duplicate-reference checks are performed.

### Scope and Identifier Semantics

- **Scope:** Exclusive to the `fields` collection of a single `RecordInit` instance.
- **Identifier equality:** Names are compared using case-sensitive UTF-8 string equality, as specified by the submitted formalization.
- **Independence:** Uniqueness is scoped per `RecordInit` instance; different `RecordInit` instances (even of the same named record) are independent.

The case-sensitive UTF-8 equality statement is the submitted design rule. Its correspondence to the actual lexer, parser, storage, and identifier normalization behavior must be supported by the relevant implementation/specification evidence when this artifact is used for an implementation decision.

## 2. Validation Responsibility

I4 is classified as **Structural/Semantic Interface Validation**.

- It requires structural node traversal to extract names from direct `FieldInit` children.
- It is a well-formedness requirement that must be satisfied before semantic type checking proceeds.
- **Proposed placement:** Compiler AST-Well-Formedness phase, before type checking.

Regardless of phase placement, a `RecordInit` with duplicate field names must not be accepted as a valid `RecordInit`.

I4 establishes uniqueness only. It does not, by itself, establish that every declared record field is present, that no unknown field is supplied, or that each field value has the correct type. Those are separate semantic checks.

## 3. Counterexamples

| Scenario | Definition | Result | Responsible Invariant |
| :--- | :--- | :--- | :--- |
| Unique fields | `RecordInit { x: 1, y: 2 }` | VALID under I4 | I4 |
| Duplicate names | `RecordInit { x: 1, x: 2 }` | INVALID | I4 |
| Empty RecordInit | `RecordInit { }` | VALID under I4 (vacuously satisfied) | I4 |
| Shared FieldInit | Two `RecordInit` nodes use one `FieldInit` node | INVALID | I2 — Parent Pointer Agreement / unique ownership |
| FieldInit in Binary | `Binary (1 + FieldInit {x: 1})` | INVALID | I1 — Parent Kind Restriction |

Additional distinctions:

- Two different `FieldInit` nodes with identical names under the same `RecordInit` violate I4.
- Repeating the same child-node reference in one parent's child collection is a structural duplicate-reference problem and must be handled by collection/tree integrity validation, independently of name uniqueness.
- Two different `RecordInit` instances may each contain a field named `x`; I4 does not prohibit this across instances.

## 4. Registry Clarification

- **Current active kind count:** 25 (K01–K21, K23–K25, K32).
- **Historical context:** The “27-kind target” referenced in earlier proposals is acknowledged as historical design/documentation debt. It does not represent a functional requirement for the current baseline.
- No K22 or K26/K27 identifiers are allocated as active kinds by this formalization.

## 5. Auditor Consistency Note

The previous Auditor review correctly identified I4 as missing from the formal definitions. This document supplies the explicit invariant definition.

The previous review also contained wording that could be read as saying I4 was already satisfied while simultaneously stating that it was not formally defined. The final independent re-audit occurred after this formalization and reported I4 as verified and robust. The earlier wording should be understood in that historical context; the final audit verdict is the controlling WP-A outcome.

## 6. Audit Acceptance Criteria

- Inclusion of this formal I4 definition.
- Verification of `RecordInit` direct-child traversal in the AST representation/validation design.
- Consistent application of I4 across all `RecordInit` instances.
- Distinction between duplicate field names and duplicate child-node references.
- Evidence that identifier equality behavior matches the language's established identifier rules.

## 7. Status

**WP-A I4 formalization:** COMPLETE.  
**Final independent WP-A audit:** ACCEPTED (as reported in the conversation).  
**WP-A:** CLOSED — ACCEPTED.  
**WP-B:** Requires a separate task authorization.  
**Stage 1 gate:** UNSIGNED.  
**Implementation authorization:** Not granted by this document.
