# RANCAGE Performance Roadmap (RPR)

**Dokumen:** Rancangan strategi performa dan benchmark  
**Versi:** 0.3 — Revised After Independent Audit  
**Status:** DRAFT — Revisi setelah audit independen; belum disetujui sebagai roadmap kerja atau untuk implementasi  
**Baseline:** RANCAGE 0.2.0a1  
**Baseline commit:** `03c6ec15b31eeddf8210223c32ca98793abe4222`  
**Tag:** `v0.2.0a1`

---

## 0. Ringkasan perubahan v0.1 → v0.2 → v0.3

Revisi ini memasukkan hasil audit RANCAGE Architect serta klarifikasi dari sumber benchmark publik.

1. Angka historis Zig 510,5 ms, Rust 515,1 ms, dan C 518,8 ms **terverifikasi tercantum** pada halaman `benjdd.com/languages2/`. Namun, hasil tersebut **belum direproduksi secara independen** dari source revision, command line, build flags, dan source hash yang dipatok.
2. Benchmark historis satu miliar iterasi dan dokumentasi upstream `main` yang saat diperiksa menyebut 100 juta pembaruan array dipisahkan menjadi profil berbeda. Detail upstream tersebut tetap pending source pinning sampai commit dan hash dikunci. Hasil kedua profil tidak boleh dicampur.
3. Ditambahkan milestone desain **Typed IR** sebelum feasibility study backend native.
4. Bounds-check elimination (BCE) menjadi optimisasi yang diblokir secara default. BCE memerlukan rancangan pembuktian keselamatan dan persetujuan owner terlebih dahulu.
5. Metodologi benchmark diperjelas: timing boundary, warm-up, kondisi mesin, statistik, validasi hasil, dan pemisahan biaya startup dari waktu kernel.
6. Interaksi benchmark dengan batas resource VM harus eksplisit. Tidak ada perubahan pada default `MAX_STEPS`, `MAX_DEPTH`, `MAX_ALLOCATED_UNITS`, atau kuota lainnya.
7. Roadmap diperluas menjadi R0–R7. Semua tahapan tetap proposal, bukan otorisasi Stage 1.

Perubahan tambahan v0.3 setelah audit independen:
8. Finding F-01 dinyatakan **UNRESOLVED / HIGH BLOCKER**. Keberadaan angka pada halaman publik tidak sama dengan reproduksi independen.
9. `/languages2/` ditetapkan sebagai satu-satunya sumber angka historis Zig/Rust/C yang ditampilkan dalam tabel RPR. `/languages/` hanya konteks historis dan memakai metodologi pengukuran berbeda.
10. Pernyataan `Input value of 40 given to each` dipertahankan sebagai kutipan fakta halaman, tetapi makna argumen untuk workload nested-loop belum dipastikan dari source program. R0 wajib memverifikasinya; tidak boleh diasumsikan sebagai input khusus Fibonacci atau loop.
11. Array-update/layout rationale dibatasi pada profil upstream loops (RPB-001-N) sampai source legacy RPB-001-L dipatok.
12. Mode pengukuran C/D tidak mengizinkan pembuatan harness otomatis; runner in-process memerlukan milestone dan persetujuan owner tersendiri.
13. Persyaratan environment diperbaiki menjadi `required-if-collectable`; metode confidence interval, jumlah resampling, seed, dan aturan keputusan dipatok sebelum R1.
14. Ditambahkan ketentuan arsip snapshot halaman, audit integer width/flags/range, serta batas yang membolehkan instalasi toolchain pembanding dan fixture pihak ketiga tanpa mengizinkan implementasi compiler RANCAGE dalam bahasa terlarang.

## 1. Visi dan prinsip

RANCAGE diarahkan menjadi bahasa pemrograman dengan tiga karakteristik utama:

- **Lightweight:** runtime dan penggunaan memori efisien, startup cepat, dependensi minimal.
- **Safe:** static typing, null safety, bounds checking, batas capability dan resource, serta perilaku aman sebagai default.
- **Strong:** compiler dan runtime matang, sistem tipe ekspresif, diagnostik kuat, dan kemampuan menghasilkan program berkinerja tinggi.

