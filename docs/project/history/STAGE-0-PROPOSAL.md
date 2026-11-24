# RANCAGE 0.2 Stage 0 Language Proposal — Primitives for Self-Hosting

**Document status:** Draft RFC / Architecture Proposal  
**Target release:** RANCAGE 0.2.0-preview  
**Baseline reference:** RANCAGE 0.1.0 (`SPEC.md`)  
**Implementation target:** `src/rancage/` (Python 3.10+ reference compiler and bounded VM)  
**Implementation status:** PENDING APPROVAL (No compiler or VM code modified)  

---

## 1. Executive Summary & Problem Statement

The RANCAGE 0.1 language core (`SPEC.md`) provides scalar types (`int`, `float`, `bool`, `string`, `void`), module-level functions, basic control flow (`if/else`, `while`), and arithmetic/logical operators. As audited in `SELF-HOSTING-FEASIBILITY.md`, this subset cannot implement any stage of a compiler:
1. No character inspection or length on strings (lexer cannot scan source text).
2. No homogeneous collections or dynamic arrays (parser cannot accumulate tokens, statements, expressions, or IR instructions).
3. No user-defined compound records (AST nodes cannot be represented).
4. No associative mappings (type checker cannot look up symbols or variable scopes).
5. No host boundary for ingestion of source files without violating sandbox security (`SECURITY.md`).

This proposal specifies **RANCAGE 0.2 Stage 0**: the minimal, strictly typed primitive foundation necessary to build AST data models, a lexer, a recursive-descent parser, and an IR emitter in RANCAGE, running entirely within the memory-safe boundaries of the existing reference VM.

---

## 2. Capability Postponement Analysis (What is Required vs What Can Wait)

To prevent scope creep and maintain the stability of the Python reference implementation, candidates for Stage 0 are classified into **Mandatory (Stage 0)**, **Deferred to Stage 0.2 Minor (Stage 0.5)**, and **Postponed to Stage 1+**:

| Feature Candidate | Classification | Technical Rationale |
|---|---|---|
| `string` indexing & `len()` | **Mandatory** (Stage 0) | Lexing is impossible without reading individual characters and knowing input length. |
| `list[T]` (Dynamic Arrays) | **Mandatory** (Stage 0) | AST nodes hold lists of statements, parameter lists, argument lists, and token buffers. |
| `record` (Product Types) | **Mandatory** (Stage 0) | AST nodes (`BinaryExpr`, `LetStmt`, `Token`) require structured fields with strict types. |
| `ord(s)` / `chr(n)` | **Mandatory** (Stage 0) | Tokenizer requires numeric ASCII/Unicode code point comparisons (e.g. `c >= 48 && c <= 57`). |
| Nullable Reference (`T?`) | **Mandatory** (Stage 0) | Recursive AST structures require nullable link points (e.g., `else_body: Block?`, `value: Expr?`). |
| `map[K, V]` (Hash Maps) | **Deferred** (Stage 0.5) | Parser and AST do **not** require maps; they use lists and records. Symbol tables in type checking can initially be linear lookup or string-keyed map only. Full generic `map[K,V]` with arbitrary hashable keys adds substantial type-checker complexity. Restricting initial map to `map[string, T]` or deferring to Stage 0.5 lowers Stage 0 risk. |
| Tagged Unions / Sum Types (`enum`) | **Postponed** (Stage 1) | Sum types with pattern matching require complex exhaustiveness checking and IR tag management. Stage 0 can represent AST variants using records with a `kind: int` or `kind: string` discriminant tag and nullable payload fields or base records. |
| Closures / Function Pointers | **Postponed** (Stage 2+) | Unnecessary for top-down recursive descent compilation. Increases VM stack complexity. |
| Direct Host Filesystem I/O | **Postponed** (Stage 3+) | Violates `SECURITY.md`. In-memory string compilation adapters eliminate any need for raw OS file handles. |

