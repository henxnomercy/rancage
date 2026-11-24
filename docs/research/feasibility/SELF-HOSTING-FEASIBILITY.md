# Self-Hosting Feasibility Audit — RANCAGE

**Date:** 2026-11-16  
**Requested by:** project owner  
**Scope:** Analyze whether RANCAGE 0.1 can host its own compiler, identify missing
capabilities, define a staged roadmap, and recommend the first implementation task.  
**Status:** proposal only — no implementation files created or modified.

## 1. Current state

Canonical implementation lives in `../../../src/rancage/` (Python 3.10+):

- [`lexer.py`](../../../src/rancage/lexer.py) — tokenizer with line/column tracking
- [`parser.py`](../../../src/rancage/parser.py) — recursive-descent + precedence-climbing
- [`ast.py`](../../../src/rancage/ast.py) — dataclass AST nodes
- [`typesys.py`](../../../src/rancage/typesys.py) — static type checker
- [`compiler.py`](../../../src/rancage/compiler.py) — AST → RANCAGE-IR bytecode
- [`vm.py`](../../../src/rancage/vm.py) — bounded stack VM, JSON `.rcb` loader
- [`cli.py`](../../../src/rancage/cli.py) — `check` / `build` / `run` / `targets`

Language baseline is RANCAGE 0.1 ([`../../../SPEC.md`](../../../SPEC.md) §3). The published `v0.1.0`
tag is frozen. All 16 existing tests must keep passing.

## 2. RANCAGE 0.1 capability inventory

What the language actually provides, from ../../../SPEC.md §3 and the executable parser:

| Capability | Available? | Notes |
|---|---|---|
| Scalar types | yes | `int`, `float`, `bool`, `string`, `void` |
| Functions | yes | typed params + return, module-level only |
| Variables | yes | `let`, immutable `const`, assignment |
| Control flow | yes | `if/else`, `while`, `return` |
| Operators | yes | arithmetic, comparison, equality, `&&`, `||`, unary `!`/`-` |
| `print(value)` | yes | only built-in |
| Comments | yes | `//`, `/* ... */` |
| Strings | partial | literals + `+` concat only; **no indexing, length, slice, split, char access** |
| Collections | **no** | no arrays, lists, tuples, maps, sets |
| Records/structs/classes | **no** | no user-defined composite types |
| Enums/algebraic types | **no** | none |
| Pattern matching | **no** | none |
| Exceptions/errors | **no** | no error type, no try/catch, no error propagation |
| File I/O | **no** | no `read_file`, `write_file`, no stdlib |
| Command-line args | **no** | none |
| Dynamic dispatch | **no** | no function pointers, no closures, no higher-order functions |
| Recursion | yes | but bounded by VM call-depth limit |
| String comparison | yes | `==`, `!=` only |
| Int/float conversion | **no** | no implicit conversion, no casts |
| Modules/imports | **no** | single-file programs only |

## 3. What a self-hosted compiler needs vs what 0.1 has

Mapping each compiler component to its language requirements:

| Compiler component | Required capabilities | RANCAGE 0.1 support |
|---|---|---|
| Lexer | char-by-char access, string indexing, mutable buffers, char classification | **missing**: no string indexing, no char access, no `len` on strings, no char code points |
| Parser | recursive AST construction, token lists, backtracking | **missing**: no lists/arrays, no records, no recursive data structures |
| AST | sum types / tagged unions, records with named fields | **missing**: no user-defined types at all |
| Type checker | symbol tables, scopes, sets, maps | **missing**: no maps/sets, no nested scopes as data |
| Compiler (IR emit) | mutable instruction lists, patching jump targets | **missing**: no lists, no mutation of collections |
| VM | stack, locals map, instruction fetch, arithmetic | **partial**: arithmetic and control flow exist, but no stack/list type, no map type, no JSON parse/emit, no file read |
| CLI driver | file read/write, argv, exit codes | **missing**: no file I/O, no argv, no exit codes |
| Bytecode format | JSON serialization/deserialization | **missing**: no JSON, no strings-as-data beyond literals |

**Verdict:** RANCAGE 0.1 cannot express any non-trivial part of its own compiler.
The gap is not incremental — the language lacks the fundamental data-model
primitives (composite types, collections, string introspection, I/O) that a
compiler is built from.

## 4. Three distinct self-hosting interpretations

The owner's request ("write the RANCAGE compiler in RANCAGE itself, then
bootstrap") conflates three different achievements. They must be separated:

1. **Self-hosted compiler on the Python reference VM.** A RANCAGE-source
   compiler that is compiled to RANCAGE-IR by the Python compiler, then executed
   by the Python reference VM. End users still need the Python-bundled VM
   executable. This is "RANCAGE-written, Python-run."

2. **Self-hosted compiler + self-hosted VM.** Same as (1), plus a VM written in
   RANCAGE, so the whole toolchain is RANCAGE source. Still requires a host VM
   to run the first bootstrap.