Performa tinggi merupakan sasaran strategis, tetapi tidak boleh dicapai dengan mengorbankan ketiga prinsip tersebut.

Target jangka panjang adalah performa kompetitif pada beberapa jenis workload yang dapat direproduksi, bukan kemenangan pada satu benchmark yang tidak mewakili penggunaan nyata.

## 2. Fakta benchmark yang sudah diverifikasi

### 2.1 Halaman `/languages/` — konteks historis, bukan sumber angka tabel

Halaman `https://benjdd.com/languages/` menampilkan dua judul benchmark, **1 Billion nested loop iterations** dan **Naïve Fibonacci**. Metodologi halaman menyebut M3 MacBook Pro dengan RAM 16 GB, `/usr/bin/time`, tiga pengujian dengan waktu terendah yang dipakai, serta pernyataan `Input value of 40 given to each`.

Halaman ini menggunakan metodologi yang berbeda dari `/languages2/`. Karena itu:

- halaman ini hanya menjadi konteks historis;
- angka atau statistik dari halaman ini tidak boleh dicampur dengan angka `/languages2/`;
- kalimat `Input value of 40 given to each` adalah pernyataan halaman, tetapi referen kata `each` dan peran argumen `40` untuk masing-masing program harus diverifikasi dari source program pada R0;
- jangan menyimpulkan bahwa `40` hanya milik Fibonacci, dan jangan pula menyimpulkan bahwa `40` pasti parameter ukuran/iterasi nested-loop tanpa memeriksa source.

### 2.2 Halaman `/languages2/` — satu-satunya asal angka historis dalam tabel RPR

Halaman `https://benjdd.com/languages2/` adalah sumber angka Zig/Rust/C yang dikutip dalam proposal ini. Halaman menyatakan **1 Billion nested loop iterations**, M3 MacBook Pro dengan RAM 16 GB, Hyperfine, tiga run, serta mean ± standard deviation dan range min–max. Halaman juga menyebut `Input value of 40 given to each`; makna argumen tersebut untuk program nested-loop tetap harus diverifikasi dari source, bukan ditebak dari halaman.

Toolchain yang ditampilkan mencakup Zig 0.13.0, Rust/Cargo 1.82.0, dan Apple Clang 16.0.0. Angka yang tercantum:

**Label wajib untuk seluruh angka berikut: DIPUBLIKASIKAN DI `/languages2/`; BELUM DIREPRODUKSI SECARA INDEPENDEN.**

| Bahasa | Mean yang dipublikasikan | Standard deviation yang dipublikasikan | Range yang dipublikasikan |
|---|---:|---:|---:|
| Zig | 510,5 ms | 1,6 ms | 508,7–511,5 ms |
| Rust | 515,1 ms | 1,5 ms | 514,1–516,8 ms |
| C | 518,8 ms | 3,0 ms | 516,0–521,9 ms |

Halaman memperlihatkan peringatan Hyperfine terkait run pertama yang lebih lambat dan menyebut opsi `--warmup` telah digunakan. Jumlah/durasi warm-up dan command Hyperfine lengkap belum dipatok dari halaman yang tersedia.

**Status klaim:** angka tersebut *published and source-observed, not independently reproduced*. Angka bukan hasil pengukuran RANCAGE, bukan ranking universal, dan bukan target waktu yang dijamin.

### 2.3 Upstream repository `bddicken/languages`

Repository `https://github.com/bddicken/languages` menjelaskan transisi dari runner lama ke runner in-process. Pada runner baru:

- program yang diuji mengukur fungsi target dari dalam proses;
- masing-masing bahasa diberi budget waktu pengujian yang sama dan menjalankan fungsi sebanyak mungkin;
- pengukuran menggunakan monotonic clock;
- hasil komputasi dan statistik seperti mean, standard deviation, minimum, maksimum, serta jumlah run dilaporkan;
- tersedia warm-up time dan run time.

