# RANCAGE Performance Roadmap (RPR)

**Dokumen:** Rancangan strategi performa dan benchmark  
**Versi:** 0.2 — Revised Proposal  
**Status:** DRAFT — Menunggu owner review; belum disetujui untuk implementasi  
**Baseline:** RANCAGE 0.2.0a1  
**Baseline commit:** `03c6ec15b31eeddf8210223c32ca98793abe4222`  
**Tag:** `v0.2.0a1`

---

## 0. Ringkasan perubahan v0.1 → v0.2

Revisi ini memasukkan hasil audit RANCAGE Architect serta klarifikasi dari sumber benchmark publik.

1. Angka historis Zig 510,5 ms, Rust 515,1 ms, dan C 518,8 ms **terverifikasi tercantum** pada halaman `benjdd.com/languages2/`. Namun, hasil tersebut **belum direproduksi secara independen** dari source revision, command line, build flags, dan source hash yang dipatok.
2. Benchmark historis satu miliar iterasi dan benchmark upstream yang lebih baru dengan 100 juta pembaruan array dipisahkan menjadi profil berbeda. Hasil keduanya tidak boleh dicampur.
3. Ditambahkan milestone desain **Typed IR** sebelum feasibility study backend native.
4. Bounds-check elimination (BCE) menjadi optimisasi yang diblokir secara default. BCE memerlukan rancangan pembuktian keselamatan dan persetujuan owner terlebih dahulu.
5. Metodologi benchmark diperjelas: timing boundary, warm-up, kondisi mesin, statistik, validasi hasil, dan pemisahan biaya startup dari waktu kernel.
6. Interaksi benchmark dengan batas resource VM harus eksplisit. Tidak ada perubahan pada default `MAX_STEPS`, `MAX_DEPTH`, `MAX_ALLOCATED_UNITS`, atau kuota lainnya.
7. Roadmap diperluas menjadi R0–R7. Semua tahapan tetap proposal, bukan otorisasi Stage 1.

## 1. Visi dan prinsip

RANCAGE diarahkan menjadi bahasa pemrograman dengan tiga karakteristik utama:

- **Lightweight:** runtime dan penggunaan memori efisien, startup cepat, dependensi minimal.
- **Safe:** static typing, null safety, bounds checking, batas capability dan resource, serta perilaku aman sebagai default.
- **Strong:** compiler dan runtime matang, sistem tipe ekspresif, diagnostik kuat, dan kemampuan menghasilkan program berkinerja tinggi.

Performa tinggi merupakan sasaran strategis, tetapi tidak boleh dicapai dengan mengorbankan ketiga prinsip tersebut.

Target jangka panjang adalah performa kompetitif pada beberapa jenis workload yang dapat direproduksi, bukan kemenangan pada satu benchmark yang tidak mewakili penggunaan nyata.

## 2. Fakta benchmark yang sudah diverifikasi

### 2.1 Halaman benchmark historis `/languages/`

Halaman `https://benjdd.com/languages/` menyatakan:

- Benchmark berjudul **1 Billion nested loop iterations** dan **Naïve Fibonacci**.
- Pengujian dilakukan pada MacBook Pro M3 dengan RAM 16 GB.
- Input yang dicantumkan adalah `40`.
- Metodologi halaman tersebut menggunakan `/usr/bin/time`.
- Setiap bahasa dijalankan tiga kali dan waktu terendah yang digunakan.

Halaman tersebut tidak, dengan sendirinya, mematok source commit SHA atau SHA-256 file implementasi.

### 2.2 Halaman `/languages2/` — asal angka yang menjadi motivasi RPR

Halaman `https://benjdd.com/languages2/` mencantumkan:

- Judul **1 Billion nested loop iterations**.
- MacBook Pro M3 dengan RAM 16 GB.
- Input `40`.
- Pengukuran menggunakan Hyperfine.
- Tiga run dan statistik mean ± standard deviation serta range min–max.
- Versi toolchain, termasuk Zig 0.13.0, Rust/Cargo 1.82.0, dan Apple Clang 16.0.0.

Hasil yang tercantum:

| Bahasa | Mean | Standard deviation | Range |
|---|---:|---:|---:|
| Zig | 510,5 ms | 1,6 ms | 508,7–511,5 ms |
| Rust | 515,1 ms | 1,5 ms | 514,1–516,8 ms |
| C | 518,8 ms | 3,0 ms | 516,0–521,9 ms |

