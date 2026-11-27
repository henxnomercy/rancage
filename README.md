<p align="center">
  <img src="assets/brand/rancage/png/color/RANCAGE-icon-256.png" alt="RANCAGE logo" width="128" height="128">
</p>

<h1 align="center">RANCAGE</h1>

<h3 align="center">A Language Built with Purpose.</h3>

<p align="center">
  <b>Lightweight by Design. Safe by Discipline. Strong by Capability.</b>
</p>

<p align="center">
  <img src="assets/brand/rancage/svg/principles/lightweight.svg" alt="Lightweight" width="48" height="48">
  <img src="assets/brand/rancage/svg/principles/safety.svg" alt="Safety" width="48" height="48">
  <img src="assets/brand/rancage/svg/principles/strong.svg" alt="Strong" width="48" height="48">
</p>

RANCAGE is an independent general-purpose programming language project rooted in Sundanese identity. The name comes from **"rancagé"** — *cakap* (speech/word), *cekatan* (agile/quick), *kreatif*, and *kapabilitas* — and is built on three fundamental principles: **Lightweight**, **Safety**, and **Strong**. It is developed incrementally with attention to efficiency, security, expressive capability, semantic consistency, and implementation reliability.

This repository contains the RANCAGE reference implementation: lexer, parser, AST, static type checker, RANCAGE-IR bytecode compiler, bounded virtual machine, CLI, examples, and tests. RANCAGE source files use the `.cage` extension and compile to `.rcb` bytecode executed by the reference VM.

> **Current reality:** the implemented target is the Python reference VM. RANCAGE does not yet produce native machine code, Android APK/AAB, iOS apps, or other production targets as shipped features.

**Rancagé dina karya, pageuh dina prinsip.**
*Cakap dalam berkarya, teguh dalam prinsip.*

## Rooted in Sundanese Identity

RANCAGE carries the heritage of the Sundanese language — **"rancagé"** meaning *cakap* (speech/word), *cekatan* (agile/quick), *kreatif*, and *kapabilitas* — into technology. The name reflects a spirit of eloquence, agility, creativity, and capability. RANCAGE is an independent project open to the global community; it is not limited to Sundanese speakers nor does it require Sundanese syntax.

## The Three Principles

### Lightweight

Efficiency without unnecessary complexity.

- Small footprint
- Fast startup
- Low memory consumption
- Minimal dependencies

### Safety

Protection built into the way software is designed and executed.

- Static checks
- Predictable runtime behavior
- Secure defaults
- Resource controls
- Carefully designed execution environment

> These are design goals. Not every item is a shipped production security feature yet.

### Strong

Capability, consistency, and dependable behavior.

- Sufficient expressiveness
- Consistent semantics
- Reliable tooling
- Clear diagnostics
- Performance appropriate to intended workloads

The three principles must stay balanced: Lightweight must not sacrifice Safety, Safety must not needlessly restrict capability, and Strong must not introduce excess complexity.

## Design Philosophy

RANCAGE is developed according to its own design, specification, decisions, and project milestones — not by copying another language's architecture. Priorities are correctness, security, stability, verifiable progress, reproducible tests and benchmarks, and mature features over premature feature expansion.

The spirit of the name — *cakap* (eloquence), *cekatan* (agility), *kreatif*, and *kapabilitas* — maps naturally onto the engineering principles. Lightweight reflects agility without excess; Safety reflects careful, principled craftsmanship; Strong reflects capability and creative problem-solving. These are conceptual resonances, not symbolic claims: RANCAGE remains a technology project open to the global community.

## Current Implementation

- **Version:** `RANCAGE 0.2.0a1` (development preview). `v0.1.0` is the frozen initial release.
- **Implementation language:** Python 3.10+, standard library only.
- **Compiler:** lexer, parser, AST builder, static type checker, RANCAGE-IR 0.2 bytecode compiler.
- **VM:** bounded reference virtual machine executing `.rcb` JSON bytecode with step and allocation budgets.
- **Targets (from `cage targets`):**
  - `rancage-vm` — implemented-experimental (reference bytecode VM)
  - `wasm` — implemented-experimental (.wasm emitter for numeric/bool/control-flow subset)
  - `native`, `dotnet`, `jvm`, `javascript`, `lua`, `kotlin`, `swift`, `c`, `engines`, `embedded` — planned
- **Not claimed:** self-hosting compiler, native binary output, Android backend, production WebAssembly, Roblox Luau, or hardened sandbox.

### Verified language features

- Types: `int`, `float`, `bool`, `string`, `void`
- Functions: `fn` with typed parameters and returns
- Bindings: `let` and immutable `const`
- Assignment, function calls, `print(value)`
- Control flow: `if/else`, `while`, `return`, `break`, `continue`
- Operators: arithmetic, comparison, equality, boolean
- Comments: `//` and `/* ... */`
- Collections: list, map, record instantiation and field access
- Nullable types and indexing (including negative index and unicode string indexing)
- Intrinsics: `len`, `push`, `pop`, `ord`, `chr`, `slice`, `map_has`, `map_remove`, etc.
- Error handling: `try`/`catch`/`throw` (English and Sundanese preset `coba`/`tewak`/`balang`)
- Modules/imports with depth limit and cyclic-import rejection
- Static type checking before code generation
- Defensive bytecode validation and pre-execution call-arity validation

