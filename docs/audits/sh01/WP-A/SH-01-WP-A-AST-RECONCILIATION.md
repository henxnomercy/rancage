# RANCAGE — SH-01 WP-A AST Reconciliation

**Work Package:** WP-A — AST Inventory & Kind Registry Reconciliation  
**Artifact type:** AST inventory and mapping record  
**Current WP-A outcome:** CLOSED — ACCEPTED (based on the final independent-audit result reported in the conversation)  
**Provenance:** Persisted from the AST reconciliation content supplied in the ChatGPT conversation. This file was reconstructed from that supplied content; it has not been independently compared with the Windows workspace or repository files.

---

## 1. Complete AST Inventory (WP-A1)

The submitted inventory identifies 26 class entries, including `Span` as a helper structure, and maps the AST node classes to the proposed kind identifiers below.

| Class Name | Source (`ast.py`) | Fields | Kind | Status |
| :--- | :--- | :--- | :--- | :--- |
| `Span` | Line 7 | `line`, `column` | — (Helper) | VERIFIED |
| `FieldDecl` | Line 12 | `name`, `type_name`, `span` | K04 | VERIFIED |
| `RecordDecl` | Line 18 | `name`, `fields`, `span` | K05 | VERIFIED |
| `Program` | Line 24 | `functions`, `module`, `records` | K01 | VERIFIED |
| `Param` | Line 30 | `name`, `type_name`, `span` | K03 | VERIFIED |
| `Function` | Line 36 | `name`, `params`, `return_type`, `body`, `span` | K02 | VERIFIED |
| `Let` | Line 46 | `name`, `type_name`, `value`, `is_const`, `span` | K06 | VERIFIED |
| `Assign` | Line 54 | `name`, `value`, `span` | K07 | VERIFIED |
| `FieldAssign` | Line 60 | `target`, `field`, `value`, `span` | K08 | VERIFIED |
| `IndexAssign` | Line 67 | `target`, `index`, `value`, `span` | K09 | VERIFIED |
| `Return` | Line 74 | `value`, `span` | K10 | VERIFIED |
| `ExprStmt` | Line 79 | `value`, `span` | K11 | VERIFIED |
| `If` | Line 84 | `condition`, `then_body`, `else_body`, `span` | K12 | VERIFIED |
| `While` | Line 91 | `condition`, `body`, `span` | K13 | VERIFIED |
| `Literal` | Line 100 | `value`, `type_name`, `span` | K14 | VERIFIED |
| `NullLiteral` | Line 106 | `value`, `type_name`, `span` | K15 | VERIFIED |
| `Name` | Line 112 | `value`, `span` | K23 | VERIFIED |
| `Unary` | Line 117 | `op`, `operand`, `span` | K16 | VERIFIED |
| `Binary` | Line 123 | `left`, `op`, `right`, `span` | K17 | VERIFIED |
| `Call` | Line 130 | `name`, `args`, `span` | K18 | VERIFIED |
| `FieldAccess` | Line 136 | `target`, `field`, `span` | K19 | VERIFIED |
| `IndexExpr` | Line 142 | `target`, `index`, `span` | K20 | VERIFIED |
| `ListLiteral` | Line 148 | `elements`, `span` | K24 | VERIFIED |
| `FieldInit` | Line 153 | `name`, `value`, `span` | K32 | VERIFIED |
| `RecordInit` | Line 159 | `name`, `fields`, `span` | K21 | VERIFIED |
| `MapLiteral` | Line 165 | `entries`, `span` | K25 | VERIFIED |

## 2. AST Class and Kind Registry Reconciliation (WP-A2)

The reconciliation report recorded:

- **Total listed class entries:** 26, including `Span`.
- **Helper:** `Span` is not assigned a serialized node kind.
- **AST node classes:** 25 active AST node representations, according to the independent re-audit's counting convention (excluding helper/base structures as applicable).
- **Active kind identifiers:** 25.
- **Current active registry:** K01–K21, K23–K25, and K32.

The independent re-audit accepted the 25-active-kind registry as consistent with the current AST node inventory. The earlier phrase “27-kind child-slot table” was classified as a historical architectural target/documentation debt, not a current requirement for 27 active identifiers.

No K22, K26, or K27 identifier is allocated as an active kind by this reconciliation.

## 3. Mapping Integrity (WP-A3)

The reconciliation report recorded the following outcomes:

- `Name`, `ListLiteral`, and `MapLiteral` were added to the mapping inventory.
- No ambiguity was identified for the existing classes in the submitted reconciliation.
- The registry and AST inventory were subsequently accepted by the independent final WP-A audit.

**Scope note:** The `VERIFIED` labels above reproduce the statuses in the submitted reconciliation. This persisted document is not itself a fresh source-code or serialization audit. The independent final-audit verdict is recorded separately in the project audit trail.

## 4. Related Parent-Child Decision

The associated remediation established the relationship:

`FieldInit (K32) → RecordInit (K21)`

The formal FieldInit restrictions and I4 unique-field-name invariant are documented in:

- `SH-01-WP-A-REMEDIATION.md`
- `SH-01-WP-A-I4-FORMALIZATION.md`

## 5. Historical and Status Notes

Earlier SH-01 drafts contained conflicting kind assignments and references to a 27-kind target. The accepted current registry is the 25-active-kind registry listed above. Historical drafts should be retained as historical evidence and must not be confused with the accepted current mapping.

**WP-A status:** CLOSED — ACCEPTED, based on the independent final-audit result reported in the conversation.

**SH-01 overall status:** Not approved by this WP-A artifact.  
**Stage 1 gate:** UNSIGNED.  
**Implementation authorization:** Not granted by this document.