Halaman juga menampilkan peringatan Hyperfine terkait run pertama yang lebih lambat pada beberapa bahasa dan menyebut opsi `--warmup` telah digunakan. Durasi/jumlah warm-up yang persis tidak dapat dipastikan hanya dari output halaman.

**Status klaim:** angka tersebut *published and source-observed*. Angka belum *independently reproduced*. RPR tidak boleh menyebutnya sebagai hasil pengukuran RANCAGE atau sebagai ranking universal.

### 2.3 Upstream repository `bddicken/languages`

Repository `https://github.com/bddicken/languages` menjelaskan transisi dari runner lama ke runner in-process. Pada runner baru:

- program yang diuji mengukur fungsi target dari dalam proses;
- masing-masing bahasa diberi budget waktu pengujian yang sama dan menjalankan fungsi sebanyak mungkin;
- pengukuran menggunakan monotonic clock;
- hasil komputasi dan statistik seperti mean, standard deviation, minimum, maksimum, serta jumlah run dilaporkan;
- tersedia warm-up time dan run time.

README direktori `loops` pada upstream yang diperiksa menjelaskan workload **100 juta pembaruan array** dan menyatakan bahwa hasil penjumlahan pada iterasi terdalam harus langsung ditugaskan ke indeks array. README repository juga menyebut perubahan benchmark loops dibanding runner lama, termasuk inner loop menjadi 10 ribu agar bahasa yang lebih lambat dapat menyelesaikan lebih banyak run.

Karena itu, benchmark upstream baru bukan workload historis satu miliar iterasi. Keduanya wajib memiliki ID dan laporan terpisah.

### 2.4 Hal yang masih belum dipatok

Audit web mengonfirmasi isi halaman dan dokumentasi publik, tetapi belum menetapkan seluruh artefak untuk reproduksi historis. Sebelum RPB-001-L dinyatakan dapat direproduksi, R0 masih harus menemukan dan menyimpan:

- commit SHA repository yang benar-benar digunakan untuk implementasi legacy pada `/languages2/`;
- path setiap source file untuk C, Rust, dan Zig;
- SHA-256 dari setiap source file dan script compile/run yang relevan;
- compiler command dan seluruh build flags;
- command Hyperfine lengkap, termasuk konfigurasi warm-up;
- isi tepat program yang dipanggil dengan argumen `40`;
- definisi tipe integer, ukuran array, jumlah iterasi, dan operasi pada setiap iterasi;
- output/checksum yang membuktikan seluruh pekerjaan benar-benar dilakukan.

Jika source revision persis tidak dapat ditemukan, profil tersebut harus diberi label **historical-page reference, not exact source reproduction**. Jangan menebak atau merekonstruksi source hanya dari judul dan angka.

## 3. Tujuan benchmark RANCAGE

RANCAGE menggunakan dua profil benchmark utama dan beberapa mode pengukuran. Profil benchmark tidak boleh dicampur.

### 3.1 RPB-001-L — Legacy Historical Compatibility

Tujuan: menyelidiki dan, bila source yang tepat tersedia, mereproduksi workload historis yang ditampilkan di `benjdd.com/languages2/`.

Aturan:

- Menggunakan source dan konfigurasi yang dipatok pada R0.
- Mempertahankan semantik, operasi, input, jumlah iterasi, dan metode timing dari fixture yang dipilih.
- Menghasilkan checksum/result yang divalidasi.
- Mencatat seluruh compiler flags dan versi toolchain.
- Menyertakan SHA-256 file sumber dan skrip runner.

Jika source historis tidak dapat dipatok, RPB-001-L tidak boleh diklaim sebagai reproduksi persis angka Zig/Rust/C di halaman tersebut. Dalam keadaan itu, hanya boleh dilaporkan sebagai rekonstruksi eksperimental baru dengan nama dan hash fixture sendiri.

### 3.2 RPB-001-N — Current Upstream Compatibility

Tujuan: mengikuti workload dan runner upstream yang lebih baru.

Aturan:

- Mematok commit SHA upstream, bukan hanya branch `main`.
- Menggunakan source, input, warm-up, run duration, dan protokol output dari revisi yang dipatok.
- Untuk loops, mengikuti spesifikasi upstream yang saat itu dipatok; dokumentasi yang diperiksa menyebut 100 juta pembaruan array.
- Menyimpan source hash, compiler/toolchain, dan runner revision.
- Memvalidasi hasil sesuai mekanisme upstream.

Setiap perubahan upstream yang material menghasilkan fixture/revision benchmark baru. Hasil antar-revisi tidak boleh digabung tanpa label.

### 3.3 Benchmark tambahan

Naïve Fibonacci dapat dipertimbangkan sebagai benchmark terpisah di masa mendatang. Ia tidak boleh digabung dengan nested-loop benchmark menjadi satu skor kecuali ada aturan agregasi eksplisit dan disetujui sebelumnya.

## 4. Mode pengukuran yang wajib dipisahkan

Pengukuran end-to-end dan pengukuran kernel menjawab pertanyaan berbeda. RPR menggunakan empat mode berikut.

### A. Source-to-run end-to-end

Mulai: saat proses `cage run <source>` diluncurkan oleh harness.  
Selesai: saat proses keluar dan status exit tersedia.

Mencakup startup proses, frontend, kompilasi, inisialisasi VM, eksekusi, dan teardown yang terjadi sebelum proses keluar.

### B. Precompiled-bytecode end-to-end

Mulai: saat proses menjalankan artefak bytecode yang telah dibuat sebelumnya diluncurkan.  
Selesai: saat proses keluar dan status exit tersedia.

Mencakup startup CLI/runtime, loading dan validasi bytecode, inisialisasi VM, eksekusi, serta teardown. Tidak mencakup waktu kompilasi source.

### C. VM kernel/in-process

Timer monotonic diletakkan di sekitar fungsi/workload yang diukur setelah input dan state benchmark disiapkan. Startup proses, lexing, parsing, kompilasi, dan validasi awal tidak termasuk jika runner memisahkannya.

Hasil wajib menyebut bahwa eksekusi masih menggunakan VM dan semua batas runtime yang aktif.

### D. Native kernel/in-process dan native end-to-end

Untuk native backend kelak, laporkan dua hal secara terpisah:

- **Native kernel:** timer mengukur fungsi/workload target, mengikuti aturan fixture.
- **Native end-to-end:** timer eksternal mengukur peluncuran executable hingga proses selesai.

Jangan membandingkan hasil kernel dengan hasil end-to-end seolah-olah keduanya setara.

## 5. Standar protokol benchmark

### 5.1 Identitas dan provenance

Setiap hasil minimal mencatat:

| Field | Isi wajib |
|---|---|
| Benchmark ID | Profil dan revisi, misalnya RPB-001-L-r1 |
| Repository | URL repository benchmark |
| Commit SHA | Commit penuh yang diuji |
| Source paths | File yang membentuk workload dan runner |
| Source hashes | SHA-256 setiap file relevan |
| Language version | Versi RANCAGE atau bahasa pembanding |
| Compiler/toolchain | Nama dan versi lengkap |
| Build flags | Seluruh flag optimisasi dan konfigurasi |
| Hardware | Model CPU, core/thread jika tersedia, RAM |
| OS | Nama, versi, dan arsitektur |
| Runtime mode | VM, precompiled VM, native, JIT, dan sebagainya |
| Input/config | Argumen, ukuran data, jumlah iterasi, warm-up dan run duration |
| Result | Checksum atau hasil komputasi yang divalidasi |
| Timing | Mean, median, standard deviation, min, max, confidence interval |
| Samples | Seluruh sampel mentah dan jumlah pengulangan |
| Environment | Power mode/governor jika tersedia, kondisi thermal, background load |

### 5.2 Warm-up

- Untuk RPB-001-N, ikuti warm-up protocol yang ditetapkan oleh revisi upstream yang dipatok.
- Catat warm-up duration dan cara warm-up dijalankan.
- Untuk VM RANCAGE tanpa JIT, jangan mengklaim warm-up sebagai JIT compilation. Warm-up tetap dapat memengaruhi cache dan keadaan proses; perlakuannya harus konsisten dan dicatat.
- Untuk eksperimen lokal yang tidak memiliki ketentuan upstream, lakukan pilot stabilitas terlebih dahulu, pilih warm-up policy sebelum pengukuran final, lalu bekukan kebijakan itu dalam fixture.
- Dilarang mengubah warm-up hanya untuk memperbaiki hasil bahasa tertentu.