README direktori `loops` pada branch `main` yang diperiksa menjelaskan workload **100 juta pembaruan array** dan menyatakan bahwa hasil penjumlahan pada iterasi terdalam harus langsung ditugaskan ke indeks array. README repository menjelaskan runner in-process yang mengukur fungsi target menggunakan monotonic clock, memberi tiap bahasa budget waktu yang sama, dan melaporkan hasil serta statistik.

**Peringatan provenance:** uraian 100 juta pembaruan array dan detail runner di atas adalah observasi dokumentasi branch `main` pada saat pemeriksaan, bukan fakta fixture RPB-001-N yang sudah dipatok. Sampai commit SHA dan source hash disimpan di R0, seluruh angka/detail workload tersebut berstatus **PENDING SOURCE PINNING** dan tidak boleh menjadi spesifikasi normatif.

Benchmark upstream baru tidak boleh diasumsikan identik dengan benchmark historis satu miliar iterasi. Keduanya wajib memiliki ID dan laporan terpisah.

### 2.4 Hal yang masih belum dipatok

Audit web mengonfirmasi isi halaman dan dokumentasi publik, tetapi belum menetapkan seluruh artefak untuk reproduksi historis. Sebelum RPB-001-L dinyatakan dapat direproduksi, R0 masih harus menemukan dan menyimpan:

- commit SHA repository yang benar-benar digunakan untuk implementasi legacy pada `/languages2/`;
- path setiap source file untuk C, Rust, dan Zig;
- SHA-256 dari setiap source file dan script compile/run yang relevan;
- compiler command dan seluruh build flags;
- command Hyperfine lengkap, termasuk konfigurasi warm-up;
- source program dan command invocation yang menjelaskan peran argumen `40` untuk setiap benchmark; halaman menyebut nilai tersebut, tetapi pemetaan argumen ke workload belum dipastikan;
- definisi tipe integer, ukuran array (jika ada), jumlah iterasi, dan operasi pada setiap iterasi; untuk RPB-001-L, penggunaan array belum diketahui sampai source legacy dipatok;
- output/checksum yang membuktikan seluruh pekerjaan benar-benar dilakukan.

Jika source revision persis tidak dapat ditemukan, profil tersebut harus diberi label **historical-page reference, not exact source reproduction**. Jangan menebak atau merekonstruksi source hanya dari judul dan angka.

R0 juga harus mengarsipkan snapshot halaman `/languages/` dan `/languages2/` yang digunakan (misalnya HTML atau WARC jika dapat diperoleh secara sah), mencatat URL final, tanggal/waktu pengambilan, dan SHA-256 snapshot. Jika snapshot tidak dapat diperoleh, catat kegagalan dan simpan metadata serta kutipan yang relevan; jangan mengklaim arsip tersedia.

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
- Untuk loops, mengikuti source dan spesifikasi upstream pada commit SHA yang dipatok. Dokumentasi branch `main` yang diperiksa menyebut 100 juta pembaruan array, tetapi angka tersebut **PENDING SOURCE PINNING** dan bukan fakta fixture final sampai diverifikasi terhadap commit dan file yang diarsipkan.
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

**Batas otorisasi harness:** mode A/B dapat menggunakan command/harness eksternal yang sudah tersedia dan disetujui. Mode C/D memerlukan runner in-process atau instrumentasi khusus. Karena repository saat ini belum memiliki benchmark harness, pembuatan runner, timer internal, atau benchmark-specific CLI untuk C/D adalah pekerjaan baru dan **memerlukan milestone harness terpisah dengan persetujuan owner**. Definisi mode C/D dalam proposal ini hanya spesifikasi pengukuran, bukan izin membuat implementasinya.

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
| Environment | **Required-if-collectable:** power mode/governor, thermal, background load. Jika tidak tersedia, catat `unavailable` dan alasan/platform limitation |

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
- Environment telemetry berstatus **required-if-collectable**, bukan syarat yang memaksa sistem menyediakan sensor/kontrol yang tidak dimilikinya. Jika CPU frequency/governor, thermal telemetry, atau power mode tidak dapat diambil, catat `unavailable` beserta alasan dan platform limitation. Jangan mengklaim dapat mengunci frekuensi pada platform yang tidak menyediakan kontrol tersebut.
- Jalankan beberapa batch independen; urutan bahasa dapat dirotasi agar satu bahasa tidak selalu diuji pada kondisi termal pertama atau terakhir.
- Jangan menggabungkan hasil lintas CPU/OS sebagai satu ranking langsung.

