"""T1 tests — RANCAGE Terminal interactive full-program runner.

These tests exercise the REPL module directly with injected streams so no real
stdio is required, plus the minimal ``cage repl`` CLI dispatch.
"""
import io
import os
import tempfile
import unittest
from unittest import mock

from rancage import cli
from rancage import vm as vm_module
from rancage.ast import Span
from rancage.compiler import RancageCompilerError
from rancage.repl import (
    BANNER,
    CANCEL_MESSAGE,
    COMMAND_CANCEL,
    COMMAND_EXIT,
    COMMAND_HELP,
    COMMAND_SUBMIT,
    CTRL_C_AGAIN_MESSAGE,
    EMPTY_SUBMIT_MESSAGE,
    EXIT_BLOCKED_MESSAGE,
    EXIT_INTERRUPTED,
    EXIT_MESSAGE,
    INTERRUPT_EXIT_MESSAGE,
    INTERRUPT_MESSAGE,
    LineReader,
    MAX_BUFFER_BYTES,
    ReplSession,
    execute_source,
    run_repl,
)
from rancage.vm import RancageRuntimeError

HELLO = 'fn main() -> int { print("hello"); return 0; }'


class _Harness:
    """Collects session output/error lines."""

    def __init__(self, **kwargs):
        self.out_lines = []
        self.err_lines = []
        self.session = ReplSession(
            out=self.out_lines.append, err=self.err_lines.append, **kwargs
        )

    def feed(self, *lines):
        results = []
        for line in lines:
            results.append(self.session.feed(line))
        return results

    @property
    def out_text(self):
        return "\n".join(self.out_lines)

    @property
    def err_text(self):
        return "\n".join(self.err_lines)


class _ScriptedStdin:
    """Minimal stream: pops queued items; ``KeyboardInterrupt`` sentinel raises."""

    def __init__(self, items):
        self._items = list(items)

    def readline(self):
        if not self._items:
            return ""
        item = self._items.pop(0)
        if item is KeyboardInterrupt:
            raise KeyboardInterrupt
        return item


class ReplBannerAndPromptTests(unittest.TestCase):
    def test_banner_identifies_terminal_and_not_sandbox(self):
        text = "\n".join(BANNER)
        self.assertIn("RANCAGE Terminal", text)
        self.assertIn("Interactive Full-Program Runner", text)
        self.assertIn("Python Reference VM", text)
        self.assertIn("Not a hardened OS sandbox", text)

    def test_prompt_switches_to_continuation_after_first_line(self):
        h = _Harness()
        self.assertEqual(h.session.prompt, ">>> ")
        h.feed("let x: int = 1;")
        self.assertEqual(h.session.prompt, "... ")


class ReplCommandTests(unittest.TestCase):
    def test_help_output(self):
        h = _Harness()
        h.feed(COMMAND_HELP)
        self.assertIn(":submit", h.out_text)
        self.assertIn(":cancel", h.out_text)
        self.assertIn(":exit", h.out_text)
        self.assertIn(str(MAX_BUFFER_BYTES), h.out_text)

    def test_clean_exit(self):
        h = _Harness()
        self.assertFalse(h.feed(COMMAND_EXIT)[0])
        self.assertFalse(h.session.active)
        self.assertIn(EXIT_MESSAGE, h.out_text)

    def test_exit_with_pending_buffer_warns_and_keeps_session(self):
        h = _Harness()
        h.feed("fn main() -> int {", "return 0;", "}")
        pending = h.session.buffer
        self.assertTrue(h.feed(COMMAND_EXIT)[0])
        self.assertTrue(h.session.active)
        self.assertIn(EXIT_BLOCKED_MESSAGE, h.out_text)
        # Buffer is neither discarded nor executed.
        self.assertEqual(h.session.buffer, pending)
        self.assertNotIn("Program selesai", h.out_text)

    def test_cancel_then_exit_succeeds(self):
        h = _Harness()
        h.feed("fn main() -> int { return 0; }")
        h.feed(COMMAND_CANCEL)
        self.assertEqual(h.session.buffer, "")
        self.assertIn(CANCEL_MESSAGE, h.out_text)
        self.assertFalse(h.feed(COMMAND_EXIT)[0])
        self.assertFalse(h.session.active)

    def test_cancel_discards_without_executing(self):
        h = _Harness()
        h.feed(HELLO)
        h.feed(COMMAND_CANCEL)
        self.assertEqual(h.session.buffer, "")
        self.assertNotIn("Program selesai", h.out_text)

    def test_command_lines_do_not_enter_buffer(self):
        h = _Harness()
        h.feed(COMMAND_HELP, COMMAND_CANCEL)
        self.assertEqual(h.session.buffer, "")
        self.assertEqual(h.session.buffer_bytes, 0)

    def test_discard_drops_pending_without_executing(self):
        h = _Harness()
        h.feed(HELLO)
        h.session.discard()
        self.assertEqual(h.session.buffer, "")
        self.assertEqual(h.err_lines, [])
        self.assertNotIn("Program selesai", h.out_text)

    def test_command_requires_exact_whole_line(self):
        h = _Harness()
        h.feed(":help ")
        h.feed(" :help")
        h.feed(":submit now")
        self.assertEqual(h.session.buffer, ":help \n :help\n:submit now")

    def test_command_looking_strings_do_not_trigger_commands(self):
        h = _Harness()
        h.feed('fn main() -> int { print(":exit"); return 0; }')
        self.assertTrue(h.session.active)
        self.assertIn(":exit", h.session.buffer)
        h.feed(COMMAND_SUBMIT)
        self.assertIn("Program selesai dengan kode 0.", h.out_text)