### 5.3 Kondisi perangkat

- Jalankan seluruh kandidat pembanding pada mesin yang sama untuk satu tabel perbandingan.
- Gunakan kondisi daya yang konsisten dan catat power mode.
- Tutup workload lain yang tidak diperlukan.
- Catat CPU frequency/governor dan kondisi thermal jika sistem menyediakannya. Jangan mengklaim dapat mengunci frekuensi pada platform yang tidak menyediakan kontrol tersebut.
- Jalankan beberapa batch independen; urutan bahasa dapat dirotasi agar satu bahasa tidak selalu diuji pada kondisi termal pertama atau terakhir.
- Jangan menggabungkan hasil lintas CPU/OS sebagai satu ranking langsung.

### 5.4 Statistik dan keputusan

Laporan wajib menyimpan semua sampel mentah serta menampilkan mean, median, standard deviation, minimum, maksimum, dan confidence interval 95%.

Untuk menyatakan satu implementasi lebih cepat daripada yang lain:

- tentukan metrik utama terlebih dahulu;
- bandingkan rasio waktu dari batch/sampel independen;
- gunakan metode confidence interval yang ditetapkan sebelum pengujian (misalnya bootstrap CI untuk rasio median atau mean yang dipilih);
- jangan memakai aturan sederhana “CI tidak tumpang tindih” sebagai satu-satunya dasar keputusan;
- jika hasil tidak cukup membedakan kandidat, laporkan **inconclusive**.

Tidak boleh memilih hanya sampel tercepat untuk menyatakan pemenang. Minimum boleh dicantumkan sebagai statistik deskriptif, bukan satu-satunya dasar ranking.

### 5.5 Correctness dan optimisasi compiler

- Hasil integer harus cocok persis dengan reference result.
- Untuk hasil floating-point, tetapkan toleransi absolut/relatif sebelum menjalankan benchmark dan dokumentasikan alasan toleransi.
- Output/checksum harus memastikan hasil workload digunakan dan pekerjaan tidak hilang karena dead-code elimination.
- Optimisasi compiler yang menghilangkan loop atau menghitung hasil secara compile-time tetap merupakan perilaku yang boleh dilaporkan hanya jika aturan fixture mengizinkannya dan hasilnya benar. Jelaskan bila compiler melakukan constant folding atau loop elimination.
- Bandingkan implementasi yang memiliki semantik setara. Jika representasi data atau tipe berbeda, dokumentasikan perbedaannya.

## 6. Semantik bahasa dan representasi data

### 6.1 Integer semantics

RANCAGE saat ini menggunakan integer bertanda 64-bit dengan overflow checks pada operasi yang didukung VM.

Perbedaan dengan C, Rust, Zig, atau bahasa lain tidak boleh diasumsikan tanpa memeriksa source dan compiler mode yang benar-benar digunakan.

Sebelum membandingkan:

1. identifikasi tipe integer dan lebar bit pada setiap implementasi;
2. verifikasi seluruh nilai intermediate pada workload;
3. pastikan tidak ada signed overflow pada workload yang diklaim setara, atau definisikan perilaku wrapping/checked yang sesuai;
4. catat compiler flags yang memengaruhi overflow semantics.

Jika seluruh operasi terbukti berada dalam rentang aman, perbedaan kebijakan overflow tidak otomatis membatalkan perbandingan workload tersebut. Jika tidak, perbandingan harus ditandai tidak setara atau workload disesuaikan dan diberi ID baru.

### 6.2 List dan array layout

RANCAGE 0.2 saat ini merepresentasikan list melalui Python `list` dan map melalui Python `dict`; list generik bukan typed contiguous array.

Hal ini penting karena array bertipe kontigu pada backend native akan memiliki layout dan biaya akses yang berbeda dari list objek Python.

Karena itu, laporan harus membedakan:

- **Current VM semantics:** struktur data sebagaimana diimplementasikan RANCAGE 0.2.
- **Typed/contiguous array proposal:** fitur atau representasi baru yang memerlukan desain bahasa dan persetujuan tersendiri.
- **Native optimized implementation:** representasi hasil lowering backend yang harus tetap mematuhi semantik bahasa.

Tidak boleh mengubah layout secara diam-diam lalu mengklaim bahwa implementasi tersebut reproduksi identik dari program VM lama.

