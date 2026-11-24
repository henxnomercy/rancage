"""RANCAGE Terminal T1 — interactive full-program runner.

Each submission is an independent complete RANCAGE program compiled through the
existing pipeline (parse -> type-check -> compile -> reference VM). A fresh
``VirtualMachine`` instance is created for every submission, so no variable,
VM state, or command history survives between submissions.

In-memory only: no history persistence, no filesystem, network, process or
import access. The REPL is not a hardened OS-level sandbox; execution bounds
come from the RANCAGE reference VM (step, depth, allocation limits).
"""
from __future__ import annotations

import sys
from typing import Callable, Protocol, TextIO, runtime_checkable

from .compiler import RancageCompilerError, compile_program
from .lexer import RancageSyntaxError
from .parser import parse_source
from .typesys import RancageTypeError, check_types
from .vm import RancageRuntimeError, VirtualMachine

# REPL input limit (UTF-8 bytes per submission). This is a REPL buffer limit,
# not a change to RANCAGE language string semantics.
MAX_BUFFER_BYTES = 1_000_000

# Default VM step budget; mirrors vm.MAX_STEPS without mutating vm.py.
DEFAULT_MAX_STEPS = 1_000_000

COMMAND_HELP = ":help"
COMMAND_SUBMIT = ":submit"
COMMAND_CANCEL = ":cancel"
COMMAND_EXIT = ":exit"

# Commands are recognised only when the whole input line equals one of these.
COMMANDS = frozenset((COMMAND_HELP, COMMAND_SUBMIT, COMMAND_CANCEL, COMMAND_EXIT))

BANNER = (
    "RANCAGE Terminal",
    "Interactive Full-Program Runner",
    "Python Reference VM",
    "Not a hardened OS sandbox.",
    "Ketik :help untuk daftar perintah.",
)

PROMPT_PRIMARY = ">>> "
PROMPT_CONTINUE = "... "

EXIT_MESSAGE = "Sesi berakhir."
CANCEL_MESSAGE = "Buffer dikosongkan."
EMPTY_SUBMIT_MESSAGE = "Buffer kosong; tidak ada program untuk dijalankan."
EXIT_BLOCKED_MESSAGE = "Buffer masih berisi program. Gunakan :cancel lalu :exit."
INTERRUPT_MESSAGE = "Dibatalkan; buffer dikosongkan."
EOF_PENDING_MESSAGE = "EOF: buffer tidak kosong; buffer dibuang tanpa dijalankan."
EOF_MESSAGE = "EOF: sesi berakhir."

HELP_LINES = (
    "Perintah (harus tepat satu baris penuh):",
    "  :help    tampilkan bantuan ini",
    "  :submit  kompilasi dan jalankan buffer sebagai satu program",
    "  :cancel  kosongkan buffer tanpa menjalankan",
    "  :exit    keluar (hanya bila buffer kosong)",
    "Baris lain ditambahkan ke buffer program.",
    f"Batas buffer: {MAX_BUFFER_BYTES} byte UTF-8 per pengiriman.",
)

# Exit status used when the session is ended by repeated Ctrl+C.
EXIT_INTERRUPTED = 130

CTRL_C_AGAIN_MESSAGE = "Ctrl+C lagi untuk keluar; buffer sudah dikosongkan."
INTERRUPT_EXIT_MESSAGE = "Dibatalkan. Sesi berakhir."


@runtime_checkable
class LineReader(Protocol):
    """Minimal text stream contract required by :func:`run_repl`.

    Only ``readline()`` is used. ``readline()`` returning ``""`` means EOF;
    raising ``KeyboardInterrupt`` signals Ctrl+C. ``io.StringIO`` satisfies this
    protocol, so tests can inject in-memory streams.
    """

    def readline(self) -> str:  # pragma: no cover - protocol declaration
        ...


def _utf8_len(text: str) -> int | None:
    """Return UTF-8 byte length, or None when the text is not encodable."""
    try:
        return len(text.encode("utf-8"))
    except UnicodeEncodeError:
        return None


def execute_source(
    source: str,
    output: Callable[[str], None] = print,
    max_steps: int = DEFAULT_MAX_STEPS,
) -> int:
    """Compile and run one complete program on a fresh virtual machine."""
    program = parse_source(source)
    check_types(program)
    ir = compile_program(program)
    vm = VirtualMachine(ir, output=output, max_steps=max_steps)
    return vm.run()