class ReplSubmissionTests(unittest.TestCase):
    def test_multi_line_buffering(self):
        h = _Harness()
        h.feed("fn main() -> int {", '    print("hi");', "    return 0;", "}")
        self.assertEqual(
            h.session.buffer,
            'fn main() -> int {\n    print("hi");\n    return 0;\n}',
        )

    def test_submit_captures_print_output(self):
        h = _Harness()
        h.feed(HELLO, COMMAND_SUBMIT)
        self.assertIn("hello", h.out_lines)
        self.assertIn("Program selesai dengan kode 0.", h.out_text)

    def test_no_automatic_main_wrapping(self):
        h = _Harness()
        h.feed('print("bare");', COMMAND_SUBMIT)
        # Source is submitted verbatim: no implicit `fn main()` wrapper is added,
        # so the top-level statement is rejected by the unchanged parser.
        self.assertIn("SyntaxError", h.err_text)
        self.assertNotIn("bare", h.out_lines)
        self.assertNotIn("Program selesai", h.out_text)

    def test_empty_submission_short_circuits_pipeline(self):
        h = _Harness()
        with mock.patch("rancage.repl.execute_source") as execute:
            h.feed(COMMAND_SUBMIT)
            execute.assert_not_called()
        self.assertIn(EMPTY_SUBMIT_MESSAGE, h.out_text)

    def test_no_vm_state_persists_between_submissions(self):
        h = _Harness(max_steps=150)
        # ~115 steps per submission: passes twice only with a fresh VM each time.
        loop_program = (
            "fn main() -> int { let i: int = 0; while (i < 12) { i = i + 1; } return 0; }"
        )
        h.feed(loop_program, COMMAND_SUBMIT, loop_program, COMMAND_SUBMIT)
        self.assertNotIn("Batas instruksi", h.err_text)
        self.assertEqual(h.out_text.count("Program selesai dengan kode 0."), 2)

    def test_submission_uses_fresh_vm(self):
        created = []
        real_vm = vm_module.VirtualMachine

        def tracking_vm(*args, **kwargs):
            instance = real_vm(*args, **kwargs)
            created.append(instance)
            return instance

        with mock.patch("rancage.repl.VirtualMachine", side_effect=tracking_vm):
            h = _Harness()
            h.feed(HELLO, COMMAND_SUBMIT, HELLO, COMMAND_SUBMIT)
        self.assertEqual(len(created), 2)
        self.assertIsNot(created[0], created[1])


