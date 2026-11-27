"""Command-line interface for RANCAGE 0.1."""
from __future__ import annotations
import argparse
import json
import sys
from pathlib import Path
from . import __version__
from .compiler import compile_program
from .lexer import RancageSyntaxError, SUPPORTED_LANGS
from .parser import parse_source
from .resolver import resolve_imports, RancageImportError
from .typesys import RancageTypeError, check_types
from .vm import RancageRuntimeError, VirtualMachine
from .targets import TARGETS
from .wasm_backend import compile_ir_to_wasm, RancageWasmError


def compile_source(path: Path, lang: str = "en") -> dict:
    try:
        source = path.read_text(encoding="utf-8")
    except OSError as exc:
        raise OSError(f"Tidak bisa membaca {path}: {exc}") from exc
    program = parse_source(source, lang=lang)
    program = resolve_imports(program, path.resolve(), lang=lang)
    check_types(program)
    return compile_program(program)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="cage", description="RANCAGE Universal Language — Python reference compiler")
    parser.add_argument("--version", action="version", version=f"RANCAGE {__version__}")
    sub = parser.add_subparsers(dest="command", required=True)
    check = sub.add_parser("check", help="Periksa sintaks dan tipe source RANCAGE")
    check.add_argument("source", type=Path)
    check.add_argument("--lang", choices=SUPPORTED_LANGS, default="en", help="Preset bahasa keyword (default: en)")
    build = sub.add_parser("build", help="Kompilasi source menjadi RANCAGE-IR bytecode (.rcb) atau WebAssembly (.wasm)")
    build.add_argument("source", type=Path)
    build.add_argument("-o", "--output", type=Path)
    build.add_argument("--target", choices=("rcb", "wasm"), default="rcb", help="Target output kompilasi (default: rcb)")
    build.add_argument("--lang", choices=SUPPORTED_LANGS, default="en", help="Preset bahasa keyword (default: en)")
    run = sub.add_parser("run", help="Jalankan source .cage atau bytecode .rcb")
    run.add_argument("program", type=Path)
    run.add_argument("--max-steps", type=int, default=1_000_000)
    run.add_argument("--lang", choices=SUPPORTED_LANGS, default="en", help="Preset bahasa keyword (default: en)")
    repl = sub.add_parser("repl", help="Mulai RANCAGE Terminal (interactive full-program runner)")
    repl.add_argument("--max-steps", type=int, default=1_000_000)
    repl.add_argument("--lang", choices=SUPPORTED_LANGS, default="en", help="Preset bahasa keyword (default: en)")
    sub.add_parser("targets", help="Tampilkan target kompilasi dan status implementasinya")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.command == "repl":
        if args.max_steps < 1:
            print("Error: --max-steps harus lebih besar dari nol", file=sys.stderr)
            return 2
        from .repl import run_repl
        return run_repl(max_steps=args.max_steps, lang=args.lang)
    try:
        if args.command == "check":
            if args.source.suffix.lower() != ".cage":
                print("Error: source harus berekstensi .cage", file=sys.stderr)
                return 2
            compile_source(args.source, lang=args.lang)
            print(f"OK: {args.source} valid (RANCAGE {__version__})")
            return 0
        if args.command == "build":
            if args.source.suffix.lower() != ".cage":
                print("Error: source harus berekstensi .cage", file=sys.stderr)
                return 2
            ir = compile_source(args.source, lang=args.lang)
            if args.target == "wasm":
                wasm_bytes = compile_ir_to_wasm(ir)
                output = args.output or args.source.with_suffix(".wasm")
                output.parent.mkdir(parents=True, exist_ok=True)
                output.write_bytes(wasm_bytes)
            else:
                output = args.output or args.source.with_suffix(".rcb")
                output.parent.mkdir(parents=True, exist_ok=True)
                output.write_text(json.dumps(ir, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            print(f"Built: {output}")
            return 0
        if args.command == "targets":
            print(f"RANCAGE {__version__} target registry (planned != supported):")
            for target_id, name, status, notes in TARGETS:
                print(f"{target_id:12} {status:25} {name} — {notes}")
            return 0
        if args.command == "run":
            if args.max_steps < 1:
                print("Error: --max-steps harus lebih besar dari nol", file=sys.stderr)
                return 2
            if args.program.suffix.lower() == ".cage":
                ir = compile_source(args.program, lang=args.lang)
                vm = VirtualMachine(ir, max_steps=args.max_steps)
            elif args.program.suffix.lower() == ".rcb":
                vm = VirtualMachine.from_file(args.program, max_steps=args.max_steps)
            else:
                print("Error: input harus berekstensi .cage atau .rcb", file=sys.stderr)
                return 2
            return vm.run()
    except RancageSyntaxError as exc:
        print(f"{args.source if hasattr(args, 'source') else args.program}:{exc.line}:{exc.column}: SyntaxError: {exc.message}", file=sys.stderr)
        return 1
    except RancageTypeError as exc:
        print(f"{args.source if hasattr(args, 'source') else args.program}:{exc.span.line}:{exc.span.column}: TypeError: {exc.message}", file=sys.stderr)
        return 1
    except (RancageRuntimeError, OSError, ValueError, RancageImportError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    return 0
