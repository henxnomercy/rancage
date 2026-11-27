# Desain Stage 1 & Multi-Preset Lexer (`en` / `su`)

## 1. Multi-Preset Lexer (`en` dan `su`)

### 1.1 Tujuan
Mendukung penulisan kode `.cage` menggunakan preset bahasa Sunda (`--lang=su`) tanpa mengubah semantik bahasa, AST, type checker, RANCAGE-IR, maupun bounded VM. Preset default tetap `en`.

### 1.2 Tabel Pemetaan Keyword

| Token Kanonik | `en` (Default) | `su` (Sunda) | Catatan |
|---|---|---|---|
| `MODULE` | `module` | `modul` | Deklarasi modul |
| `FN` | `fn` | `pungsi` | Deklarasi fungsi |
| `LET` | `let` | `pasang` | Variabel mutable |
| `CONST` | `const` | `tetep` | Konstanta immutable |
| `RETURN` | `return` | `balik` | Pengembalian fungsi |
| `IF` | `if` | `lamun` | Percabangan |
| `ELSE` | `else` | `lain` | Cabang alternatif |
| `WHILE` | `while` | `salila` | Loop kondisi |
| `FOR` | `for` | `pikeun` | Loop deterministik (Stage 1) |
| `RECORD` | `record` | `wangun` | Deklarasi record |
| `TRUE` | `true` | `bener` | Literal boolean benar |
| `FALSE` | `false` | `salah` | Literal boolean salah |
| `NULL` | `null` | `kosong` | Literal null |

### 1.3 Aturan Teknis
- **Maximal munch**: Lexer membaca seluruh token `[A-Za-z_][A-Za-z0-9_]*` sebelum mencocokkan kamus keyword, sehingga identifier berimbuhan Sunda seperti `lamunan`, `balikkeun`, atau `beneran` tetap aman sebagai `IDENT`.
- **Intrinsic `citak` / `print`**: `citak` tidak dimasukkan ke dalam `KEYWORDS_SU` / `RESERVED`. Pada mode `su`, pemanggilan `citak(...)` dipetakan ke intrinsic `print` pada tahap parser, sehingga `citak` tidak dikunci sebagai reserved keyword.
- **Cadangan masa depan**: `henteu` dicadangkan dalam catatan desain untuk operator `not` di masa depan.
- **Seleksi mode**: Melalui flag CLI `--lang=en|su` (default `en`), diteruskan ke `Lexer(source, lang=...)` dan `Parser(tokens, lang=...)`. Header pragma `// @basa: su` dicatat sebagai rancangan lanjutan.

## 2. Stage 1 — Fitur Pertama: `for` Loop

### 2.1 Sintaks
```cage
for (let i: int = 0; i < 5; i = i + 1) {
    print(i);
}
```
Dalam mode `--lang=su`:
```cage
pikeun (pasang i: int = 0; i < 5; i = i + 1) {
    citak(i);
}
```

### 2.2 Semantik & Type Checking
- `init` bersifat opsional (deklarasi `let`/`const`, assignment, atau expression statement).
- `condition` bersifat opsional; jika ada harus bertipe `bool`.
- `step` bersifat opsional (assignment, field/index assignment, atau expression statement).
- Variabel yang dideklarasikan pada `init` berada dalam lingkup loop (`condition`, `step`, dan `body`), tetap mematuhi aturan Stage 0 bahwa nama lokal tidak boleh membayangi (shadow) variabel yang sudah dideklarasikan di fungsi yang sama.
- Seperti `while`, `for` tidak diasumsikan pasti dieksekusi oleh analisis `_always_returns`.

### 2.3 Kompilasi RANCAGE-IR 0.2
`For` dikompilasi ke instruksi `JUMP_IF_FALSE` dan `JUMP` yang sudah ada di RANCAGE-IR 0.2 tanpa menambah opcode baru di VM, sehingga tetap kompatibel dan dibatasi oleh `MAX_STEPS`.