## 7. Kondisi aktual dan batas resource RANCAGE

Fakta repository yang dilaporkan Architect:

- RANCAGE 0.2 adalah compiler dan VM berbasis Python.
- Bahasa saat ini mendukung `while`; belum ada `for`.
- Collection list memakai Python `list`; map memakai Python `dict`.
- IR saat ini stack-based JSON bytecode, bukan typed SSA IR.
- VM menghitung langkah instruksi dan memiliki default `MAX_STEPS = 1_000_000`.
- `max_steps` dapat dikonfigurasi pada instance VM dan tersedia opsi CLI.
- Operasi arithmetic dan collection memiliki pemeriksaan batas/overflow sesuai implementasi saat ini.
- Belum ada native backend maupun benchmark harness di repository.

Fakta ini adalah baseline desain, bukan hasil pengukuran performa. Bottleneck aktual hanya boleh dinyatakan setelah profiling.

### 7.1 Benchmark mode dan resource limits

- Default `MAX_STEPS`, `MAX_DEPTH`, `MAX_COLLECTION_SIZE`, `MAX_STRING_LENGTH`, dan `MAX_ALLOCATED_UNITS` tidak boleh dinaikkan secara global.
- Jika workload memerlukan limit lebih besar, perubahan hanya boleh melalui konfigurasi instance/per-run yang eksplisit dan tercatat.
- Setiap hasil yang memakai quota berbeda dari default harus diberi label **benchmark configuration — non-default resource budget**.
- Gunakan subprocess dan timeout untuk benchmark opt-in berskala besar.
- Laporkan konfigurasi resource dan konsekuensinya. Jangan menyebut hasil tersebut sebagai representasi default safety profile.
- Native code yang belum memiliki enforcement resource setara tidak boleh diklaim mempertahankan jaminan resource isolation VM.

### 7.2 Hubungan OATS-016 dengan RPB-001

**OATS-016** adalah stress/resource-control test: menguji apakah VM berhenti secara benar ketika mencapai batas instruksi dan apakah benchmark stress berskala besar berjalan hanya dengan konfigurasi opt-in yang terkontrol.

**RPB-001** adalah performance benchmark: mengukur throughput/waktu pada workload yang didefinisikan dan divalidasi.

Keduanya mempunyai tujuan, harness, dan acceptance criteria berbeda. Benchmark satu miliar iterasi bukan bagian dari test suite reguler.

## 8. Strategi arsitektur performa

### 8.1 Frontend

Lexer, parser, AST, dan type checker yang sudah ada tetap menjadi fondasi. Optimisasi backend tidak boleh diam-diam mengubah semantik source program.

### 8.2 Typed IR — rancangan wajib sebelum native backend

Sebelum pemilihan dan implementasi backend native, RANCAGE memerlukan proposal arsitektur Typed IR.

Proposal Typed IR minimal harus menjelaskan:

- hubungan dengan AST dan RANCAGE-IR 0.2;
- apakah IR baru berbentuk SSA atau representasi typed lainnya;
- tipe nilai, operasi, control-flow, basic block, dan terminator;
- representasi list/map/record/string serta operasi mutasinya;
- nullability dan integer overflow semantics;
- efek samping, error, dan operasi yang dapat gagal;
- verifikasi well-formedness IR;
- aturan lowering ke bytecode VM dan/atau native backend;
- kompatibilitas dengan IR 0.1/0.2;
- strategi pengujian kesetaraan hasil antara VM dan backend lain.

Typed IR design adalah milestone desain. Ia tidak otomatis mengizinkan perubahan kode, format IR publik, atau penghapusan kompatibilitas.

### 8.3 Native backend feasibility

Pilihan yang dapat diteliti setelah Typed IR design:

| Alternatif | Potensi | Risiko/kendala | Status |
|---|---|---|---|
| LLVM | Optimizer matang dan target platform luas | Integrasi, ukuran dependensi, versi LLVM, linking dan runtime | Feasibility study only |
| Cranelift | Backend code generation dan IR yang mendukung compiler JIT/AOT tertentu | Ecosystem/toolchain Rust dan konflik dengan keputusan implementasi RANCAGE yang berlaku | Blocked for implementation pending explicit owner approval |
| Backend mandiri | Kontrol penuh atas format dan kebutuhan RANCAGE | Instruction selection, register allocation, ABI, object file, debug info, portabilitas, maintenance | Research only; not recommended as initial path |

