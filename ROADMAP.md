# RANCAGE Roadmap

## Visi Proyek

- **Bahasa:** RANCAGE (`.cage` source, `.rcb` bytecode, CLI `cage`)
- **Prinsip:** Lightweight, Safety, Strong
- **Bahasa Implementasi:** Python 3.10+ (bukan migrasi ke Rust)
- **Target Utama:** CLI, utilitas, pengolah data, game teks deterministik, dengan backend VM, WebAssembly (`.wasm`), dan native x86-64 (`.exe` kecil) secara bertahap.

## Roadmap 7 Tahap (Solo + AI)

| Tahap | Target | Output | Prinsip | Status |
|---|---|---|---|---|
| 0 | Python compiler + bounded VM, 134 tests, Windows PyInstaller package | `.rcb` bytecode, `cage check/run` | Safety, Strong | Selesai (Frozen `v0.2.0a1`) |
| 1 | Stage 1: `for` loop, `break`/`continue`, modul/import, error handling, stdlib inti | Loop deterministik & kontrol, modular, error handling | Strong | Selesai |
| 1.5 | Preset keyword Sunda (`su`) + flag CLI `--lang=su` | `.cage` bisa ditulis dalam Sunda (`su`), tetap kompatibel `en` | Strong / Identitas | Berjalan |
| 2 | Backend WebAssembly (`.wasm`) | `.wasm` kecil, jalan di browser/Node | Lightweight | Berjalan (subset numerik/bool/control-flow) |
| 3 | Backend native x86-64 (`.exe` kecil) | `.exe` < 5 MB, startup < 100 ms, tanpa runtime eksternal | Lightweight, Strong | Terencana |
| 4 | Build provenance sederhana | Hash + identitas build `.rcb`/`.exe`, verifikasi asal-usul | Safety | Terencana |
| 5 | Contoh nyata: CLI tool, pengolah data kecil, game teks deterministik | Bukti "bisa jalan" untuk target umum | Strong | Terencana |
| 6 | Self-hosting: Compiler RANCAGE dalam RANCAGE | Bootstrap dari Python ke RANCAGE mandiri | Mandiri (long-term) | Visi jangka panjang |

## Tahap 7 (Visi Jangka Panjang)

- Compiler RANCAGE 100% ditulis dalam RANCAGE (self-hosting).
- Standard library stabil: koleksi, map, record, file I/O dasar, string API.
- SDK MIT-licensed: materi ekstensi, converter, tooling dasar.
- Language Server Protocol (LSP) ringan untuk editor (VSCode plugin).
- Backend Android (transpiler `.cage` ke Kotlin/Luau) jika backend inti sudah matang.
- Build provenance lengkap: tanda tangan kriptografis dan verifikasi rantai pasokan.

## Di Luar Cakupan Saat Ini (Ditunda / Disingkirkan)

- Aplikasi remote desktop (seperti RustDesk) dan FPS 3D / grafik multimedia berat ditunda hingga backend native/WASM terbukti.
- Migrasi bahasa compiler ke Rust (Python tetap menjadi bahasa compiler; backend WASM/native hanya untuk codegen output).
- Multi-platform serentak tanpa runner dan smoke test pada OS target.

## Aturan Rilis

Target yang direncanakan bukan target yang sudah didukung. Setiap fitur dan platform wajib lulus test suite dan smoke test pada target terkait sebelum dinyatakan didukung.
