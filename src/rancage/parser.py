"""Recursive-descent parser and Pratt expression parser for RANCAGE 0.1."""
from __future__ import annotations
from .ast import *
from .lexer import Lexer, Token, RancageSyntaxError, KEYWORDS, RESERVED, CANONICAL_KEYWORDS

PRECEDENCE = {"||": 1, "&&": 2, "==": 3, "!=": 3, "<": 4, "<=": 4, ">": 4, ">=": 4,
              "+": 5, "-": 5, "*": 6, "/": 6, "%": 6}

class Parser:
    def __init__(self, tokens: list[Token], lang: str = "en"):
        self.tokens = tokens
        self.lang = lang
        self.i = 0

    def current(self) -> Token:
        return self.tokens[self.i]

    def _canon(self, tok: Token) -> str:
        if tok.kind in CANONICAL_KEYWORDS:
            return CANONICAL_KEYWORDS[tok.kind]
        if tok.kind == "IDENT":
            # EN-mode: keywords emitted as IDENT matched by value
            if tok.value in ("import", "try", "catch", "throw", "break", "continue"):
                return tok.value
            return tok.value
        if tok.kind == "SYMBOL":
            return tok.value
        return ""

    def check(self, value: str) -> bool:
        return self._canon(self.current()) == value

    def advance(self) -> Token:
        tok = self.current()
        if tok.kind != "EOF": self.i += 1
        return tok

    def match(self, value: str) -> bool:
        if self.check(value):
            self.advance(); return True
        return False

    def expect(self, value: str, message: str | None = None) -> Token:
        if self.check(value): return self.advance()
        tok = self.current()
        raise RancageSyntaxError(message or f"Diharapkan {value!r}, ditemukan {tok.value!r}", tok.line, tok.column)

    def identifier(self, message: str = "Diharapkan nama identifier") -> Token:
        tok = self.current()
        if tok.kind != "IDENT" or tok.value in RESERVED:
            raise RancageSyntaxError(message, tok.line, tok.column)
        return self.advance()

    def type_expr(self, depth: int = 0) -> str:
        if depth > 64:
            tok = self.current()
            raise RancageSyntaxError("Batas kedalaman tipe terlampaui", tok.line, tok.column)
        if self.match("list"):
            self.expect("[")
            elem_type = self.type_expr(depth + 1)
            self.expect("]")
            base = f"list[{elem_type}]"
        elif self.match("map"):
            self.expect("[")
            key_tok = self.identifier("Diharapkan 'string' sebagai key map")
            if key_tok.value != "string":
                raise RancageSyntaxError("Key map saat ini hanya mendukung 'string'", key_tok.line, key_tok.column)
            self.expect(",")
            val_type = self.type_expr(depth + 1)
            self.expect("]")
            base = f"map[string, {val_type}]"
        else:
            base = self.identifier("Diharapkan tipe").value
        if self.match("?"):
            base = f"{base}?"
        return base

    def record_decl(self) -> RecordDecl:
        start = self.expect("record")
        name = self.identifier("Diharapkan nama record")
        self.expect("{")
        fields = []
        while not self.check("}"):
            if self.current().kind == "EOF":
                tok = self.current()
                raise RancageSyntaxError("Blok record tidak ditutup dengan '}'", tok.line, tok.column)
            f_name = self.identifier("Diharapkan nama field record")
            self.expect(":")
            f_type = self.type_expr()
            self.expect(";")
            fields.append(FieldDecl(f_name.value, f_type, Span(f_name.line, f_name.column)))
        self.expect("}")
        return RecordDecl(name.value, fields, Span(start.line, start.column))

    def parse(self) -> Program:
        module = "main"
        if self.match("module"):
            module = self.identifier("Diharapkan nama module").value
            self.expect(";")
        functions = []
        records = []
        imports = []
        while self.current().kind != "EOF":
            if self.check("record"):
                records.append(self.record_decl())
            elif self.check("fn"):
                functions.append(self.function())
            elif self.check("import"):
                tok = self.current()
                self.advance()
                path_tok = self.current()
                if path_tok.kind != "STRING":
                    raise RancageSyntaxError("import membutuhkan path string literal", path_tok.line, path_tok.column)
                self.advance()
                self.expect(";")
                imports.append(ImportDecl(path_tok.value, Span(tok.line, tok.column)))
            else:
                tok = self.current()
                raise RancageSyntaxError("Program tingkat atas hanya boleh berisi deklarasi record, fn, atau import", tok.line, tok.column)
        # A file with nothing at all is an error. A library file (records only,
        # or functions only, or both) is valid; main() is required only by the
        # type-checker when the file is the entry point.
        if not functions and not imports and not records:
            tok = self.current()
            raise RancageSyntaxError("Program harus memiliki minimal satu deklarasi (fn, record, atau import)", tok.line, tok.column)
        return Program(functions, module, records, imports)

    def function(self) -> Function:
        start = self.expect("fn", "Program tingkat atas hanya boleh berisi deklarasi fn")
        name = self.identifier("Diharapkan nama fungsi")
        self.expect("(")
        params = []
        if not self.check(")"):
            while True:
                p = self.identifier("Diharapkan nama parameter")
                self.expect(":")
                t = self.type_expr()
                params.append(Param(p.value, t, Span(p.line, p.column)))
                if not self.match(","): break
                if self.check(")"): break
        self.expect(")")
        self.expect("->", "Diharapkan '->' sebelum tipe return")
        ret = self.type_expr()
        body = self.block()
        return Function(name.value, params, ret, body, Span(start.line, start.column))

    def block(self) -> list[Stmt]:
        self.expect("{")
        body = []
        while not self.check("}"):
            if self.current().kind == "EOF":
                tok = self.current(); raise RancageSyntaxError("Blok tidak ditutup dengan '}'", tok.line, tok.column)
            body.append(self.statement())
        self.expect("}")
        return body

    def _let_or_const(self, start_tok: Token) -> Let:
        is_const = self._canon(start_tok) == "const"
        name = self.identifier("Diharapkan nama variabel")
        type_name = None
        if self.match(":"):
            type_name = self.type_expr()
        self.expect("=", "Deklarasi variabel harus memiliki nilai awal")
        value = self.expression()
        return Let(name.value, type_name, value, is_const, Span(start_tok.line, start_tok.column))

    def _assign_or_expr(self) -> Stmt:
        target = self.expression()
        if self.match("="):
            value = self.expression()
            if isinstance(target, Name):
                return Assign(target.value, value, Span(target.span.line, target.span.column))
            if isinstance(target, FieldAccess):
                return FieldAssign(target.target, target.field, value, Span(target.span.line, target.span.column))
            if isinstance(target, IndexExpr):
                return IndexAssign(target.target, target.index, value, Span(target.span.line, target.span.column))
            raise RancageSyntaxError("Target penugasan tidak valid", target.span.line, target.span.column)
        return ExprStmt(target, Span(target.span.line, target.span.column))

    def statement(self) -> Stmt:
        tok = self.current()
        if self.match("let") or self.match("const"):
            stmt = self._let_or_const(self.tokens[self.i - 1])
            self.expect(";")
            return stmt
        if self.match("return"):
            value = None if self.check(";") else self.expression()
            self.expect(";")
            return Return(value, Span(tok.line, tok.column))
        if self.match("if"):
            self.expect("(")
            condition = self.expression()
            self.expect(")")
            then_body = self.block()
            else_body = self.block() if self.match("else") else None
            return If(condition, then_body, else_body, Span(tok.line, tok.column))
        if self.match("while"):
            self.expect("(")
            condition = self.expression()
            self.expect(")")
            return While(condition, self.block(), Span(tok.line, tok.column))
        if self.match("try"):
            try_body = self.block()
            self.expect("catch", "Diharapkan 'catch' setelah blok 'try'")
            self.expect("(")
            err_tok = self.identifier("Diharapkan nama variabel error")
            err_type = "string"
            if self.match(":"):
                err_type = self.type_expr()
            self.expect(")")
            catch_body = self.block()
            return TryCatch(try_body, err_tok.value, err_type, catch_body, Span(tok.line, tok.column))
        if self.match("throw"):
            val = self.expression()
            self.expect(";")
            return Throw(val, Span(tok.line, tok.column))
        if self.match("break"):
            self.expect(";")
            return Break(Span(tok.line, tok.column))
        if self.match("continue"):
            self.expect(";")
            return Continue(Span(tok.line, tok.column))
        if self.match("for"):
            self.expect("(")
            init: Stmt | None = None
            if not self.match(";"):
                if self.match("let") or self.match("const"):
                    init = self._let_or_const(self.tokens[self.i - 1])
                else:
                    init = self._assign_or_expr()
                self.expect(";")
            condition: Expr | None = None
            if not self.match(";"):
                condition = self.expression()
                self.expect(";")
            step: Stmt | None = None
            if not self.check(")"):
                step = self._assign_or_expr()
            self.expect(")")
            return For(init, condition, step, self.block(), Span(tok.line, tok.column))
        stmt = self._assign_or_expr()
        self.expect(";")
        return stmt

    def expression(self, min_prec: int = 1) -> Expr:
        tok = self.advance()
        if tok.value in ("!", "-"):
            left: Expr = Unary(tok.value, self.expression(7), Span(tok.line, tok.column))
        elif tok.value == "(":
            left = self.expression()
            self.expect(")")
        elif tok.kind == "INT":
            left = Literal(int(tok.value), "int", Span(tok.line, tok.column))
        elif tok.kind == "FLOAT":
            left = Literal(float(tok.value), "float", Span(tok.line, tok.column))
        elif tok.kind == "STRING":
            left = Literal(tok.value, "string", Span(tok.line, tok.column))
        elif tok.kind in ("TRUE", "FALSE") or (tok.kind == "IDENT" and tok.value in ("true", "false")):
            left = Literal(self._canon(tok) == "true", "bool", Span(tok.line, tok.column))
        elif tok.kind == "NULL" or (tok.kind == "IDENT" and tok.value == "null"):
            left = NullLiteral(Span(tok.line, tok.column))
        elif tok.kind in CANONICAL_KEYWORDS:
            raise RancageSyntaxError(f"Keyword '{tok.value}' tidak bisa digunakan dalam ekspresi", tok.line, tok.column)
        elif tok.value == "[":
            elements = []
            if not self.check("]"):
                while True:
                    elements.append(self.expression())
                    if not self.match(","): break
                    if self.check("]"): break
            self.expect("]")
            left = ListLiteral(elements, Span(tok.line, tok.column))
        elif tok.value == "{":
            entries = []
            if not self.check("}"):
                while True:
                    key = self.expression()
                    self.expect(":")
                    val = self.expression()
                    entries.append((key, val))
                    if not self.match(","): break
                    if self.check("}"): break
            self.expect("}")
            left = MapLiteral(entries, Span(tok.line, tok.column))
        elif tok.kind == "IDENT":
            if tok.value in KEYWORDS:
                raise RancageSyntaxError(f"Keyword '{tok.value}' tidak bisa digunakan dalam ekspresi", tok.line, tok.column)
            if self.match("("):
                args = []
                if not self.check(")"):
                    while True:
                        args.append(self.expression())
                        if not self.match(","): break
                        if self.check(")"): break
                self.expect(")")
                call_name = "print" if (self.lang == "su" and tok.value == "citak") else tok.value
                left = Call(call_name, args, Span(tok.line, tok.column))
            elif self.match("{"):
                fields = []
                if not self.check("}"):
                    while True:
                        fname = self.identifier("Diharapkan nama field")
                        self.expect(":")
                        fval = self.expression()
                        fields.append(FieldInit(fname.value, fval, Span(fname.line, fname.column)))
                        if not self.match(","): break
                        if self.check("}"): break
                self.expect("}")
                left = RecordInit(tok.value, fields, Span(tok.line, tok.column))
            else:
                left = Name(tok.value, Span(tok.line, tok.column))
        else:
            raise RancageSyntaxError(f"Diharapkan ekspresi, ditemukan {tok.value!r}", tok.line, tok.column)
        while True:
            if self.match("."):
                field_tok = self.identifier("Diharapkan nama field")
                left = FieldAccess(left, field_tok.value, Span(field_tok.line, field_tok.column))
            elif self.check("["):
                bracket_tok = self.advance()
                idx = self.expression()
                self.expect("]")
                left = IndexExpr(left, idx, Span(bracket_tok.line, bracket_tok.column))
            else:
                break
        while True:
            op = self.current().value
            prec = PRECEDENCE.get(op, 0)
            if prec < min_prec: break
            op_tok = self.advance()
            right = self.expression(prec + 1)
            left = Binary(left, op_tok.value, right, Span(op_tok.line, op_tok.column))
        return left


def parse_source(source: str, lang: str = "en") -> Program:
    return Parser(Lexer(source, lang=lang).tokenize(), lang=lang).parse()
