"""WebAssembly (.wasm) binary backend for RANCAGE-IR 0.2 (pure Python stdlib).

Supported subset:
- Types: int (i64), float (f64), bool (i32), void
- Control flow: fn calls, if/else, while, for, return
- Operators: arithmetic (+, -, *, /, %), comparisons, equality, boolean (!, &&, ||), unary -
- Host import: print(x) -> env.print_i64 / env.print_f64 / env.print_bool
"""
from __future__ import annotations
import struct
from typing import Any

WASM_MAGIC = b"\x00asm\x01\x00\x00\x00"

TYPE_I32 = 0x7F
TYPE_I64 = 0x7E
TYPE_F64 = 0x7C
BLOCK_VOID = 0x40

SUPPORTED_WASM_TYPES = {
    "int": TYPE_I64,
    "float": TYPE_F64,
    "bool": TYPE_I32,
}

UNSUPPORTED_OPS = {
    "MAKE_LIST", "LIST_GET", "LIST_SET",
    "MAKE_MAP", "MAP_GET", "MAP_SET",
    "MAKE_RECORD", "GET_FIELD", "SET_FIELD",
    "STRING_GET",
    "SETUP_TRY", "POP_TRY", "THROW",
    "BREAK", "CONTINUE",
}


class RancageWasmError(ValueError):
    pass


def _uleb128(value: int) -> bytes:
    if value < 0:
        raise ValueError(f"uleb128 expects non-negative int, got {value}")
    out = bytearray()
    while True:
        byte = value & 0x7F
        value >>= 7
        if value:
            out.append(byte | 0x80)
        else:
            out.append(byte)
            break
    return bytes(out)


def _sleb128(value: int) -> bytes:
    out = bytearray()
    while True:
        byte = value & 0x7F
        value >>= 7
        done = (value == 0 and (byte & 0x40) == 0) or (value == -1 and (byte & 0x40) != 0)
        if not done:
            out.append(byte | 0x80)
        else:
            out.append(byte)
            break
    return bytes(out)


def _encode_str(text: str) -> bytes:
    raw = text.encode("utf-8")
    return _uleb128(len(raw)) + raw


def _encode_vec(items: list[bytes]) -> bytes:
    return _uleb128(len(items)) + b"".join(items)


def _section(section_id: int, payload: bytes) -> bytes:
    return bytes([section_id]) + _uleb128(len(payload)) + payload


def _map_type(type_name: str, context: str) -> int | None:
    if type_name == "void":
        return None
    if type_name in SUPPORTED_WASM_TYPES:
        return SUPPORTED_WASM_TYPES[type_name]
    raise RancageWasmError(
        f"Tipe '{type_name}' pada {context} belum didukung oleh backend WebAssembly"
    )