### Sundanese preset

RANCAGE includes an ASCII Sundanese keyword preset (`su`): `coba`/`tewak`/`balang` for error handling, `eureun`/`tuluy` for loop control, and `mawa` for import. Canonical tokens are verified by the lexer tests.

## Project Structure

```
src/rancage/     # reference compiler, parser, type checker, VM, CLI, targets
tests/           # unit and integration tests (unittest, stdlib only)
examples/        # .cage example programs
assets/brand/rancage/  # brand assets (PNG, SVG principles, provenance)
docs/            # architecture, audits, research, project docs
licenses/        # CORE-PROPRIETARY, SDK-MIT
```

## Requirements

- Python 3.10+
- Git (for source checkout)
- Runtime uses the Python standard library only

## Getting Started

Windows source checkout:

```powershell
python --version
.\cage.cmd --version
.\run-tests.cmd
.\cage.cmd check examples\hello.cage
.\cage.cmd run examples\hello.cage
```

Linux/macOS source checkout:

```bash
python --version
PYTHONPATH=src python -m rancage --version
PYTHONPATH=src python -m unittest discover -s tests -v
PYTHONPATH=src python -m rancage run examples/hello.cage
```

## CLI Usage

Canonical extensions: `.cage` for source, `.rcb` for compiled bytecode. Primary command is `cage` (`cage.exe` on Windows); `rancage` remains an alias where `cage` is taken by another application. Old `.nova`, `.nvm`, and interim `.rcg` extensions are no longer accepted by source CLI commands.

```powershell
.\cage.cmd check examples\hello.cage
.\cage.cmd build examples\hello.cage -o build\hello.rcb
.\cage.cmd run examples\hello.cage
.\cage.cmd run build\hello.rcb
.\cage.cmd targets
```

## Examples

- `examples/hello.cage` — canonical hello program
- `examples/test_wasm_su.cage` — Sundanese wasm-rejection regression
- `examples/test_kontrol_su.cage` — Sundanese control-flow regression
- `examples/test_batas_vm.cage` — VM step-budget regression

## Testing and Verification

Run the source test suite:

```powershell
.\run-tests.cmd
```

or on Linux/macOS:

```bash
PYTHONPATH=src python -m unittest discover -s tests -v
```

**Actual result:** `Ran 190 tests in < 1s — OK`.

The Windows standalone workflow builds one-file and one-folder variants and runs executable smoke tests. `--version`, source validation/execution, bytecode build, and bytecode execution have been manually tested for the example programs on Windows without a separate Python installation.

## Security Notes

RANCAGE `.rcb` bytecode is JSON-based and readable/editable. PyInstaller packaging (Windows standalone preview) is a deployment convenience, not obfuscation or tamper protection. Do not put API keys or secrets in RANCAGE client-side programs. The VM is not a hardened sandbox for hostile workloads — review [SECURITY.md](SECURITY.md). Third-party notices are in [THIRD-PARTY-NOTICES.md](THIRD-PARTY-NOTICES.md).

## Licensing

RANCAGE uses a **hybrid licensing model**. The RANCAGE compiler/runtime core and CAGE executable are proprietary under [licenses/CORE-PROPRIETARY.txt](licenses/CORE-PROPRIETARY.txt). The license permits royalty-free use of the official, unmodified CAGE release to create, compile, test, and run your own RANCAGE programs, including commercial applications. You may distribute your own programs and `.rcb` output without royalties, but may not bundle or redistribute the RANCAGE Core itself without separate written permission.

Only SDK materials explicitly designated as MIT-licensed are covered by [licenses/SDK-MIT.txt](licenses/SDK-MIT.txt). Documentation, examples, tests, specifications, build scripts, and other repository contents are not automatically covered by the SDK's MIT license.

Public visibility on GitHub does not make RANCAGE Core open-source. GitHub's Terms of Service permit viewing and forking public repositories through the GitHub service; those limited platform rights do not grant a general license to use, modify, or redistribute RANCAGE Core outside those terms. See [LICENSE](LICENSE) for the licensing map.

## Project Status and Future Direction

`v0.1.0` remains the frozen initial release. `0.2.0-alpha.1` is an unreleased development preview focused on Windows standalone packaging. The language grammar and semantics are not intentionally changed in this preview.

- **Implemented:** reference Python compiler and VM, `.cage`/`.rcb`, static type checking, collections, nullable types, error handling, imports, CLI, wasm emitter (experimental), Sundanese preset.
- **In development:** Windows standalone packaging pipeline (PyInstaller).
- **Planned / Future goals:** native backend, Android, JVM, .NET, JavaScript, Lua/Luau, Kotlin, Swift, C ABI, embedded, and game-engine adapters — all listed as `planned` in `cage targets`; none are implemented or verified yet.

No native backend, Android backend, self-hosting compiler, hardened sandbox, or production platform support is claimed.