Tidak ada backend yang dipilih dalam RPR v0.2.

**Governance note:** keputusan repository saat ini melarang penambahan implementasi compiler dalam Rust/C/C++/Zig atau file Cargo tanpa persetujuan owner. Karena Cranelift memerlukan ekosistem Rust, prototype atau penambahan toolchain Rust memerlukan persetujuan eksplisit lebih dahulu. Pembahasan konseptual tidak sama dengan persetujuan implementasi.

## 9. Audit dan prioritas optimisasi

Tidak ada optimisasi yang boleh diimplementasikan sebelum correctness baseline dan profiling mendukungnya.

| Optimisasi | Kelayakan saat ini | Ketergantungan | Risiko/gerbang |
|---|---|---|---|
| Constant folding | Layak diteliti setelah aturan semantik/overflow dipastikan | Typed IR sangat membantu, tetapi tidak harus native | Hasil harus identik termasuk overflow/error |
| Dead code elimination | Layak setelah efek samping dan error dimodelkan | Typed IR/effect model | Tidak boleh menghapus operasi yang observable atau gagal menurut semantik |
| Common subexpression elimination | Belum prioritas sebelum IR dan efek samping jelas | Typed IR | Hanya ekspresi pure dengan aturan aliasing yang jelas |
| Loop-invariant code motion | Riset lanjutan | CFG, typed IR, effect/alias analysis | Tidak boleh memindah operasi melewati side effect atau error |
| Induction variable optimization | Riset lanjutan | CFG dan typed IR | Harus mempertahankan overflow dan batas integer |
| Function inlining | Riset setelah profiling | Call graph/typed IR atau backend | Dampak code size dan call-depth/resource limits |
| Register allocation | Hanya relevan pada native backend | Native backend | Belum relevan bagi stack VM saat ini |
| Bounds-check elimination | **Blocked by default** | Analisis/proof keselamatan yang memadai | Wajib proposal bukti formal/teknis dan persetujuan owner; jika tidak terbukti, checks tetap ada |
| SIMD/vectorization | Riset lanjutan | Typed IR, native backend, alignment/data layout | Semantik integer/floating-point dan portability harus dipertahankan |

Prioritas final ditentukan dari hasil R2. Daftar ini bukan instruksi untuk mengimplementasikan seluruh optimisasi.

## 10. Roadmap R0–R7

Seluruh roadmap bersifat proposal. Setiap tahap memerlukan scope, acceptance criteria, dan owner approval sebelum implementasi.

### R0 — Benchmark Specification and Source Pinning

Tujuan: mengubah referensi benchmark menjadi fixture yang dapat diaudit.

Deliverables:
- RPB-001-L dan RPB-001-N specification;
- upstream repository commit SHA yang dipatok untuk setiap profil;
- file paths dan SHA-256 source/runner;
- implementasi C/Rust/Zig dan compiler flags yang sesuai;
- workload, input, iterasi, data type, operasi, dan result validation;
- command line dan metode timing yang tepat;
- penjelasan eksplisit atas bagian yang tidak dapat direproduksi.

Exit criteria:
- profil mempunyai identitas revision/hash;
- workload dan result dapat diverifikasi dari source;
- metode pengukuran tidak ambigu;
- legacy/current tidak tercampur.

Jika source historis tidak dapat diidentifikasi, R0 harus menyatakan keterbatasan itu dan tidak boleh mengklaim reproduksi persis angka historis.

### R1 — Local Reference Baseline

Tujuan: memperoleh baseline pembanding pada satu perangkat lokal.

Kandidat minimal: C, Rust, Zig, dan RANCAGE dalam mode yang dapat dijalankan saat itu.

Deliverables:
- hardware/software inventory;
- command dan build flags;
- raw timing samples;
- correctness result;
- startup/kernel mode yang diuji;
- limitations report.

Exit criteria: laporan dapat direproduksi pada mesin dan konfigurasi yang sama. Hasil R1 tidak dibandingkan langsung dengan angka M3 jika perangkatnya berbeda.

### R2 — RANCAGE VM Profiling

Tujuan: menemukan bottleneck aktual, bukan menebak dari pembacaan source.