class ReplSession:
    """Stateful source buffer plus command handling.

    The session owns no host capabilities: output and diagnostics are injected
    callables, and execution is delegated to :func:`execute_source`.
    """

    def __init__(
        self,
        out: Callable[[str], None] = print,
        err: Callable[[str], None] | None = None,
        max_steps: int = DEFAULT_MAX_STEPS,
    ):
        self._out = out
        self._err = out if err is None else err
        self.max_steps = max_steps
        self._lines: list[str] = []
        self._byte_count = 0
        self.active = True

    # -- observable buffer state ------------------------------------------
    @property
    def buffer(self) -> str:
        """Accumulated source, lines joined by ``\\n`` (no trailing newline)."""
        return "\n".join(self._lines)

    @property
    def buffer_bytes(self) -> int:
        return self._byte_count

    @property
    def has_pending(self) -> bool:
        # Owner decision A-02: any non-zero byte count is pending, including
        # whitespace-only input. Zero bytes short-circuits the pipeline.
        return self._byte_count > 0

    @property
    def prompt(self) -> str:
        return PROMPT_CONTINUE if self._lines else PROMPT_PRIMARY

    # -- command dispatch --------------------------------------------------
    def feed(self, line: str) -> bool:
        """Handle one input line. Return True while the session continues."""
        text = line.rstrip("\r\n")
        if text not in COMMANDS:
            self._append(text)
            return True
        if text == COMMAND_HELP:
            for help_line in HELP_LINES:
                self._out(help_line)
            return True
        if text == COMMAND_SUBMIT:
            self._submit()
            return True
        if text == COMMAND_CANCEL:
            self._cancel()
            return True
        self._exit()
        return self.active

    def discard(self) -> None:
        """Drop pending input without executing it or emitting a hint."""
        self._lines = []
        self._byte_count = 0

    def interrupt(self) -> None:
        """Discard pending input after Ctrl+C; buffer is never executed."""
        self.discard()
        self._err(INTERRUPT_MESSAGE)

    # -- buffer -----------------------------------------------------------
    def _append(self, text: str) -> None:
        line_bytes = _utf8_len(text)
        if line_bytes is None:
            self._err("Error: baris masukan bukan teks UTF-8 valid; baris ditolak.")
            return
        # Existing content is preserved when a new line is rejected.
        separator = 1 if self._lines else 0
        candidate = self._byte_count + separator + line_bytes
        if candidate > MAX_BUFFER_BYTES:
            self._err(
                f"Error: batas buffer {MAX_BUFFER_BYTES} byte terlampaui; baris ditolak. "
                "Gunakan :cancel untuk mengosongkan buffer."
            )
            return
        self._lines.append(text)
        self._byte_count = candidate

    def _cancel(self) -> None:
        self.discard()
        self._out(CANCEL_MESSAGE)

    def _exit(self) -> None:
        if self.has_pending:
            # Warning only: buffer is neither executed nor discarded.
            self._out(EXIT_BLOCKED_MESSAGE)
            return
        self.discard()
        self.active = False
        self._out(EXIT_MESSAGE)

    # -- execution --------------------------------------------------------
    def _submit(self) -> None:
        if not self.has_pending:
            self._out(EMPTY_SUBMIT_MESSAGE)
            return
        source = self.buffer
        try:
            status = execute_source(source, output=self._out, max_steps=self.max_steps)
        except RancageSyntaxError as exc:
            self._err(f"SyntaxError: line {exc.line}, column {exc.column}: {exc.message}")
        except RancageTypeError as exc:
            self._err(
                f"TypeError: line {exc.span.line}, column {exc.span.column}: {exc.message}"
            )
        except RancageCompilerError as exc:
            # The exception's original text already embeds "(baris N, kolom M)"
            # when a span exists, so the location must not be prefixed again.
            self._err(f"CompilerError: {exc}")
        except RancageRuntimeError as exc:
            self._err(f"RuntimeError: {exc}")
        else:
            self._out(f"Program selesai dengan kode {status}.")
        # Every submission is independent: the buffer is always cleared once
        # the attempt finishes, regardless of the outcome.
        self.discard()


def run_repl(
    stdin: LineReader | None = None,
    stdout: TextIO | None = None,
    stderr: TextIO | None = None,
    max_steps: int = DEFAULT_MAX_STEPS,
) -> int:
    """Run an interactive RANCAGE session against the given streams."""
    stdin = sys.stdin if stdin is None else stdin
    stdout = sys.stdout if stdout is None else stdout
    stderr = sys.stderr if stderr is None else stderr

    def out(text: str) -> None:
        print(text, file=stdout)

    def err(text: str) -> None:
        print(text, file=stderr)

    for banner_line in BANNER:
        out(banner_line)

    session = ReplSession(out=out, err=err, max_steps=max_steps)
    consecutive_interrupts = 0
    while session.active:
        stdout.write(session.prompt)
        stdout.flush()
        try:
            line = stdin.readline()
        except KeyboardInterrupt:
            # Ctrl+C never executes pending input; the session stays usable.
            consecutive_interrupts += 1
            session.interrupt()
            if consecutive_interrupts >= 2:
                err(INTERRUPT_EXIT_MESSAGE)
                return EXIT_INTERRUPTED
            err(CTRL_C_AGAIN_MESSAGE)
            continue
        consecutive_interrupts = 0
        if line == "":
            if session.has_pending:
                err(EOF_PENDING_MESSAGE)
            else:
                out(EOF_MESSAGE)
            session.discard()
            return 0
        if not session.feed(line):
            return 0
    return 0