class ReplErrorRecoveryTests(unittest.TestCase):
    def test_syntax_error_recovery(self):
        h = _Harness()
        h.feed("fn main( -> int {", COMMAND_SUBMIT)
        self.assertIn("SyntaxError", h.err_text)
        h.feed(HELLO, COMMAND_SUBMIT)
        self.assertIn("hello", h.out_lines)
        self.assertIn("Program selesai dengan kode 0.", h.out_text)

    def test_type_error_recovery(self):
        h = _Harness()
        h.feed('fn main() -> int { let x: int = "s"; return 0; }', COMMAND_SUBMIT)
        self.assertIn("TypeError", h.err_text)
        h.feed(HELLO, COMMAND_SUBMIT)
        self.assertIn("hello", h.out_lines)

    def test_runtime_error_recovery(self):
        h = _Harness()
        h.feed("fn main() -> int { print(1 / 0); return 0; }", COMMAND_SUBMIT)
        self.assertIn("RuntimeError", h.err_text)
        h.feed(HELLO, COMMAND_SUBMIT)
        self.assertIn("hello", h.out_lines)

    def test_low_step_budget_exhausts_and_reports_runtime_error(self):
        h = _Harness(max_steps=10)
        h.feed("fn main() -> int { let i: int = 0; while (i < 100) { i = i + 1; } return 0; }", COMMAND_SUBMIT)
        self.assertIn("Batas instruksi program terlampaui", h.err_text)
        # Session stays usable after budget exhaustion.
        self.assertTrue(h.session.active)

    def test_buffer_cleared_after_failed_submission(self):
        h = _Harness()
        h.feed("fn main( -> int {", COMMAND_SUBMIT)
        self.assertEqual(h.session.buffer, "")

    def test_unexpected_internal_error_is_not_suppressed(self):
        h = _Harness()
        h.feed(HELLO)
        with mock.patch("rancage.repl.execute_source", side_effect=RuntimeError("boom")):
            with self.assertRaises(RuntimeError):
                h.feed(COMMAND_SUBMIT)