**Decision for Stage 0 Scope:** Implement `string` introspection (`s[i]`, `len(s)`, `slice(s, start, len)`, `ord(s)`, `chr(n)`), homogeneous dynamic arrays `list[T]`, named product records `record Name { ... }`, and nullable references `T?` with explicit `null`. Provide `map[string, T]` (string-keyed dictionaries) as a restricted container, postponing open generic keys `map[K, V]` and full algebraic sum types `enum`.

---

## 3. String & Unicode Semantics

### 3.1 Encoding & Indexing
- Source files and runtime strings are valid UTF-8.
- Indexing `s[i]` operates on **Unicode code points** (scalar values), returning a new single-character string `string`.
- `len(s)` returns the number of Unicode scalar values in `s` as an `int`.
- Negative indexing is disallowed at compile-time when constant, and raises a runtime error `RancageRuntimeError` if dynamically evaluated negative or `>= len(s)`.

### 3.2 Slicing
- Intrinsic function `slice(s: string, start: int, length: int) -> string`:
  - Returns a substring of `length` code points beginning at `start`.
  - Boundary behavior: If `start < 0` or `length < 0` or `start > len(s)`, raises `RancageRuntimeError`.
  - Clamping: If `start + length > len(s)`, slices to `len(s)` without error.

### 3.3 Character Conversion Primitives
- `ord(ch: string) -> int`:
  - Requires `len(ch) == 1`. Returns the integer Unicode code point (e.g., `ord("A") == 65`, `ord("0") == 48`).
  - Raises `RancageRuntimeError` if `len(ch) != 1`.
- `chr(cp: int) -> string`:
  - Converts integer Unicode scalar value `cp` to a 1-character string.
  - Raises `RancageRuntimeError` if `cp < 0` or `(cp >= 0xD800 and cp <= 0xDFFF)` or `cp > 0x10FFFF`.

---

## 4. Generic Collections: `list[T]` and `map[string, V]`

### 4.1 Type System & Syntax
`list[T]` represents a dynamically sized, ordered, homogeneous array of element type `T`.
- `T` may be any valid primitive type (`int`, `float`, `bool`, `string`), record type, or another collection (e.g., `list[list[int]]`).
- Array literal syntax: `[expr1, expr2, ...]` where all element expressions match type `T`.
- Empty array initialization requires explicit type annotation:
  ```cage
  let tokens: list[Token] = [];
  ```
- Type checker ensures homogeneous type across all elements and enforces element type on push/assignment.

### 4.2 Operations on `list[T]`
1. Index lookup: `xs[i]` -> returns `T`. Bound-checked `0 <= i < len(xs)`.
2. Index assignment: `xs[i] = expr;` -> assigns `expr: T` into index `i`.
3. `push(xs: list[T], item: T) -> void` -> appends `item` to end of `xs`.
4. `pop(xs: list[T]) -> T` -> removes and returns last element; raises `RancageRuntimeError` if `len(xs) == 0`.
5. `len(xs: list[T]) -> int` -> returns current element count.

### 4.3 String-Keyed Dictionaries `map[string, V]`
For symbol tables and environment representations:
1. Map literal: `{}` with type annotation `let syms: map[string, int] = {};`
2. Key lookup: `m[k]` -> returns `V`. If `k` does not exist, raises runtime error `RancageRuntimeError` (or returns `null` if `V` is nullable).
3. Key assignment: `m[k] = val;` -> associates `k` with `val: V`.
4. `map_has(m: map[string, V], k: string) -> bool` -> checks presence of key.
5. `map_remove(m: map[string, V], k: string) -> bool` -> deletes key, returns `true` if existed.
6. `len(m: map[string, V]) -> int` -> returns count of key-value pairs.

---

## 5. Records, Recursive AST Nodes, and Reference Semantics

### 5.1 Record Declaration & Instantiation
Records are declared at module scope:
```cage
record Span {
    line: int;
    column: int;
}

record Token {
    kind: int;
    text: string;
    span: Span;
}
```
Instantiation uses constructor syntax:
```cage
let sp: Span = Span { line: 1, column: 1 };
let tok: Token = Token { kind: 101, text: "let", span: sp };
```