def _analyze_function(
    fn_name: str,
    fn_ir: dict[str, Any],
    fn_sigs: dict[str, tuple[list[int], int | None]],
) -> tuple[list[int], dict[str, int], dict[int, int], set[int]]:
    """Infer local variable types, stack operand types, and void-call POPs."""
    params: list[str] = fn_ir.get("params", [])
    param_types, _ = fn_sigs[fn_name]
    locals_by_name: dict[str, int] = {}
    local_types: list[int] = []

    for pname, ptype in zip(params, param_types):
        locals_by_name[pname] = len(local_types)
        local_types.append(ptype)

    code: list[list[Any]] = fn_ir.get("code", [])
    stack: list[int | None] = []
    op_types: dict[int, int] = {}
    skip_pops: set[int] = set()

    for pc, instr in enumerate(code):
        op = instr[0]
        if op in UNSUPPORTED_OPS:
            raise RancageWasmError(
                f"Operasi '{op}' di fungsi '{fn_name}' belum didukung oleh backend WebAssembly"
            )
        if op == "PUSH":
            val = instr[1]
            if isinstance(val, bool):
                stack.append(TYPE_I32)
            elif isinstance(val, int):
                stack.append(TYPE_I64)
            elif isinstance(val, float):
                stack.append(TYPE_F64)
            elif val is None:
                stack.append(None)
            else:
                raise RancageWasmError(
                    f"Literal bertipe '{type(val).__name__}' di '{fn_name}' belum didukung oleh backend WebAssembly"
                )
        elif op == "LOAD":
            name = instr[1]
            if name not in locals_by_name:
                raise RancageWasmError(f"Variabel lokal '{name}' belum terdefinisi sebelum LOAD di '{fn_name}'")
            idx = locals_by_name[name]
            stack.append(local_types[idx])
        elif op == "STORE":
            name = instr[1]
            vtype = stack.pop() if stack else TYPE_I64
            if vtype is None:
                raise RancageWasmError(f"Nilai null tidak didukung pada STORE '{name}' di '{fn_name}'")
            if name not in locals_by_name:
                locals_by_name[name] = len(local_types)
                local_types.append(vtype)
            op_types[pc] = vtype
        elif op == "POP":
            if stack:
                stack.pop()
        elif op == "NEG":
            vtype = stack[-1] if stack else TYPE_I64
            if vtype is None:
                vtype = TYPE_I64
            op_types[pc] = vtype
        elif op == "NOT":
            if stack:
                stack.pop()
            stack.append(TYPE_I32)
        elif op in ("ADD", "SUB", "MUL", "DIV", "MOD"):
            rhs = stack.pop() if stack else TYPE_I64
            lhs = stack.pop() if stack else TYPE_I64
            vtype = lhs if lhs is not None else (rhs if rhs is not None else TYPE_I64)
            op_types[pc] = vtype
            stack.append(vtype)
        elif op in ("EQ", "NE", "LT", "LE", "GT", "GE"):
            rhs = stack.pop() if stack else TYPE_I64
            lhs = stack.pop() if stack else TYPE_I64
            vtype = lhs if lhs is not None else (rhs if rhs is not None else TYPE_I64)
            op_types[pc] = vtype
            stack.append(TYPE_I32)
        elif op in ("AND", "OR"):
            if stack:
                stack.pop()
            if stack:
                stack.pop()
            stack.append(TYPE_I32)
        elif op == "JUMP":
            pass
        elif op == "JUMP_IF_FALSE":
            if stack:
                stack.pop()
        elif op == "CALL":
            callee, argc = instr[1], instr[2]
            arg_types = [stack.pop() if stack else TYPE_I64 for _ in range(argc)]
            arg_types.reverse()
            if callee == "print":
                if argc != 1 or arg_types[0] is None:
                    raise RancageWasmError(f"Pemanggilan print di '{fn_name}' membutuhkan 1 argumen numerik/bool")
                op_types[pc] = arg_types[0]
                if pc + 1 < len(code) and code[pc + 1][0] == "POP":
                    skip_pops.add(pc + 1)
            elif callee in fn_sigs:
                _, ret_type = fn_sigs[callee]
                if ret_type is not None:
                    stack.append(ret_type)
                elif pc + 1 < len(code) and code[pc + 1][0] == "POP":
                    skip_pops.add(pc + 1)
            else:
                raise RancageWasmError(
                    f"Intrinsic/fungsi '{callee}' di '{fn_name}' belum didukung oleh backend WebAssembly"
                )
        elif op == "RETURN":
            if stack:
                stack.pop()
        else:
            raise RancageWasmError(f"Opcode '{op}' tidak dikenal oleh backend WebAssembly")

    return local_types, locals_by_name, op_types, skip_pops


