"""Module resolver for RANCAGE: resolves import chains into a single merged Program.

Design:
- import "path.cage";   (EN)  |  mawa "path.cage";   (SU)
- Paths are relative to the importing file's directory.
- All fn and record declarations from imported files are merged into the caller's
  Program before type-checking and compilation.  main() in imported files is
  silently skipped (not merged) so the entry point stays unique.
- Bounded: max import depth = 16, cycle detection via canonical path set.
- Only the Python standard library is used.
"""
from __future__ import annotations
from pathlib import Path
from .ast import Program, Function, RecordDecl, ImportDecl
from .lexer import RancageSyntaxError
from .parser import parse_source

MAX_IMPORT_DEPTH = 16


class RancageImportError(Exception):
    pass


def resolve_imports(
    root_program: Program,
    root_path: Path | None,
    lang: str = "en",
    _visited: frozenset[str] | None = None,
    _depth: int = 0,
) -> Program:
    """Return a new Program with all imported functions and records merged in.

    Args:
        root_program: The already-parsed program (may contain ImportDecl nodes).
        root_path:    Absolute path to the file that was parsed, or None for
                      in-memory/REPL sources (imports are disallowed then).
        lang:         Keyword preset forwarded to the lexer of imported files.
        _visited:     Internal: set of canonical resolved paths already on the stack.
        _depth:       Internal: current import nesting depth.
    """
    if not root_program.imports:
        return root_program

    if root_path is None:
        imp = root_program.imports[0]
        raise RancageImportError(
            f"Import tidak didukung dari sumber in-memory: {imp.path!r}"
        )

    if _depth > MAX_IMPORT_DEPTH:
        raise RancageImportError(
            f"Batas kedalaman import ({MAX_IMPORT_DEPTH}) terlampaui"
        )

    if _visited is None:
        _visited = frozenset([str(root_path.resolve())])

    merged_fns: list[Function] = []
    merged_recs: list[RecordDecl] = []
    seen_fn_names: set[str] = set()
    seen_rec_names: set[str] = set()

    # Process imports first (depth-first), so the caller's definitions shadow
    # any same-named imported definitions — but we report duplicate names as an error.
    for imp in root_program.imports:
        # Resolve path relative to the importing file's directory
        raw = imp.path
        if Path(raw).is_absolute():
            target = Path(raw)
        else:
            target = (root_path.parent / raw).resolve()

        if not target.exists():
            raise RancageImportError(
                f"File import tidak ditemukan: {raw!r} "
                f"(dicari di: {target})"
            )
        if target.suffix.lower() != ".cage":
            raise RancageImportError(
                f"File import harus berekstensi .cage: {raw!r}"
            )

        canonical = str(target)
        if canonical in _visited:
            raise RancageImportError(
                f"Impor siklikal terdeteksi: {raw!r} sudah ada di rantai impor saat ini"
            )

        try:
            source_text = target.read_text(encoding="utf-8")
        except OSError as exc:
            raise RancageImportError(f"Tidak bisa membaca file import {raw!r}: {exc}") from exc

        try:
            imported_prog = parse_source(source_text, lang=lang)
        except RancageSyntaxError as exc:
            raise RancageImportError(
                f"Kesalahan sintaks di file import {raw!r} "
                f"(baris {exc.line}, kolom {exc.column}): {exc.message}"
            ) from exc

        # Recursively resolve imports in the imported file
        imported_prog = resolve_imports(
            imported_prog,
            target,
            lang=lang,
            _visited=_visited | {canonical},
            _depth=_depth + 1,
        )

        # Merge records (skip duplicates from same file; error on name clash across imports)
        for rec in imported_prog.records:
            if rec.name not in seen_rec_names:
                merged_recs.append(rec)
                seen_rec_names.add(rec.name)

        # Merge functions — skip main() from imported files; error on duplicate names
        for fn in imported_prog.functions:
            if fn.name == "main":
                continue  # entry-point from imported files is excluded
            if fn.name in seen_fn_names:
                raise RancageImportError(
                    f"Nama fungsi '{fn.name}' dari {raw!r} sudah ada dari impor sebelumnya"
                )
            merged_fns.append(fn)
            seen_fn_names.add(fn.name)

    # Now add the root program's own declarations
    for rec in root_program.records:
        if rec.name in seen_rec_names:
            raise RancageImportError(
                f"Nama record '{rec.name}' di file ini bentrok dengan nama record dari impor"
            )
        merged_recs.append(rec)
        seen_rec_names.add(rec.name)

    for fn in root_program.functions:
        if fn.name in seen_fn_names and fn.name != "main":
            raise RancageImportError(
                f"Nama fungsi '{fn.name}' di file ini bentrok dengan fungsi dari impor"
            )
        merged_fns.append(fn)
        seen_fn_names.add(fn.name)

    return Program(
        functions=merged_fns,
        module=root_program.module,
        records=merged_recs,
        imports=[],  # imports already resolved; clear so downstream sees no ImportDecl
    )