### 5.4 Statistik dan keputusan

Laporan wajib menyimpan semua sampel mentah serta menampilkan mean, median, standard deviation, minimum, maksimum, dan confidence interval 95%.

**Protokol statistik default untuk eksperimen lokal RPR (harus dibekukan sebelum R1):**

- Untuk tiap kandidat dan mode, lakukan 5 warm-up executions yang tidak dihitung, lalu sekurang-kurangnya 30 paired measured batches. Setiap batch memuat satu measured execution untuk reference dan setiap kandidat, dengan urutan yang dirotasi/diacak dan disimpan. Dengan demikian tersedia minimal 30 sampel per implementasi. Untuk benchmark yang memiliki runner upstream, protokol upstream yang dipatok menggantikan angka default ini dan harus dicatat.
- Untuk setiap batch, hitung `log(time_candidate / time_reference)`. Metrik estimasi adalah median dari paired log-ratios tersebut; transformasikan kembali dengan eksponensial untuk memperoleh rasio waktu. Rasio di bawah 1 berarti kandidat lebih cepat.
- Estimator interval: paired bootstrap percentile 95% CI dengan resampling pada unit batch berpasangan, 10.000 resamples, dan deterministic RNG seed `20261117`. Simpan implementasi/statistik script dan seed bersama raw data.
- Kandidat hanya boleh dinyatakan lebih cepat bila batas atas 95% CI rasio berada di bawah 1,00. Kandidat hanya boleh dinyatakan lebih lambat bila batas bawah berada di atas 1,00. Selain itu hasil **inconclusive**.
- Aturan ini adalah protokol proposal untuk pengujian internal; perubahan estimator, resample count, seed, atau threshold setelah data terlihat dilarang. Perubahan hanya boleh dilakukan sebelum R1 dan dicatat sebagai revisi protokol.

Untuk RPB-001-L, statistik yang ditampilkan pada halaman historis tetap dilaporkan sebagaimana sumber menampilkannya; jangan menghitung ulang atau menggabungkannya dengan statistik eksperimen lokal.

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

1. identifikasi tipe integer dan lebar bit pada setiap implementasi, per variabel/operasi yang relevan;
2. catat compiler version, optimization level, dan seluruh flag yang memengaruhi overflow/undefined behavior atau runtime checks (misalnya checked/wrapping mode dan flag spesifik compiler);
3. verifikasi seluruh nilai intermediate pada workload dari source dan, bila perlu, instrumentasi/reference calculation;
4. buktikan bahwa rentang nilai intermediate tidak overflow pada workload yang diklaim setara, atau definisikan perilaku wrapping/checked yang sesuai;
5. simpan bukti range analysis dan konfigurasi build sebagai bagian fixture R0.

Jika seluruh operasi terbukti berada dalam rentang aman, perbedaan kebijakan overflow tidak otomatis membatalkan perbandingan workload tersebut. Jika tidak, perbandingan harus ditandai tidak setara atau workload disesuaikan dan diberi ID baru.

### 6.2 List dan array layout

RANCAGE 0.2 saat ini merepresentasikan list melalui Python `list` dan map melalui Python `dict`; list generik bukan typed contiguous array.

Rationale array-layout pada bagian ini secara langsung relevan terhadap RPB-001-N hanya jika source revision yang dipatok mengonfirmasi workload array-update tersebut. Untuk RPB-001-L, penggunaan array, layout, dan pola akses **UNKNOWN pending R0 source pinning**; judul halaman benchmark saja tidak membuktikan bahwa workload legacy memperbarui array.