Area:
- opcode dispatch;
- stack operations;
- loop/control-flow;
- arithmetic;
- list access/mutation;
- function calls;
- allocation dan formatting jika relevan.

Deliverables:
- profiling data;
- biaya per kategori;
- workload scaling report;
- bottleneck ranking beserta bukti.

Tidak ada perubahan VM yang otomatis diotorisasi oleh tahap profiling.

### R3 — Typed IR Architecture Design

Tujuan: menetapkan desain IR yang cukup kuat untuk optimisasi dan calon backend.

Deliverables:
- Typed IR architecture proposal;
- type/effect/control-flow model;
- integer/null/collection semantics;
- verifier design;
- compatibility and lowering plan;
- risk and test strategy.

Exit criteria: Architect menyatakan desain lengkap, Auditor mengaudit, QA menilai testability, dan owner menyetujui sebelum implementasi apa pun.

### R4 — Native Backend Feasibility Study

Tujuan: mengevaluasi LLVM, Cranelift, dan backend mandiri berdasarkan Typed IR design serta prinsip RANCAGE.

Deliverables:
- dependency and maintenance comparison;
- target platform analysis;
- compile-time, binary-size, memory, startup, and runtime considerations;
- safety and debugging analysis;
- recommendation with explicit trade-offs.

Exit criteria: keputusan owner diperlukan. Tidak ada backend yang dipilih otomatis oleh hasil studi.

### R5 — Native Backend Prototype

Tujuan: prototype terbatas setelah backend dipilih dan owner menyetujui implementasinya.

Acceptance criteria:
- subset bahasa yang dinyatakan jelas;
- executable native dapat dihasilkan;
- hasil sesuai reference VM;
- error/integer/null semantics diuji;
- batasan resource dan platform didokumentasikan;
- reproducible build instructions tersedia.

R5 tidak boleh dimulai hanya karena R4 selesai; diperlukan otorisasi implementasi tersendiri.

### R6 — Measured Optimization

Tujuan: mengoptimalkan bagian yang terbukti menjadi bottleneck.

Setiap optimisasi harus memiliki:
- hipotesis yang diuji;
- baseline dan hasil setelah perubahan;
- correctness tests;
- security audit;
- memory/code-size impact;
- dokumentasi trade-off.

BCE tetap blocked tanpa proposal pembuktian dan owner approval.

### R7 — Competitive Benchmarking

Tujuan: mengukur posisi RANCAGE terhadap C, Rust, Zig, dan bahasa lain pada workload yang sama.

Laporan harus memisahkan:
- kernel vs end-to-end;
- VM vs native;
- compile time vs execution time;
- memory use dan binary size;
- benchmark legacy vs current upstream;
- correctness dan statistik.

Klaim ranking hanya boleh dibuat berdasarkan profil, source revision, perangkat, dan metodologi yang sama. Jika hasil tidak konklusif, laporkan demikian.

## 11. Temuan audit dan disposisi dalam revisi

| Finding | Level Architect | Disposisi RPR v0.2 |
|---|---|---|
| F-01 — historical benchmark source not pinned | CRITICAL | **Partially resolved / HIGH blocker for comparison.** Angka terbukti tercantum pada halaman publik; source revision dan hashes persis masih harus dipatok pada R0. |
| F-02 — no Typed IR milestone | HIGH | **Accepted.** Added R3 before backend feasibility. |
| F-03 — BCE lacks proof mechanism | HIGH | **Accepted.** BCE blocked by default pending proof proposal and owner approval. |
| F-04 — integer overflow semantics | HIGH | **Refined.** Inspect exact source/compiler mode and prove workload does not overflow. A semantic difference matters only if it affects this workload. |
| F-05 — benchmark environment/statistics incomplete | MEDIUM | **Accepted.** Added warm-up, machine state, sample, and confidence interval protocol. |
| F-06 — timing boundaries ambiguous | MEDIUM | **Accepted.** Added four explicit measurement modes. |
| F-07 — optimization dependency order unclear | MEDIUM | **Accepted.** Optimizations now gated by typed IR, profiling, and semantic proof. |
| F-08 — Cranelift conflicts with language/toolchain policy | MEDIUM | **Accepted.** Cranelift prototype/toolchain is blocked pending explicit owner approval. |
| F-09 — typed contiguous array differs from current list layout | LOW | **Accepted.** Current VM, typed-array proposal, and native layout are reported separately. |
| F-10 — ranking before baseline | LOW | **Accepted.** Ranking deferred to R7 and requires same profile/platform. |
| F-11 — OATS-016 separate from RPB-001 | INFORMATIONAL | **Retained.** |
| F-12 — governance and frozen baseline | INFORMATIONAL | **Retained.** |