### 5.2 Recursive AST Representation & Nullability (`T?`)
Compilers require recursive AST node links. In 0.1, all types are non-nullable. Stage 0 introduces the nullable marker `T?`:
```cage
record ExprNode {
    kind: int;
    int_val: int;
    str_val: string;
    left: ExprNode?;
    right: ExprNode?;
    span: Span;
}
```
- `null` literal is assignable to any `T?` reference type.
- Equality comparison `expr == null` and `expr != null` is statically allowed for nullable types.
- Accessing a field `node.left` when `node == null` raises `RancageRuntimeError`.

### 5.3 Memory and Reference Semantics
- **Scalar types (`int`, `float`, `bool`, `string`):** Value semantics. Strings are immutable values.
- **Composite types (`record`, `list[T]`, `map[string, V]`):** Reference semantics.
  - Assignment `let b = a;` copies the reference pointing to the underlying heap structure.
  - Mutations through `b.field = 42;` or `push(b, x);` are visible through `a`.
  - In the Python reference VM, records, lists, and maps are represented by Python heap objects (`dict`, `list`), participating in Python host garbage collection without manual memory allocation or risk of memory corruption.

---

## 6. Minimal Secure Host Interface for Compiler Driver

`SECURITY.md` strictly prohibits arbitrary host file execution or directory traversal in the RANCAGE runtime. The self-hosted compiler must operate deterministically within the memory boundary:

### 6.1 Host Adapter Invocation Pattern
Instead of introducing unsafe filesystem APIs (`file_open`, `file_read`, `system`), the compilation interface is exposed as a pure in-memory entry point:

```cage
// compiler_main.cage
fn compile_source(source_text: string, module_name: string) -> string {
    let tokens: list[Token] = tokenize(source_text);
    let ast: ProgramNode = parse_program(tokens, module_name);
    let ir_json: string = emit_ir(ast);
    return ir_json;
}
```

### 6.2 Python Host Integration Bridge
The Python CLI (`cli.py`) and host runtime invoke the entry point securely:
```python
# Host Python Driver Adapter (src/rancage/driver.py)
def run_rancage_compiler(compiler_vm: VirtualMachine, source_code: str, module_name: str) -> dict:
    # Passes source string directly on stack via entry call
    output_str = compiler_vm.call_function("compile_source", [source_code, module_name])
    return json.loads(output_str)
```
- **Zero OS privileges required:** No file descriptors or system calls leak into bytecode.
- **Bounded execution:** Instruction step counters (`max_steps`) and stack depth limits (`max_depth`) remain active.
- **Defense in depth:** Malformed or adversarial `.cage` source files cannot escape VM boundaries.

---

## 7. RANCAGE-IR Compatibility Plan

### 7.1 Preservation of Existing 0.1 Schema
The v0.1 JSON schema documented in `SPEC.md §4.1` remains frozen and fully operational:
```json
{
  "format": "RANCAGE-IR",
  "version": "0.1",
  "module": "name",
  "entry": "main",
  "functions": {}
}
```
All existing 23 opcodes keep identical signatures and semantics in `src/rancage/vm.py`:
`PUSH`, `LOAD`, `STORE`, `POP`, `ADD`, `SUB`, `MUL`, `DIV`, `MOD`, `EQ`, `NE`, `LT`, `LE`, `GT`, `GE`, `AND`, `OR`, `NOT`, `NEG`, `JUMP`, `JUMP_IF_FALSE`, `CALL`, `RETURN`.

### 7.2 Version 0.2 Bytecode Container
Programs targeting Stage 0 declare `"version": "0.2"`. The reference VM is updated backward-compatibly:
```python
if self.program.get("version") not in {"0.1", "0.2"}:
    raise RancageRuntimeError("Format atau versi RANCAGE-IR tidak didukung")
```