Secara umum, array bertipe kontigu pada backend native dapat memiliki layout dan biaya akses berbeda dari list objek Python. Karena itu, laporan harus membedakan:

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
- kompatibilitas dengan IR 0.1/0.2 dan RANCAGE-IR historis;
- strategi pengujian kesetaraan hasil antara VM dan backend lain.

Typed IR design adalah milestone desain. Ia tidak otomatis mengizinkan perubahan kode, format IR publik, atau penghapusan kompatibilitas.

### 8.3 Native backend feasibility

Pilihan yang dapat diteliti setelah Typed IR design:

| Alternatif | Potensi | Risiko/kendala | Status |
|---|---|---|---|
| LLVM | Optimizer matang dan target platform luas | Integrasi, ukuran dependensi, versi LLVM, linking dan runtime | Feasibility study only |
| Cranelift | Backend code generation dan IR yang mendukung compiler JIT/AOT tertentu | Ecosystem/toolchain Rust dan konflik dengan keputusan implementasi RANCAGE yang berlaku | Blocked for implementation pending explicit owner approval |
| Backend mandiri | Kontrol penuh atas format dan kebutuhan RANCAGE | Instruction selection, register allocation, ABI, object file, debug info, portabilitas, maintenance | Research only; not recommended as initial path |

Tidak ada backend yang dipilih dalam RPR v0.3.

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
- penjelasan eksplisit atas bagian yang tidak dapat direproduksi;
- snapshot halaman sumber beserta URL final, retrieval timestamp, dan SHA-256 (atau catatan eksplisit jika snapshot tidak dapat diperoleh);
- verifikasi peran argumen `40` pada masing-masing workload dari source dan command invocation;
- integer width, compiler flags, dan bukti rentang nilai intermediate untuk setiap implementasi pembanding;
- status penggunaan array/layout RPB-001-L; jika belum diketahui, labeli UNKNOWN dan jangan jadikan dasar optimisasi;
- commit SHA dan file hashes untuk RPB-001-N sebelum angka workload pada dokumentasi upstream dianggap spesifikasi fixture.

Exit criteria:
- profil mempunyai identitas revision/hash;
- workload dan result dapat diverifikasi dari source;
- metode pengukuran tidak ambigu;
- legacy/current tidak tercampur.

Jika source historis tidak dapat diidentifikasi, R0 harus menyatakan keterbatasan itu dan tidak boleh mengklaim reproduksi persis angka historis.

### R1 — Local Reference Baseline

Tujuan: memperoleh baseline pembanding pada satu perangkat lokal.

Kandidat minimal: C, Rust, Zig, dan RANCAGE dalam mode yang dapat dijalankan saat itu.

**Batas toolchain dan fixture:** setelah R1 secara eksplisit disetujui, menginstal toolchain C/Rust/Zig untuk membangun program pembanding dan menyimpan fixture benchmark pihak ketiga yang tidak dimodifikasi diperbolehkan sebagai aktivitas eksperimen. Ini tidak mengizinkan penambahan implementasi compiler RANCAGE dalam C/Rust/C++/Zig, file Cargo, atau perubahan kebijakan repository. Setiap pengecualian memerlukan persetujuan owner terpisah.

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

## 11. Temuan audit independen dan disposisi v0.3

Tabel ini mencatat status temuan dari audit Architect v0.1 dan audit independen v0.2. Disposisi pada v0.3 adalah respons penulis proposal; bukan pengganti audit independen berikutnya.