Catatan: disposisi ini adalah revisi proposal oleh penulis, bukan hasil audit independen kedua.

## 12. Governance dan batas perubahan

- RANCAGE 0.2.0a1 tetap menjadi baseline Stage 0.
- Commit `03c6ec15b31eeddf8210223c32ca98793abe4222` tidak boleh diubah atau di-rewrite.
- Tag `v0.2.0a1` tidak boleh dipindahkan.
- Stage 0 tetap CLOSED dan FROZEN.
- Stage 1 tetap NOT STARTED dan NOT AUTHORIZED sampai owner menyetujuinya.
- RPR v0.2 tidak mengotorisasi perubahan source code, IR format, compiler, VM, runtime quota, atau toolchain.
- Tidak ada native backend, optimizer, benchmark harness, atau benchmark run yang otomatis disetujui oleh dokumen ini.
- File Roo Code seperti `.roo/` dan `.roomodes` tetap merupakan artefak lokal tooling dan tidak boleh dimasukkan ke Git.
- Urutan governance untuk milestone penting: Architect → Developer → Auditor → QA Engineer → Owner Approval.

## 13. Keputusan owner yang masih diperlukan

Sebelum proposal ini dapat menjadi roadmap kerja, owner perlu memutuskan:

1. Apakah RPR v0.2 diterima sebagai proposal riset performa, tanpa otorisasi implementasi langsung?
2. Apakah R0 diizinkan untuk mematok source benchmark publik dan menghasilkan fixture dokumentasi saja?
3. Jika commit historis tidak dapat ditemukan, apakah RPB-001-L boleh diganti dengan rekonstruksi baru yang diberi identitas terpisah?
4. Apakah Typed IR design (R3) boleh dibuat sebagai proposal arsitektur tersendiri?
5. Apakah riset Cranelift yang memerlukan toolchain Rust boleh dilakukan, mengingat batasan implementasi compiler yang berlaku?
6. Apakah empat mode pengukuran pada §4 diterima sebagai format laporan resmi?

## 14. Kesimpulan

RANCAGE tidak akan mengejar posisi pertama hanya dengan mempercepat Python VM. Strategi jangka panjang adalah membangun representasi intermediate yang kuat, mengevaluasi backend native berdasarkan bukti, mengoptimalkan bottleneck yang terukur, serta mempertahankan semantik dan prinsip keselamatan.

Angka historis pada `benjdd.com/languages2/` menjadi motivasi dan referensi publik, bukan janji target waktu. Sasaran kompetitif hanya dapat dinilai setelah benchmark source, toolchain, hardware, dan metode pengukuran dipatok secara dapat direproduksi.

**Status akhir dokumen:** DRAFT — REVISED AFTER ARCHITECT REVIEW. Menunggu pemeriksaan Auditor dan persetujuan owner. Tidak ada implementasi yang disetujui.

---

## Referensi eksternal

1. Historical benchmark page: https://benjdd.com/languages/  
   Metode yang ditampilkan: `/usr/bin/time`, tiga run dengan hasil terendah, M3 MacBook Pro, RAM 16 GB, input `40`.
2. Hyperfine benchmark page: https://benjdd.com/languages2/
   Sumber angka historis Zig/Rust/C; menampilkan mean, standard deviation, range, tiga run, hardware dan versi toolchain.
3. Upstream repository: https://github.com/bddicken/languages
   Dokumentasi runner in-process, monotonic timing, hasil dan statistik.
4. Upstream loops README: https://github.com/bddicken/languages/tree/main/loops
   Dokumentasi workload loop versi baru yang menyebut 100 juta pembaruan array. Branch `main` harus diganti dengan commit SHA pada fixture RPB-001-N sebelum pengujian formal.

**External-source audit note:** halaman web telah diperiksa, tetapi SHA commit historis yang tepat dan SHA-256 file benchmark belum dipatok dalam dokumen ini. Itu tetap menjadi deliverable R0.