class ReplBufferLimitTests(unittest.TestCase):
    def test_exact_limit_accepted(self):
        h = _Harness()
        h.feed("a" * MAX_BUFFER_BYTES)
        self.assertEqual(h.session.buffer_bytes, MAX_BUFFER_BYTES)
        self.assertEqual(len(h.session.buffer), MAX_BUFFER_BYTES)
        self.assertEqual(h.err_lines, [])

    def test_one_byte_over_limit_rejected(self):
        h = _Harness()
        h.feed("a" * (MAX_BUFFER_BYTES + 1))
        self.assertEqual(h.session.buffer, "")
        self.assertEqual(h.session.buffer_bytes, 0)
        self.assertIn("terlampaui", h.err_text)

    def test_rejection_preserves_previously_accepted_buffer(self):
        h = _Harness()
        h.feed("a" * (MAX_BUFFER_BYTES - 1))
        accepted = h.session.buffer
        h.feed("bb")
        self.assertEqual(h.session.buffer, accepted)
        self.assertIn("terlampaui", h.err_text)

    def test_line_separator_counted_in_limit(self):
        h = _Harness()
        h.feed("a" * MAX_BUFFER_BYTES)
        h.feed("b")
        self.assertEqual(h.session.buffer_bytes, MAX_BUFFER_BYTES)

    def test_truncated_input_is_never_executed(self):
        h = _Harness()
        h.feed(HELLO)
        h.feed("z" * (MAX_BUFFER_BYTES - 1))
        self.assertIn("terlampaui", h.err_text)
        h.feed(COMMAND_SUBMIT)
        self.assertIn("hello", h.out_lines)
        self.assertNotIn("z", h.err_text)

    def test_multibyte_characters_measured_in_utf8_bytes(self):
        h = _Harness()
        # 'é' is two UTF-8 bytes; the buffer holds 2 * count bytes.
        h.feed("é" * (MAX_BUFFER_BYTES // 2))
        self.assertEqual(h.session.buffer_bytes, MAX_BUFFER_BYTES)
        h.feed("a")
        self.assertIn("terlampaui", h.err_text)


class ReplStreamTests(unittest.TestCase):
    def test_eof_with_empty_buffer_exits_cleanly(self):
        stdout, stderr = io.StringIO(), io.StringIO()
        status = run_repl(stdin=_ScriptedStdin([]), stdout=stdout, stderr=stderr)
        self.assertEqual(status, 0)
        self.assertIn("RANCAGE Terminal", stdout.getvalue())

    def test_eof_with_pending_buffer_reports_discard(self):
        stdout, stderr = io.StringIO(), io.StringIO()
        status = run_repl(
            stdin=_ScriptedStdin(["fn main() -> int {"]), stdout=stdout, stderr=stderr
        )
        self.assertEqual(status, 0)
        self.assertIn("EOF", stderr.getvalue())
        self.assertNotIn("Program selesai", stdout.getvalue())

    def test_ctrl_c_cancels_pending_input_and_keeps_session(self):
        stdout, stderr = io.StringIO(), io.StringIO()
        status = run_repl(
            stdin=_ScriptedStdin(
                [HELLO + "\n", KeyboardInterrupt, COMMAND_EXIT + "\n"]
            ),
            stdout=stdout,
            stderr=stderr,
        )
        self.assertEqual(status, 0)
        self.assertIn(INTERRUPT_MESSAGE, stderr.getvalue())
        self.assertIn(CTRL_C_AGAIN_MESSAGE, stderr.getvalue())
        self.assertNotIn("Program selesai", stdout.getvalue())
        self.assertIn(EXIT_MESSAGE, stdout.getvalue())

    def test_repeated_ctrl_c_terminates_session_without_executing(self):
        stdout, stderr = io.StringIO(), io.StringIO()
        status = run_repl(
            stdin=_ScriptedStdin([KeyboardInterrupt, KeyboardInterrupt]),
            stdout=stdout,
            stderr=stderr,
        )
        self.assertEqual(status, EXIT_INTERRUPTED)
        self.assertIn(INTERRUPT_EXIT_MESSAGE, stderr.getvalue())
        self.assertNotIn("Program selesai", stdout.getvalue())

    def test_full_session_transcript(self):
        stdout, stderr = io.StringIO(), io.StringIO()
        status = run_repl(
            stdin=_ScriptedStdin(
                ["fn main() -> int {", '    print("ok");', "    return 0;", "}",
                 COMMAND_SUBMIT, COMMAND_EXIT]
            ),
            stdout=stdout,
            stderr=stderr,
        )
        self.assertEqual(status, 0)
        self.assertIn("ok", stdout.getvalue())
        self.assertIn("Program selesai dengan kode 0.", stdout.getvalue())
        self.assertIn("... ", stdout.getvalue())
        self.assertEqual(stderr.getvalue(), "")


class ReplFilesystemTests(unittest.TestCase):
    def test_normal_operation_creates_no_filesystem_artifacts(self):
        with tempfile.TemporaryDirectory() as workdir:
            previous = os.getcwd()
            os.chdir(workdir)
            try:
                before = sorted(os.listdir(workdir))
                stdout, stderr = io.StringIO(), io.StringIO()
                run_repl(
                    stdin=_ScriptedStdin([HELLO, COMMAND_SUBMIT, COMMAND_EXIT]),
                    stdout=stdout,
                    stderr=stderr,
                )
                after = sorted(os.listdir(workdir))
            finally:
                os.chdir(previous)
            self.assertEqual(before, after)
            self.assertIn("hello", stdout.getvalue())


class ReplPipelineTests(unittest.TestCase):
    def test_execute_source_returns_program_exit_code(self):
        output = []
        status = execute_source("fn main() -> int { print(1); return 7; }", output=output.append)
        self.assertEqual(status, 7)
        self.assertEqual(output, ["1"])

    def test_execute_source_enforces_low_step_budget(self):
        with self.assertRaises(RancageRuntimeError) as ctx:
            execute_source(
                "fn main() -> int { let i: int = 0; while (i < 10) { i = i + 1; } return 0; }",
                output=lambda _: None,
                max_steps=1,
            )
        self.assertIn("Batas instruksi", str(ctx.exception))


class CliReplDispatchTests(unittest.TestCase):
    def test_cli_repl_dispatch(self):
        with mock.patch("rancage.repl.run_repl", return_value=0) as run:
            status = cli.main(["repl"])
        self.assertEqual(status, 0)
        run.assert_called_once()
        self.assertEqual(run.call_args.kwargs["max_steps"], 1_000_000)

    def test_cli_repl_passes_max_steps(self):
        with mock.patch("rancage.repl.run_repl", return_value=0) as run:
            status = cli.main(["repl", "--max-steps", "500"])
        self.assertEqual(status, 0)
        self.assertEqual(run.call_args.kwargs["max_steps"], 500)

    def test_cli_repl_rejects_non_positive_max_steps(self):
        stderr = io.StringIO()
        with mock.patch("sys.stderr", stderr):
            status = cli.main(["repl", "--max-steps", "0"])
        self.assertEqual(status, 2)
        self.assertIn("--max-steps", stderr.getvalue())


class ReplPendingSemanticsTests(unittest.TestCase):
    """Owner decision A-02: pending means UTF-8 byte count > 0."""

    def test_blank_line_is_zero_bytes_and_not_pending(self):
        h = _Harness()
        h.feed("")
        self.assertEqual(h.session.buffer_bytes, 0)
        self.assertFalse(h.session.has_pending)

    def test_blank_line_never_executes(self):
        h = _Harness()
        with mock.patch("rancage.repl.execute_source") as execute:
            h.feed("", COMMAND_SUBMIT)
            execute.assert_not_called()
        self.assertIn(EMPTY_SUBMIT_MESSAGE, h.out_text)

    def test_lone_closing_brace_does_not_execute(self):
        h = _Harness()
        h.feed("}")
        self.assertTrue(h.session.has_pending)
        h.feed(COMMAND_SUBMIT)
        # One byte is pending, so the normal pipeline rejects it as a program.
        self.assertIn("SyntaxError", h.err_text)
        self.assertNotIn("Program selesai", h.out_text)
        self.assertEqual(h.session.buffer_bytes, 0)

    def test_whitespace_only_input_is_pending(self):
        h = _Harness()
        h.feed("   ")
        self.assertEqual(h.session.buffer_bytes, 3)
        self.assertTrue(h.session.has_pending)

    def test_exit_with_whitespace_only_warns_and_preserves(self):
        h = _Harness()
        h.feed("  \t ")
        pending = h.session.buffer
        self.assertTrue(h.feed(COMMAND_EXIT)[0])
        self.assertTrue(h.session.active)
        self.assertIn(EXIT_BLOCKED_MESSAGE, h.out_text)
        self.assertEqual(h.session.buffer, pending)
        self.assertNotIn(EXIT_MESSAGE, h.out_text)

    def test_submit_whitespace_only_runs_normal_pipeline(self):
        h = _Harness()
        h.feed("   ")
        with mock.patch(
            "rancage.repl.execute_source", wraps=execute_source
        ) as execute:
            h.feed(COMMAND_SUBMIT)
            execute.assert_called_once()
        # Parser diagnostic is preserved rather than short-circuited.
        self.assertIn("SyntaxError", h.err_text)
        self.assertNotIn(EMPTY_SUBMIT_MESSAGE, h.out_text)
        # Buffer cleared after the completed attempt.
        self.assertEqual(h.session.buffer_bytes, 0)


class ReplEncodingTests(unittest.TestCase):
    def test_lone_surrogate_rejected_without_mutation(self):
        h = _Harness()
        h.feed("fn main() -> int { return 0; }")
        before_buffer = h.session.buffer
        before_bytes = h.session.buffer_bytes
        h.feed("\ud800")
        self.assertEqual(h.session.buffer, before_buffer)
        self.assertEqual(h.session.buffer_bytes, before_bytes)
        self.assertIn("UTF-8", h.err_text)

    def test_session_usable_after_surrogate_rejection(self):
        h = _Harness()
        h.feed("\udfff")
        self.assertEqual(h.session.buffer_bytes, 0)
        h.feed(HELLO, COMMAND_SUBMIT)
        self.assertIn("hello", h.out_lines)
        self.assertIn("Program selesai dengan kode 0.", h.out_text)


class ReplUtf8BoundaryTests(unittest.TestCase):
    def test_exactly_one_million_bytes_accepted(self):
        h = _Harness()
        # 333_332 three-byte chars (999_996) + one four-byte char == 1_000_000.
        h.feed("漢" * 333_332 + "𐍈")
        self.assertEqual(len(h.session.buffer.encode("utf-8")), MAX_BUFFER_BYTES)
        self.assertEqual(h.session.buffer_bytes, MAX_BUFFER_BYTES)
        self.assertEqual(h.err_lines, [])

    def test_one_million_and_one_bytes_rejected(self):
        h = _Harness()
        h.feed("漢" * 333_332 + "𐍈")
        accepted = h.session.buffer
        h.feed("a")
        self.assertEqual(len(accepted.encode("utf-8")), MAX_BUFFER_BYTES)
        self.assertEqual(h.session.buffer, accepted)
        self.assertEqual(h.session.buffer_bytes, MAX_BUFFER_BYTES)
        self.assertIn("terlampaui", h.err_text)

    def test_rejected_multibyte_input_never_executed(self):
        h = _Harness()
        h.feed(HELLO)
        h.feed("漢" * 333_334)  # 1_000_002 bytes: rejected wholesale.
        self.assertIn("terlampaui", h.err_text)
        h.feed(COMMAND_SUBMIT)
        self.assertIn("hello", h.out_lines)
        self.assertNotIn("漢", h.err_text)


class ReplCompilerDiagnosticTests(unittest.TestCase):
    def test_compiler_location_rendered_exactly_once(self):
        h = _Harness()
        failure = RancageCompilerError(
            "Indexing expression requires inferred type metadata", Span(3, 5)
        )
        h.feed(HELLO)
        with mock.patch("rancage.repl.execute_source", side_effect=failure):
            h.feed(COMMAND_SUBMIT)
        self.assertEqual(h.err_text.count("baris 3, kolom 5"), 1)
        self.assertIn("CompilerError:", h.err_text)
        self.assertIn("Indexing expression requires inferred type metadata", h.err_text)

    def test_compiler_error_without_span_renders_no_location(self):
        h = _Harness()
        failure = RancageCompilerError("internal compiler failure")
        h.feed(HELLO)
        with mock.patch("rancage.repl.execute_source", side_effect=failure):
            h.feed(COMMAND_SUBMIT)
        self.assertIn("CompilerError: internal compiler failure", h.err_text)
        self.assertNotIn("baris", h.err_text)


class ReplStreamContractTests(unittest.TestCase):
    def test_stringio_satisfies_line_reader_protocol(self):
        self.assertIsInstance(io.StringIO(), LineReader)

    def test_scripted_stdin_satisfies_line_reader_protocol(self):
        self.assertIsInstance(_ScriptedStdin([]), LineReader)

    def test_object_without_readline_is_not_a_line_reader(self):
        self.assertNotIsInstance(object(), LineReader)


class CliReplIntegrationTests(unittest.TestCase):
    def test_real_cli_repl_session_end_to_end(self):
        script = (
            'fn main() -> int {\n'
            '    print("cli-ok");\n'
            "    return 0;\n"
            "}\n"
            + COMMAND_SUBMIT
            + "\n"
            + COMMAND_EXIT
            + "\n"
        )
        stdin, stdout, stderr = io.StringIO(script), io.StringIO(), io.StringIO()
        with tempfile.TemporaryDirectory() as workdir:
            previous = os.getcwd()
            os.chdir(workdir)
            try:
                before = sorted(os.listdir(workdir))
                with mock.patch("sys.stdin", stdin), mock.patch(
                    "sys.stdout", stdout
                ), mock.patch("sys.stderr", stderr):
                    status = cli.main(["repl"])
                after = sorted(os.listdir(workdir))
            finally:
                os.chdir(previous)
        self.assertEqual(status, 0)
        self.assertEqual(before, after)
        self.assertIn("RANCAGE Terminal", stdout.getvalue())
        self.assertIn("cli-ok", stdout.getvalue())
        self.assertIn("Program selesai dengan kode 0.", stdout.getvalue())
        self.assertIn(EXIT_MESSAGE, stdout.getvalue())
        self.assertEqual(stderr.getvalue(), "")

    def test_real_cli_repl_forwards_max_steps_to_vm(self):
        captured = []
        real_vm = vm_module.VirtualMachine

        def tracking_vm(*args, **kwargs):
            captured.append(kwargs.get("max_steps"))
            return real_vm(*args, **kwargs)

        script = HELLO + "\n" + COMMAND_SUBMIT + "\n" + COMMAND_EXIT + "\n"
        stdin, stdout, stderr = io.StringIO(script), io.StringIO(), io.StringIO()
        with mock.patch("rancage.repl.VirtualMachine", side_effect=tracking_vm):
            with mock.patch("sys.stdin", stdin), mock.patch(
                "sys.stdout", stdout
            ), mock.patch("sys.stderr", stderr):
                status = cli.main(["repl", "--max-steps", "777"])
        self.assertEqual(status, 0)
        self.assertEqual(captured, [777])


class Stage0PreservationTests(unittest.TestCase):
    def test_vm_limits_unchanged(self):
        self.assertEqual(vm_module.MAX_STEPS, 1_000_000)
        self.assertEqual(vm_module.MAX_DEPTH, 128)
        self.assertEqual(vm_module.MAX_COLLECTION_SIZE, 100_000)
        self.assertEqual(vm_module.MAX_STRING_LENGTH, 1_000_000)

    def test_stage0_pipeline_behaviour_intact(self):
        output = []
        status = execute_source(
            "fn main() -> int { let i: int = 0; while (i < 3) { print(i); i = i + 1; } return 0; }",
            output=output.append,
        )
        self.assertEqual(output, ["0", "1", "2"])
        self.assertEqual(status, 0)


if __name__ == "__main__":
    unittest.main()