| Finding | Level audit | Disposisi v0.3 |
|---|---|---|
| F-01 / A-01 — historical benchmark source not pinned | HIGH blocker | **UNRESOLVED.** Angka hanya published/source-observed dari `/languages2/`; belum independently reproduced. Tidak boleh digunakan sebagai target atau ranking reproduksi. |
| F-02 — no Typed IR milestone | HIGH | **Addressed in proposal.** R3 Typed IR design tetap tahap desain saja. |
| F-03 — BCE lacks proof mechanism | HIGH | **Addressed in proposal.** BCE blocked by default; proof proposal dan owner approval wajib. |
| F-04 / A-02 — integer overflow semantics | HIGH | **Open pending R0 evidence.** Wajib catat integer width, flags, dan bukti rentang nilai intermediate per implementasi. Tidak boleh mengasumsikan mismatch atau kesetaraan. |
| F-05 / N-5 — environment/statistics incomplete | MEDIUM | **Addressed in proposal.** Environment telemetry required-if-collectable dengan alasan jika unavailable; statistik internal dipatok sebelum R1. |
| F-06 — timing boundaries ambiguous | MEDIUM | **Addressed in proposal.** Empat mode memiliki timing boundary berbeda. |
| F-07 — optimization dependency order unclear | MEDIUM | **Addressed in proposal.** Optimisasi bergantung pada typed IR/profiling/proof sesuai jenisnya. |
| F-08 / N-7 — Cranelift/toolchain policy | MEDIUM | **Clarified.** Toolchain pembanding dan fixture pihak ketiga hanya boleh dipakai setelah R1 disetujui; implementasi compiler RANCAGE dalam bahasa yang dilarang tetap tidak diizinkan. Cranelift tetap perlu persetujuan eksplisit. |
| F-09 / N-3 — array layout vs legacy workload | LOW/HIGH relevance risk | **Scoped.** Array-layout rationale berlaku pada RPB-001-N jika source pinned mengonfirmasi; RPB-001-L array usage UNKNOWN pending R0. |
| F-10 — ranking before baseline | LOW | **Addressed.** Ranking hanya pada R7 dan profil/platform/metode yang setara. |
| F-11/F-12 — OATS separation and governance | INFORMATIONAL | **Retained.** |
| N-1 — `/languages/` vs `/languages2/` methodology | HIGH | **Addressed.** `/languages2/` satu-satunya asal angka tabel historis; `/languages/` hanya konteks dan tidak boleh dicampur. |
| N-2 — input `40` attribution | HIGH | **Partially clarified; source mapping pending.** Kedua halaman menyatakan `Input value of 40 given to each`. RPR tidak menafsirkan `40` sebagai khusus Fibonacci atau sebagai parameter loop sebelum source dan command invocation diperiksa. |
| A-03 — archived page evidence | MEDIUM | **Added to R0.** Snapshot, URL, retrieval timestamp, SHA-256, atau alasan ketidaktersediaannya harus dicatat. |
| N-4 — in-process harness implied | MEDIUM | **Addressed.** Mode C/D hanya definisi; runner/harness baru memerlukan milestone dan persetujuan owner terpisah. |
| N-6 — CI estimator unpinned | MEDIUM | **Addressed in proposal.** Estimator, resample count, seed, dan decision threshold ditentukan sebelum R1. |
| N-8 — upstream `main` facts unpinned | LOW | **Addressed.** Detail 100 juta update ditandai pending source pinning sampai commit SHA dan hash dikunci. |

## 12. Governance dan batas perubahan

- RANCAGE 0.2.0a1 tetap menjadi baseline Stage 0.
- Commit `03c6ec15b31eeddf8210223c32ca98793abe4222` tidak boleh diubah atau di-rewrite.
- Tag `v0.2.0a1` tidak boleh dipindahkan.
- Stage 0 tetap CLOSED dan FROZEN.
- Stage 1 tetap NOT STARTED dan NOT AUTHORIZED sampai owner menyetujuinya.
- RPR v0.3 tidak mengotorisasi perubahan source code, IR format, compiler, VM, runtime quota, atau toolchain.
- Tidak ada native backend, optimizer, benchmark harness, atau benchmark run yang otomatis disetujui oleh dokumen ini.
- Mode C/D adalah definisi metodologi saja. Pembuatan in-process runner, benchmark harness, timer, atau benchmark CLI memerlukan milestone dan persetujuan owner terpisah.
- R1 boleh menggunakan toolchain pembanding dan fixture pihak ketiga hanya setelah R1 disetujui; hal itu tidak mengubah larangan implementasi compiler RANCAGE dalam C/Rust/C++/Zig.
- File Roo Code seperti `.roo/` dan `.roomodes` tetap merupakan artefak lokal tooling dan tidak boleh dimasukkan ke Git.
- Urutan governance untuk milestone penting: Architect → Developer → Auditor → QA Engineer → Owner Approval.