def compile_ir_to_wasm(ir: dict[str, Any]) -> bytes:
    """Compile a RANCAGE-IR 0.2 dictionary into a standalone WebAssembly (.wasm) binary."""
    if ir.get("format") != "RANCAGE-IR":
        raise RancageWasmError("Format IR tidak valid untuk backend WebAssembly")

    functions: dict[str, dict[str, Any]] = ir.get("functions", {})
    if not functions:
        raise RancageWasmError("IR tidak memiliki fungsi untuk dikompilasi ke WebAssembly")

    fn_names = list(functions.keys())
    fn_sigs: dict[str, tuple[list[int], int | None]] = {}
    for name in fn_names:
        fn_ir = functions[name]
        params = fn_ir.get("params", [])
        param_type_names = fn_ir.get("param_types") or ["int"] * len(params)
        p_types = []
        for pt in param_type_names:
            mapped = _map_type(pt, f"parameter fungsi '{name}'")
            assert mapped is not None
            p_types.append(mapped)
        ret_type = _map_type(fn_ir.get("return_type", "void"), f"return fungsi '{name}'")
        fn_sigs[name] = (p_types, ret_type)

    analyzed: dict[str, tuple[list[int], dict[str, int], dict[int, int], set[int]]] = {}
    used_prints: set[int] = set()
    for name in fn_names:
        local_types, locals_by_name, op_types, skip_pops = _analyze_function(name, functions[name], fn_sigs)
        analyzed[name] = (local_types, locals_by_name, op_types, skip_pops)
        for pc, instr in enumerate(functions[name].get("code", [])):
            if instr[0] == "CALL" and instr[1] == "print":
                used_prints.add(op_types[pc])

    # Type table deduplication
    type_list: list[tuple[tuple[int, ...], tuple[int, ...]]] = []
    type_index: dict[tuple[tuple[int, ...], tuple[int, ...]], int] = {}

    def intern_type(params_t: list[int], results_t: list[int]) -> int:
        key = (tuple(params_t), tuple(results_t))
        if key not in type_index:
            type_index[key] = len(type_list)
            type_list.append(key)
        return type_index[key]

    # Imports (only used print_* host helpers)
    print_import_specs = [
        (TYPE_I64, "print_i64"),
        (TYPE_F64, "print_f64"),
        (TYPE_I32, "print_bool"),
    ]
    import_entries: list[bytes] = []
    print_fn_idx: dict[int, int] = {}
    for wasm_t, import_name in print_import_specs:
        if wasm_t in used_prints:
            t_idx = intern_type([wasm_t], [])
            print_fn_idx[wasm_t] = len(import_entries)
            import_entries.append(_encode_str("env") + _encode_str(import_name) + b"\x00" + _uleb128(t_idx))

    num_imports = len(import_entries)
    user_fn_idx = {name: num_imports + i for i, name in enumerate(fn_names)}

    fn_type_indices: list[int] = []
    for name in fn_names:
        p_types, ret_type = fn_sigs[name]
        r_types = [ret_type] if ret_type is not None else []
        fn_type_indices.append(intern_type(p_types, r_types))

    # Code bodies
    code_bodies: list[bytes] = []
    for name in fn_names:
        fn_ir = functions[name]
        code = fn_ir.get("code", [])
        local_types, locals_by_name, op_types, skip_pops = analyzed[name]
        p_types, ret_type = fn_sigs[name]
        extra_locals = local_types[len(p_types):]

        body_bytes = _emit_function_body(
            code=code,
            ret_type=ret_type,
            locals_by_name=locals_by_name,
            op_types=op_types,
            skip_pops=skip_pops,
            print_fn_idx=print_fn_idx,
            user_fn_idx=user_fn_idx,
        )

        # Group extra locals by type for compact WASM encoding
        local_groups: list[bytes] = []
        if extra_locals:
            cur_t = extra_locals[0]
            count = 1
            for t in extra_locals[1:]:
                if t == cur_t:
                    count += 1
                else:
                    local_groups.append(_uleb128(count) + bytes([cur_t]))
                    cur_t = t
                    count = 1
            local_groups.append(_uleb128(count) + bytes([cur_t]))

        full_body = _encode_vec(local_groups) + body_bytes + b"\x0B"
        code_bodies.append(_uleb128(len(full_body)) + full_body)

    # Assemble WASM sections
    type_items = [
        b"\x60" + _encode_vec([bytes([t]) for t in p]) + _encode_vec([bytes([t]) for t in r])
        for p, r in type_list
    ]
    out = bytearray(WASM_MAGIC)
    out.extend(_section(1, _encode_vec(type_items)))
    if import_entries:
        out.extend(_section(2, _encode_vec(import_entries)))
    out.extend(_section(3, _encode_vec([_uleb128(ti) for ti in fn_type_indices])))

    exports = [
        _encode_str(name) + b"\x00" + _uleb128(user_fn_idx[name])
        for name in fn_names
    ]
    out.extend(_section(7, _encode_vec(exports)))
    out.extend(_section(10, _encode_vec(code_bodies)))
    return bytes(out)


