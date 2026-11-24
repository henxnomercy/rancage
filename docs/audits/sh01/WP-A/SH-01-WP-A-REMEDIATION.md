# RANCAGE — SH-01 WP-A Remediation

**Work Package:** WP-A — AST Inventory & Kind Registry Reconciliation  
**Artifact type:** Remediation record  
**Current WP-A outcome:** CLOSED — ACCEPTED (based on the final independent-audit result reported in the conversation)  
**Provenance:** Persisted from remediation content supplied in the ChatGPT conversation. This file was reconstructed from that supplied content; it has not been independently compared with the Windows workspace or repository files.

---

## 1. Remediation Summary

The remediation addressed the findings articulated during the independent review:

1. The earlier claim of a 27-kind registry was inconsistent with the current AST inventory.
2. `Name`, `ListLiteral`, and `MapLiteral` had been omitted from earlier mapping material.
3. The formal parent-child constraint for `FieldInit` (K32) within `RecordInit` (K21) was missing.

The corrected registry contains **25 active kind identifiers**.

## 2. Corrected Kind Registry (Proposed and Reconciled)

| Kind ID | Kind Name | Associated AST Class(es) | Status | Child-Slot Definition | Parent Restriction |
| :--- | :--- | :--- | :--- | :--- | :--- |
| K01 | Program | `Program` | ACTIVE | `functions`, `records` | Root only |
| K02 | Function | `Function` | ACTIVE | `params`, `body` | `Program` |
| K03 | Param | `Param` | ACTIVE | — | `Function` |
| K04 | FieldDecl | `FieldDecl` | ACTIVE | — | `RecordDecl` |
| K05 | RecordDecl | `RecordDecl` | ACTIVE | `fields` | `Program` |
| K06 | Let | `Let` | ACTIVE | `value` | `Stmt` list |
| K07 | Assign | `Assign` | ACTIVE | `value` | `Stmt` list |
| K08 | FieldAssign | `FieldAssign` | ACTIVE | `target`, `value` | `Stmt` list |
| K09 | IndexAssign | `IndexAssign` | ACTIVE | `target`, `index`, `value` | `Stmt` list |
| K10 | Return | `Return` | ACTIVE | `value` | `Function` body |
| K11 | ExprStmt | `ExprStmt` | ACTIVE | `value` | `Stmt` list |
| K12 | If | `If` | ACTIVE | `cond`, `then`, `else` | `Stmt` list |
| K13 | While | `While` | ACTIVE | `cond`, `body` | `Stmt` list |
| K14 | Literal | `Literal` | ACTIVE | — | Expr node |
| K15 | NullLiteral | `NullLiteral` | ACTIVE | — | Expr node |
| K16 | Unary | `Unary` | ACTIVE | `operand` | Expr node |
| K17 | Binary | `Binary` | ACTIVE | `left`, `right` | Expr node |
| K18 | Call | `Call` | ACTIVE | `args` | Expr node |
| K19 | FieldAccess | `FieldAccess` | ACTIVE | `target` | Expr node |
| K20 | IndexExpr | `IndexExpr` | ACTIVE | `target`, `index` | Expr node |
| K21 | RecordInit | `RecordInit` | ACTIVE | `fields` | Expr node |
| K23 | Name | `Name` | ACTIVE | — | Expr node |
| K24 | ListLiteral | `ListLiteral` | ACTIVE | `elements` | Expr node |
| K25 | MapLiteral | `MapLiteral` | ACTIVE | `entries` | Expr node |
| K32 | FieldInit | `FieldInit` | ACTIVE | `value` | `RecordInit` |

**Registry count:** 25 active identifiers: K01–K21, K23–K25, and K32.

## 3. FieldInit (K32) Formal Parent-Child Constraint

- **Parent:** `RecordInit` (K21).
- **Relationship:** `FieldInit` is a child-slot of `RecordInit`.
- **RecordInit collection arity:** The submitted remediation specifies that the `RecordInit` children count may be greater than or equal to zero.
- **Duplicate protection:** Field names among `FieldInit` children of one `RecordInit` MUST be unique.
- **Invalid relationship:** A `FieldInit` under a non-`RecordInit` parent is invalid.
- **Orphan handling:** An orphan `FieldInit` is invalid.

The exact serialized child representation and any flattening behavior must be interpreted according to the actual implementation evidence. The submitted audit noted that `FieldInit` is an AST structural node while serialization may flatten it. This remediation record does not invent a separate serialized arity for `FieldInit` beyond the submitted mapping's `value` child slot.

## 4. Counterexamples and Logic Verification

| Scenario | Definition | Result | Responsible Invariant / Check |
| :--- | :--- | :--- | :--- |
| Valid FieldInit | `RecordInit (K21) → FieldInit (K32) → Literal (K14)` | ACCEPTED | Valid parent-child relationship |
| Invalid parent | `Binary (K17) → FieldInit (K32)` | REJECTED | I1 — Structural consistency / allowed-child restriction |
| Duplicate field name | `RecordInit { x: 1, x: 2 }` | Structurally representable; invalid as a RecordInit | I4 — Unique field name per record |
| Null parent | `FieldInit (K32)` with no valid parent pointer | REJECTED | I2 — Parent/child integrity |
| Shared FieldInit | Two RecordInit nodes refer to the same FieldInit node | INVALID | I2 — Parent-pointer agreement / unique ownership |

The distinction between duplicate child references and duplicate field names is important:

- **Duplicate child reference:** the same node reference occurs more than once in a child collection. This is a structural collection-integrity issue.
- **Duplicate field name:** two FieldInit entries in one RecordInit have different or repeated node identities but equal field names. This is covered by I4.

## 5. Registry Clarification

- **Current active kind count:** 25.
- **Active identifiers:** K01–K21, K23–K25, K32.
- **Historical context:** The “27-kind target” in earlier proposal material is historical design/documentation debt, not a current functional requirement.
- **Unallocated identifiers:** K22 and K26/K27 are not assigned as active kinds by this remediation.

The registry must not be expanded merely to reach the historical count of 27.

## 6. Historical Mapping Conflicts

The corrected registry consolidates the current mapping and supersedes inconsistent assignments appearing in earlier drafts, including the previously discussed RecordDecl, Let, RecordInit, and MapLiteral mappings.

Current accepted assignments include:

- `RecordDecl` → K05
- `Let` → K06
- `RecordInit` → K21
- `MapLiteral` → K25
- `FieldInit` → K32, with parent `RecordInit` K21

Earlier drafts should remain preserved as historical records rather than being silently rewritten.

## 7. I4 Formalization Reference

The formal mathematical definition, identifier equality semantics, validation placement, and detailed counterexamples for I4 are recorded in `SH-01-WP-A-I4-FORMALIZATION.md`.

## 8. Audit Outcome and Remaining Scope

The independent re-audit initially returned CONDITIONAL because I4 had not yet been formally defined. A subsequent I4 formalization was submitted, followed by a final independent audit.

The final independent-audit result reported in the conversation was **ACCEPTED**, with:

- Registry count (25) verified as consistent.
- I4 formalization verified as robust.
- FieldInit (K32) parent-child constraint verified.
- No further findings.

This remediation artifact records WP-A only.

**WP-A:** CLOSED — ACCEPTED.  
**WP-B:** Ready for separate authorization.  
**WP-C / WP-D:** Not started.  
**SH-01 overall:** Not approved by this document.  
**Stage 1 gate:** UNSIGNED.  
**Implementation authorization:** Not granted by this document.