## 13. Keputusan owner yang masih diperlukan

Sebelum proposal ini dapat menjadi roadmap kerja, owner perlu memutuskan:

1. Apakah RPR v0.3 diterima sebagai proposal riset performa, tanpa otorisasi implementasi langsung?
2. Apakah R0 diizinkan untuk mematok source benchmark publik dan menghasilkan fixture dokumentasi saja?
3. Jika commit historis tidak dapat ditemukan, apakah RPB-001-L boleh diganti dengan rekonstruksi baru yang diberi identitas terpisah?
4. Apakah Typed IR design (R3) boleh dibuat sebagai proposal arsitektur tersendiri?
5. Apakah riset Cranelift yang memerlukan toolchain Rust boleh dilakukan, mengingat batasan implementasi compiler yang berlaku?
6. Apakah empat mode pengukuran pada §4 diterima sebagai format laporan resmi, dengan C/D tetap nonaktif sampai milestone harness disetujui?
7. Apakah representasi typed/contiguous array boleh diteliti sebagai proposal desain terpisah, tanpa mengubah semantik list RANCAGE 0.2?
8. Apakah protokol statistik internal pada §5.4 diterima sebelum R1, atau owner ingin menetapkan protokol alternatif sebelum data benchmark dikumpulkan?

## 14. Kesimpulan

RANCAGE tidak akan mengejar posisi pertama hanya dengan mempercepat Python VM. Strategi jangka panjang adalah membangun representasi intermediate yang kuat, mengevaluasi backend native berdasarkan bukti, mengoptimalkan bottleneck yang terukur, serta mempertahankan semantik dan prinsip keselamatan.

Angka historis pada `benjdd.com/languages2/` menjadi motivasi dan referensi publik, bukan janji target waktu. Sasaran kompetitif hanya dapat dinilai setelah benchmark source, toolchain, hardware, dan metode pengukuran dipatok secara dapat direproduksi.

**Status akhir dokumen:** DRAFT v0.3 — REVISED AFTER INDEPENDENT AUDIT. Menunggu audit ulang dan keputusan owner. Verdict audit v0.2 adalah REVISE; tidak ada implementasi yang disetujui.

---

## Referensi eksternal

1. Historical benchmark page: https://benjdd.com/languages/  
   Konteks historis: `/usr/bin/time`, tiga run dengan hasil terendah, M3 MacBook Pro, RAM 16 GB. Halaman menyatakan `Input value of 40 given to each`; pemetaan argumen ke tiap workload wajib diverifikasi dari source.
2. Hyperfine benchmark page: https://benjdd.com/languages2/
   Satu-satunya sumber angka historis Zig/Rust/C dalam tabel RPR; menampilkan mean, standard deviation, range, tiga run, hardware, versi toolchain, serta pernyataan `Input value of 40 given to each`. Angka belum independently reproduced.
3. Upstream repository: https://github.com/bddicken/languages
   Dokumentasi runner in-process, monotonic timing, hasil dan statistik.
4. Upstream loops README: https://github.com/bddicken/languages/tree/main/loops
   Dokumentasi branch `main` yang diperiksa menyebut workload 100 juta pembaruan array. Angka ini pending source pinning; branch `main` harus diganti dengan commit SHA dan source hash pada fixture RPB-001-N sebelum menjadi spesifikasi formal.

**External-source audit note:** halaman web dan dokumentasi upstream telah diperiksa, tetapi SHA commit historis yang tepat dan SHA-256 file benchmark belum dipatok dalam dokumen ini. Itu tetap menjadi deliverable R0. Tidak ada klaim bahwa source historis sudah direproduksi. Pernyataan `Input value of 40 given to each` berasal dari teks halaman; arti argumen per workload tetap belum diverifikasi dari source.