### 7.3 Stage 0 Opcodes (Strictly Bounded)
To support collection and record access without overloading arithmetic operators:
1. `MAKE_LIST` `[ "MAKE_LIST", count ]`: Pops `count` items from stack, creates `list`, pushes reference.
2. `LIST_GET` `[ "LIST_GET" ]`: Pops `index`, pops `list`, pushes `list[index]`.
3. `LIST_SET` `[ "LIST_SET" ]`: Pops `val`, pops `index`, pops `list`, assigns `list[index] = val`.
4. `MAKE_RECORD` `[ "MAKE_RECORD", record_name, field_names ]`: Pops field values, pushes record dictionary.
5. `GET_FIELD` `[ "GET_FIELD", field_name ]`: Pops record reference, pushes field value.
6. `SET_FIELD` `[ "SET_FIELD", field_name ]`: Pops value, pops record reference, sets `record[field_name] = value`.
7. `STRING_GET` `[ "STRING_GET" ]`: Pops `index`, pops `string`, pushes 1-char substring.
8. Intrinsic operations (`len`, `push`, `pop`, `ord`, `chr`, `slice`, `map_has`, `map_remove`) are mapped to validated built-in function calls under `CALL`, keeping the VM instruction set compact.

---

## 8. Detailed Grammar Extensions

Extending `SPEC.md §3.3`:

```ebnf
program         = [ "module" , IDENT , ";" ] , { declaration } ;
declaration     = record_decl | function ;

record_decl     = "record" , IDENT , "{" , { field_decl } , "}" ;
field_decl      = IDENT , ":" , type , ";" ;

type            = base_type , [ "?" ] ;
base_type       = "int" | "float" | "bool" | "string" | "void"
                | "list" , "[" , type , "]"
                | "map" , "[" , "string" , "," , type , "]"
                | IDENT ;

statement       = let | const | assignment | return | if | while | expr_stmt ;
assignment      = target , "=" , expression , ";" ;
target          = IDENT [ "[" , expression , "]" | "." , IDENT ] ;

expression      = ... (precedence climbing)
primary         = IDENT
                | LITERAL
                | "null"
                | "[" , [ expression , { "," , expression } ] , "]"
                | IDENT , "{" , [ field_init , { "," , field_init } ] , "}"
                | primary , "[" , expression , "]"
                | primary , "." , IDENT
                | primary , "(" , [ args ] , ")" ;

field_init      = IDENT , ":" , expression ;
```

---

## 9. Error Behavior Matrix

| Error Condition | Phase Detected | Exception Type | Example Source / Scenario |
|---|---|---|---|
| Incompatible element in list literal | Compile Time | `RancageTypeError` | `let xs: list[int] = [1, "two", 3];` |
| Indexing non-indexable type | Compile Time | `RancageTypeError` | `let n: int = 10; let x = n[0];` |
| Invalid field access on record | Compile Time | `RancageTypeError` | `tok.unknown_field` |
| Mutating const list or record binding | Compile Time | `RancageTypeError` | `const xs = [1]; xs = [2];` |
| Out-of-bounds list or string index | Runtime | `RancageRuntimeError` | `let s = "hi"; let c = s[5];` |
| Indexing empty list or popping empty | Runtime | `RancageRuntimeError` | `let xs: list[int] = []; pop(xs);` |
| Field access on `null` | Runtime | `RancageRuntimeError` | `let n: ExprNode? = null; print(n.kind);` |
| Invalid code point in `chr()` | Runtime | `RancageRuntimeError` | `chr(-5);` or `chr(0x110000);` |
| Non-single-char in `ord()` | Runtime | `RancageRuntimeError` | `ord("ABC");` |
| Instruction or recursion budget exceeded | Runtime | `RancageRuntimeError` | Stack depth > 128 or steps > 1,000,000 |

---

## 10. Test Matrix & Acceptance Criteria