def _emit_function_body(
    code: list[list[Any]],
    ret_type: int | None,
    locals_by_name: dict[str, int],
    op_types: dict[int, int],
    skip_pops: set[int],
    print_fn_idx: dict[int, int],
    user_fn_idx: dict[str, int],
) -> bytes:
    """Emit structured WebAssembly bytecode from flat RANCAGE-IR instructions."""
    # Identify loops via backward JUMP instructions: (loop_start, jump_pc)
    loops_by_start: dict[int, list[int]] = {}
    for pc, instr in enumerate(code):
        if instr[0] == "JUMP" and instr[1] <= pc:
            loops_by_start.setdefault(instr[1], []).append(pc)
    for starts in loops_by_start.values():
        starts.sort(reverse=True)

    out = bytearray()
    # Active loop stack: list of (exit_target_pc, wasm_block_depth_of_exit_block)
    loop_stack: list[tuple[int, int]] = []
    wasm_depth = 0

    def emit_range(start_pc: int, end_pc: int, active_loop_start: int | None = None) -> None:
        nonlocal wasm_depth
        pc = start_pc
        while pc < end_pc:
            if pc in loops_by_start and pc != active_loop_start:
                # Pick the outermost loop starting at pc that fits inside [start_pc, end_pc)
                matching = [le for le in loops_by_start[pc] if le < end_pc]
                if matching:
                    loop_end = matching[0]
                    exit_depth = wasm_depth
                    out.extend(b"\x02\x40")  # block (void) -> exit target
                    out.extend(b"\x03\x40")  # loop (void) -> continue target
                    wasm_depth += 2
                    loop_stack.append((loop_end + 1, exit_depth))
                    emit_range(pc, loop_end, active_loop_start=pc)
                    # Back-edge jump to loop header (innermost loop block = depth 0)
                    out.extend(b"\x0C\x00")
                    out.extend(b"\x0B\x0B")  # end loop, end block
                    loop_stack.pop()
                    wasm_depth -= 2
                    pc = loop_end + 1
                    continue

            instr = code[pc]
            op = instr[0]

            if op == "JUMP_IF_FALSE":
                target = instr[1]
                if loop_stack and target == loop_stack[-1][0]:
                    exit_depth = loop_stack[-1][1]
                    rel_depth = (wasm_depth - 1) - exit_depth
                    out.append(0x45)  # i32.eqz
                    out.append(0x0D)  # br_if
                    out.extend(_uleb128(rel_depth))
                    pc += 1
                    continue
                # Structured if / else
                has_else = (
                    target - 1 > pc
                    and target - 1 < end_pc
                    and code[target - 1][0] == "JUMP"
                    and code[target - 1][1] >= target
                )
                out.extend(b"\x04\x40")  # if (void)
                wasm_depth += 1
                if has_else:
                    else_end = code[target - 1][1]
                    emit_range(pc + 1, target - 1)
                    out.append(0x05)  # else
                    emit_range(target, else_end)
                    pc = else_end
                else:
                    emit_range(pc + 1, target)
                    pc = target
                out.append(0x0B)  # end if
                wasm_depth -= 1
                continue

            if op == "PUSH":
                val = instr[1]
                if val is None:
                    # Trailing PUSH None + RETURN in non-void function is unreachable
                    if ret_type is not None and pc + 1 < end_pc and code[pc + 1][0] == "RETURN":
                        out.append(0x00)  # unreachable
                        pc += 2
                        continue
                elif isinstance(val, bool):
                    out.append(0x41)  # i32.const
                    out.extend(_sleb128(1 if val else 0))
                elif isinstance(val, int):
                    out.append(0x42)  # i64.const
                    out.extend(_sleb128(val))
                elif isinstance(val, float):
                    out.append(0x44)  # f64.const
                    out.extend(struct.pack("<d", val))
            elif op == "LOAD":
                out.append(0x20)  # local.get
                out.extend(_uleb128(locals_by_name[instr[1]]))
            elif op == "STORE":
                out.append(0x21)  # local.set
                out.extend(_uleb128(locals_by_name[instr[1]]))
            elif op == "POP":
                if pc not in skip_pops:
                    out.append(0x1A)  # drop
            elif op == "NEG":
                if op_types[pc] == TYPE_F64:
                    out.append(0x9A)  # f64.neg
                else:
                    # 0 - x: store not needed if we use local? No, in WASM i64 has no neg opcode!
                    # Emit i64.const -1; i64.mul (equivalent to -x for two's complement)
                    out.append(0x42)
                    out.extend(_sleb128(-1))
                    out.append(0x7E)  # i64.mul
            elif op == "NOT":
                out.append(0x45)  # i32.eqz
            elif op in ("ADD", "SUB", "MUL", "DIV", "MOD"):
                _emit_arith(out, op, op_types[pc])
            elif op in ("EQ", "NE", "LT", "LE", "GT", "GE"):
                _emit_cmp(out, op, op_types[pc])
            elif op == "AND":
                out.append(0x71)  # i32.and
            elif op == "OR":
                out.append(0x72)  # i32.or
            elif op == "CALL":
                callee = instr[1]
                out.append(0x10)  # call
                if callee == "print":
                    out.extend(_uleb128(print_fn_idx[op_types[pc]]))
                else:
                    out.extend(_uleb128(user_fn_idx[callee]))
            elif op == "RETURN":
                out.append(0x0F)  # return
            pc += 1

    emit_range(0, len(code))
    return bytes(out)


def _emit_arith(out: bytearray, op: str, vtype: int) -> None:
    if vtype == TYPE_F64:
        table = {"ADD": 0xA0, "SUB": 0xA1, "MUL": 0xA2, "DIV": 0xA3}
        if op not in table:
            raise RancageWasmError("Operator '%' untuk float belum didukung di WebAssembly")
        out.append(table[op])
    else:
        table = {"ADD": 0x7C, "SUB": 0x7D, "MUL": 0x7E, "DIV": 0x7F, "MOD": 0x81}
        out.append(table[op])


def _emit_cmp(out: bytearray, op: str, vtype: int) -> None:
    if vtype == TYPE_F64:
        table = {"EQ": 0x61, "NE": 0x62, "LT": 0x63, "LE": 0x65, "GT": 0x64, "GE": 0x66}
    elif vtype == TYPE_I32:
        table = {"EQ": 0x46, "NE": 0x47, "LT": 0x48, "LE": 0x4C, "GT": 0x4A, "GE": 0x4E}
    else:
        table = {"EQ": 0x51, "NE": 0x52, "LT": 0x53, "LE": 0x57, "GT": 0x55, "GE": 0x59}
    out.append(table[op])
