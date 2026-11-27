"""Lexer for the RANCAGE language."""
from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class Token:
    kind: str
    value: str
    line: int
    column: int

class RancageSyntaxError(Exception):
    def __init__(self, message: str, line: int, column: int):
        super().__init__(message)
        self.message, self.line, self.column = message, line, column

SINGLE = set("{}():,;+-*/%=<>![]?.")
DOUBLE = {"->", "==", "!=", "<=", ">=", "&&", "||"}
SUPPORTED_LANGS = ("en", "su")

KEYWORDS_EN = {
    "module": "MODULE",
    "import": "IMPORT",
    "fn": "FN",
    "let": "LET",
    "const": "CONST",
    "return": "RETURN",
    "if": "IF",
    "else": "ELSE",
    "while": "WHILE",
    "for": "FOR",
    "record": "RECORD",
    "try": "TRY",
    "catch": "CATCH",
    "throw": "THROW",
    "break": "BREAK",
    "continue": "CONTINUE",
}
LITERALS_EN = {"true": "TRUE", "false": "FALSE", "null": "NULL"}

KEYWORDS_SU = {
    "modul": "MODULE",
    "mawa": "IMPORT",
    "pungsi": "FN",
    "pasang": "LET",
    "tetep": "CONST",
    "balik": "RETURN",
    "lamun": "IF",
    "lain": "ELSE",
    "salila": "WHILE",
    "pikeun": "FOR",
    "wangun": "RECORD",
    "coba": "TRY",
    "tewak": "CATCH",
    "balang": "THROW",
    "eureun": "BREAK",
    "tuluy": "CONTINUE",
}
LITERALS_SU = {"bener": "TRUE", "salah": "FALSE", "kosong": "NULL"}

CANONICAL_KEYWORDS = {
    "MODULE": "module",
    "IMPORT": "import",
    "FN": "fn",
    "LET": "let",
    "CONST": "const",
    "RETURN": "return",
    "IF": "if",
    "ELSE": "else",
    "WHILE": "while",
    "FOR": "for",
    "RECORD": "record",
    "TRY": "try",
    "CATCH": "catch",
    "THROW": "throw",
    "BREAK": "break",
    "CONTINUE": "continue",
    "TRUE": "true",
    "FALSE": "false",
    "NULL": "null",
}

KEYWORDS = set(KEYWORDS_EN)
RESERVED = KEYWORDS | set(LITERALS_EN)
# In EN mode the lexer emits "import" as IDENT (since EN uses KEYWORDS dict only in parser).
# In SU mode the lexer emits kind="IMPORT" for "mawa".
# Either way, _canon() on the parser side maps kind IMPORT -> "import",
# and check("import") also matches IDENT tokens whose value is "import".


class Lexer:
    def __init__(self, source: str, lang: str = "en"):
        if lang not in SUPPORTED_LANGS:
            raise ValueError(f"Preset bahasa tidak didukung: {lang!r}")
        self.source = source
        self.lang = lang
        self.keywords_map = KEYWORDS_EN if lang == "en" else KEYWORDS_SU
        self.literals_map = LITERALS_EN if lang == "en" else LITERALS_SU
        self.i = 0
        self.line = 1
        self.column = 1
        self.tokens: list[Token] = []

    def _peek(self, offset: int = 0) -> str:
        p = self.i + offset
        return self.source[p] if p < len(self.source) else "\0"

    def _advance(self) -> str:
        ch = self._peek()
        if ch == "\0":
            return ch
        self.i += 1
        if ch == "\n":
            self.line += 1
            self.column = 1
        else:
            self.column += 1
        return ch

    def _add(self, kind: str, value: str, line: int, column: int) -> None:
        self.tokens.append(Token(kind, value, line, column))

    def tokenize(self) -> list[Token]:
        while self._peek() != "\0":
            ch = self._peek()
            if ch in " \t\r\n":
                self._advance()
                continue
            if ch == "/" and self._peek(1) == "/":
                while self._peek() not in ("\n", "\0"):
                    self._advance()
                continue
            if ch == "/" and self._peek(1) == "*":
                start_line, start_col = self.line, self.column
                self._advance(); self._advance()
                while not (self._peek() == "*" and self._peek(1) == "/"):
                    if self._peek() == "\0":
                        raise RancageSyntaxError("Komentar blok tidak ditutup", start_line, start_col)
                    self._advance()
                self._advance(); self._advance()
                continue
            line, col = self.line, self.column
            if ch.isalpha() or ch == "_":
                chars = []
                while self._peek().isalnum() or self._peek() == "_":
                    chars.append(self._advance())
                word = "".join(chars)
                if self.lang == "su":
                    kind = self.keywords_map.get(word) or self.literals_map.get(word) or "IDENT"
                else:
                    kind = "IDENT"
                self._add(kind, word, line, col)
                continue
            if ch.isdigit():
                chars = []
                while self._peek().isdigit():
                    chars.append(self._advance())
                kind = "INT"
                if self._peek() == "." and self._peek(1).isdigit():
                    kind = "FLOAT"
                    chars.append(self._advance())
                    while self._peek().isdigit():
                        chars.append(self._advance())
                self._add(kind, "".join(chars), line, col)
                continue
            if ch == '"':
                self._advance()
                chars = []
                while self._peek() not in ('"', "\0"):
                    c = self._advance()
                    if c == "\n":
                        raise RancageSyntaxError("String tidak boleh melewati baris", line, col)
                    if c == "\\":
                        esc = self._advance()
                        mapping = {"n": "\n", "r": "\r", "t": "\t", '"': '"', "\\": "\\"}
                        if esc not in mapping:
                            raise RancageSyntaxError(f"Escape sequence tidak dikenal: \\{esc}", self.line, self.column)
                        chars.append(mapping[esc])
                    else:
                        chars.append(c)
                if self._peek() != '"':
                    raise RancageSyntaxError("String tidak ditutup", line, col)
                self._advance()
                self._add("STRING", "".join(chars), line, col)
                continue
            two = ch + self._peek(1)
            if two in DOUBLE:
                self._advance(); self._advance()
                self._add("SYMBOL", two, line, col)
                continue
            if ch in SINGLE:
                self._advance()
                self._add("SYMBOL", ch, line, col)
                continue
            raise RancageSyntaxError(f"Karakter tidak dikenal: {ch!r}", line, col)
        self._add("EOF", "", self.line, self.column)
        return self.tokens