Stage 0 implementation will be gated by 100% pass on both existing baseline tests and new Stage 0 suites:

| Suite ID | Test Description | Target Verification |
|---|---|---|
| `LEGACY-01` | Run all 16 existing tests in `tests/test_rancage.py` | Zero regressions in 0.1 scalar and control flow semantics. |
| `STR-01` | String length and character index | `len("hello") == 5`, `"hello"[1] == "e"`. |
| `STR-02` | Unicode scalar slicing and multi-byte UTF-8 | `len("kucing 🐱") == 8`, `slice("kucing 🐱", 7, 1) == "🐱"`. |
| `STR-03` | `ord()` and `chr()` conversions | `ord("A") == 65`, `chr(65) == "A"`, round-trip equality. |
| `STR-04` | String index out-of-bounds error | Negative index or index `>= len` raises `RancageRuntimeError`. |
| `LIST-01` | Dynamic array allocation, push, pop | Push integers 1..5, verify length, pop in LIFO order. |
| `LIST-02` | Element type checking | Rejection of mixed-type array literals at compile time. |
| `LIST-03` | List index assignment and reading | `xs[0] = 42; print(xs[0]);` |
| `REC-01` | Record declaration, initialization, field reading | Instantiate `Span { line: 12, column: 4 }`, access fields. |
| `REC-02` | Recursive data structure with `T?` and `null` | Build 3-node binary tree, traverse preorder, verify leaves. |
| `MAP-01` | String-keyed map insertion, lookup, `map_has` | Insert symbols into `map[string, int]`, query presence and values. |
| `HOST-01` | In-memory compilation driver bridge | Pass sample `.cage` text into VM entry function, receive valid IR string. |

---

## 11. Dependency Diagram

```
+-------------------------------------------------------------+
|                      RANCAGE 0.2 Core                       |
+-------------------------------------------------------------+
                              |
       +----------------------+----------------------+
       |                                             |
       v                                             v
[String & Unicode]                            [Generic Types]
- s[i], len(s), slice()                       - list[T]
- ord(s), chr(n)                              - map[string, V]
       |                                             |
       +----------------------+----------------------+
                              |
                              v
                   [Records & Nullability]
                   - record Name { ... }
                   - T? and null
                              |
                              v
                [Recursive AST Data Structures]
                - Token, Span, Node records
                              |
                              v
             [In-Memory Host Compilation Driver]
             - fn compile_source(source: string) -> string
```

---

## 12. Explicit Implementation Milestones

Execution will proceed only after formal project-owner approval of this proposal:

1. **Milestone M0.1 (Lexer & AST Extensions):**
   - Extend `ast.py` with `RecordDecl`, `FieldAccess`, `IndexExpr`, `ListLiteral`, `MapLiteral`, `NullLiteral`.
   - Update `lexer.py` to tokenize `record`, `null`, `[`, `]`, `{`, `}`, `.`, `?`.
2. **Milestone M0.2 (Parser & Type Checker):**
   - Recursive descent support for record declarations and generic type expressions.
   - Extend `typesys.py` to validate record field signatures, generic list compatibility, and null safety.
3. **Milestone M0.3 (Compiler & IR Emitting):**
   - Emit `MAKE_LIST`, `LIST_GET`, `LIST_SET`, `MAKE_RECORD`, `GET_FIELD`, `SET_FIELD`, `STRING_GET`.
   - Register intrinsics (`len`, `push`, `pop`, `ord`, `chr`, `slice`) under standard `CALL`.
4. **Milestone M0.4 (Virtual Machine Updates):**
   - Support `"version": "0.2"` while preserving `"version": "0.1"`.
   - Implement opcode handlers with bounded memory and index safety.
5. **Milestone M0.5 (Verification & Conformance):**
   - Execute test suite (`run-tests.cmd`): 16 legacy tests + 12 new Stage 0 tests.
   - Update `SPEC.md`, `CHANGELOG.md`, and `AI-HANDOFF.md`.