3. **Fully independent self-hosted toolchain.** A RANCAGE compiler that emits
   native machine code (or another self-contained target) with no Python in the
   loop at all. Requires a native backend, which is explicitly **not** implemented
   in 0.1 (see `PROJECT_STATUS.md` "Not implemented" and `targets.py`).

Interpretation (1) is the realistic first milestone. (2) is a stretch goal after
the language matures. (3) is blocked on a native backend and is out of scope for
this audit.

## 5. Smallest staged language-feature roadmap to self-hosting

Each stage is independently testable and gated by the project's release rule:
"a planned target is not supported until it builds and passes tests."

### Stage 0 — Foundation primitives (prerequisite for everything)

Add to the language, behind an explicit version bump (RANCAGE 0.2):

- String indexing (`s[i]`), `len(s)`, char-to-int / int-to-char, substring/slice
- Dynamic arrays (`list[T]`) with push, pop, indexing, length
- Mutable maps (`map[K,V]`) with get/set/contains
- Records / structs with named fields (and enums later)

Acceptance criteria:
- Golden-output tests for each primitive in `tests/`
- No regression in the existing 16 tests
- ../../../SPEC.md updated to match the executable parser

### Stage 1 — Compiler data model in RANCAGE

Express AST nodes as records, token stream as array, symbol table as map.

Acceptance criteria:
- A `.cage` program can build and traverse a small AST of records
- Unit tests construct an AST node, mutate a field, and print it

### Stage 2 — Lexer + parser in RANCAGE

Implement `tokenize` and `parse` over the Stage 0 primitives.

Acceptance criteria:
- The RANCAGE lexer+parser produces the same token stream / AST as the Python
  reference for `examples/*.cage`
- A conformance test compares RANCAGE-compiler output against Python-compiler
  output byte-for-byte on the three examples

### Stage 3 — Type checker + IR emitter in RANCAGE

Acceptance criteria:
- `cage check` and `cage build` work when driven by the RANCAGE compiler
- All 16 existing tests still pass (Python reference remains canonical)
- New tests: RANCAGE compiler rejects the same error programs the Python one does

### Stage 4 — VM in RANCAGE (optional, for interpretation 2)

Acceptance criteria:
- The RANCAGE VM runs `.rcb` files produced by Stage 3
- Execution budget and call-depth limits are honored

### Stage 5 — Bootstrap + native backend (interpretation 3, long-term)

Blocked on Stage 0–4 plus a native code generator. Not part of this audit's
near-term plan.

## 6. Architectural dependencies

- Stage 0 is a hard prerequisite for Stages 1–4; none of the compiler can be
  written without collections, string introspection, and records.
- The Python reference compiler must remain canonical during all stages
  (AGENTS.md rule 1). The RANCAGE compiler is a second implementation that must
  agree with the reference on a shared test corpus.
- The RANCAGE-IR JSON format must not change (AGENTS.md rule 4), so the
  RANCAGE compiler must emit the same IR schema as `compiler.py`.
- File I/O for the CLI driver needs a capability-gated host API, which the
  roadmap (`ROADMAP.md` v0.3 "standard-library design") has not yet specified.
  The current security policy (SECURITY.md §5) forbids host filesystem access,
  so a new capability mechanism must be designed before Stage 3 can be a real
  CLI.

## 7. Risks

| Risk | Severity | Mitigation |
|---|---|---|
| Stage 0 changes language semantics / IR | high | Version-bump to 0.2; keep 0.1 frozen; no IR format change |
| Two implementations drift | high | Byte-for-byte conformance tests against Python reference |
| Capability-based stdlib not designed yet | medium | Block CLI stage until stdlib design is reviewed (ROADMAP v0.3) |
| Scope creep toward native backend | medium | Interpretation (3) explicitly out of scope; separate proposal |
| Breaking the 16-test suite | high | Every stage runs `run-tests.cmd` before merge |
| Owner expectation mismatch | high | This audit must be approved before any code is written |

## 8. Recommended first implementation task

**Do not write any RANCAGE compiler code yet.** The smallest approved next step
is:

> Draft a RANCAGE 0.2 language proposal adding Stage 0 primitives (string
> indexing/length, dynamic arrays, maps, records), with ../../../SPEC.md changes,
> reference tests, and a decision on whether the IR format stays 0.1.

That proposal is a documentation + test task, not a compiler task, and it
respects the constraint that `../../../src/rancage/` stays untouched until the owner
approves.

## 9. Conclusion

RANCAGE 0.1 is not self-hostable. It lacks every data-model primitive a compiler
needs. The honest path is a staged language evolution (Stages 0–4), keeping the
Python reference compiler canonical at every step, with interpretation (1) —
"self-hosted compiler running on the Python reference VM" — as the first
achievable milestone. No code should be written until the owner approves this
audit and the Stage 0 proposal.
