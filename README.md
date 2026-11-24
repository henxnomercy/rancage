# RANCAGE — Universal Programming Language

**Published version tag:** `v0.1.0-alpha.1` (pre-release)
**Python package version:** `0.1.0a1`
**CLI version output:** `RANCAGE 0.1.0a1`
**Language baseline:** RANCAGE 0.1 syntax and semantics
**Implementation:** Python reference compiler and VM

RANCAGE is an experimental general-purpose programming language project. This
repository contains its reference implementation: lexer, parser, AST, static
type checker, RANCAGE-IR bytecode compiler, bounded virtual machine, CLI,
examples, documentation, and tests.

> **Current reality:** the implemented execution target is the Python reference
> VM. RANCAGE does not yet compile to native machine code, Android APK/AAB, iOS
> apps, WebAssembly, Roblox Luau, or other production targets.

## Versioning

This clean-slate repository starts with one root commit and the annotated Git
tag `v0.1.0-alpha.1`. The Python package metadata uses the PEP 440 normalized
version `0.1.0a1`, which is the value shown by the CLI as
`RANCAGE 0.1.0a1`. These are representations of the same pre-release version.

The language syntax and semantics baseline remains RANCAGE 0.1. The package
version, CLI display, Git tag, language baseline, and RANCAGE-IR format version
are separate version layers and must not be conflated.

## Implementation decision

The active compiler, CLI, and reference VM are implemented in **Python 3.10+**.
RANCAGE source files use the `.cage` extension and are not Python programs. Rust
is not part of the active implementation. Read
[docs/research/rpr/decisions/IMPLEMENTATION_DECISION.md](docs/research/rpr/decisions/IMPLEMENTATION_DECISION.md).

## Development setup

Requirements: Python 3.10+ and Git. Runtime uses the Python standard library
only.

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

## Windows standalone packaging

The repository includes a **Windows executable packaging pipeline** using
PyInstaller. The end-user package runs without a separate Python installation
because the Python runtime is bundled into the distribution.

This is a packaged Python application, **not** a native compiler rewrite and
**not** self-hosting RANCAGE. Python remains the language used to implement the
compiler. PyInstaller is a build-time tool; end users do not install it.

The Windows x64 workflow builds and smoke-tests the package, then uploads a
workflow artifact. The ZIP distribution contains `cage.exe`, a one-folder
fallback, examples, and third-party notices.

To build on Windows, see [docs/project/BUILDING-STANDALONE.md](docs/project/BUILDING-STANDALONE.md).
PyInstaller is not a cross-compiler; build on the target operating system.

## CLI commands

```powershell
.\cage.cmd check examples\hello.cage
.\cage.cmd build examples\hello.cage -o build\hello.rcb
.\cage.cmd run examples\hello.cage
.\cage.cmd run build\hello.rcb
.\cage.cmd targets
```

The canonical file extensions are `.cage` for source and `.rcb` for compiled
bytecode. The primary command is `cage` (`cage.exe` on Windows); `rancage`
remains an alias for systems where `cage` is already used by another
application. The old `.RANCAGE`, `.nvm`, and interim `.rcg` extensions are no
longer accepted by source CLI commands. The VM accepts RANCAGE-IR format
versions 0.1 and 0.2; unsupported format markers are rejected.

## Implemented language features

- Scalar types: `int`, `float`, `bool`, `string`, and `void`
- `fn` functions with typed parameters and return types
- Mutable `let` bindings and immutable `const` bindings
- `if/else`, `while`, `return`, arithmetic, comparisons, equality, and
  boolean operators
- Records with named fields, initialization, field access, and field mutation
- Generic lists (`list[T]`) and maps (`map[string, V]`), including nested
  collection types
- Nullable types (`T?`) and the `null` literal
- List, map, and string indexing
- Intrinsics including `len`, `push`, `pop`, `slice`, `ord`, `chr`,
  `map_has`, and `map_remove`
- Static type checking before code generation
- JSON-based RANCAGE-IR and a bounded reference VM with runtime/resource checks

See [SPEC.md](SPEC.md) for the language specification.

## Tests and verification

Run the source test suite with:

```powershell
.\run-tests.cmd
```

The current suite contains **134 unit, integration, and QA tests**. The Windows
standalone workflow builds one-file and one-folder variants and runs executable
smoke tests. The clean-slate Windows QA run reported 134/134 tests passing and
separately verified the local standalone bundle.

## Security and packaging notes

RANCAGE `.rcb` bytecode is JSON-based and readable/editable. PyInstaller
packaging is a deployment convenience, not obfuscation or tamper protection.
Do not put API keys or secrets in RANCAGE client-side programs. The VM is not a
hardened sandbox for hostile workloads; review [SECURITY.md](SECURITY.md).
Third-party notices are in [THIRD-PARTY-NOTICES.md](THIRD-PARTY-NOTICES.md).

## Licensing

RANCAGE uses a **hybrid licensing model**. The RANCAGE compiler/runtime core
and CAGE executable are proprietary under
[licenses/CORE-PROPRIETARY.txt](licenses/CORE-PROPRIETARY.txt). The license
permits royalty-free use of the official, unmodified CAGE release to create,
compile, test, and run your own RANCAGE programs, including commercial
applications. You may distribute your own programs and `.rcb` output without
royalties, but may not bundle or redistribute the RANCAGE Core itself without
separate written permission.

Only SDK materials explicitly designated as MIT-licensed are covered by
[licenses/SDK-MIT.txt](licenses/SDK-MIT.txt). The current `sdk/` directory is
a draft extension contract, not a stable external ABI or production SDK.
Documentation, examples, tests, specifications, build scripts, and other
repository contents are not automatically covered by the SDK's MIT license.

Public visibility on GitHub does not make RANCAGE Core open-source. GitHub's
Terms of Service permit viewing and forking public repositories through the
GitHub service; those limited platform rights do not grant a general license
to use, modify, or redistribute RANCAGE Core outside those terms. See
[LICENSE](LICENSE) for the licensing map.

## Project status

Stage 0 is complete, closed, and frozen at the clean-slate snapshot tagged
`v0.1.0-alpha.1`. Stage 1 has not started and is not authorized. No native
backend, Android backend, self-hosting compiler, hardened sandbox, or
production platform support is claimed.