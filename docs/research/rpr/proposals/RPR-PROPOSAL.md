# RANCAGE Performance Roadmap (RPR)

**Dokumen:** Rancangan strategi performa dan benchmark  
**Versi:** 0.1 — Proposal  
**Status:** DRAFT — Belum disetujui untuk implementasi  
**Baseline:** RANCAGE 0.2.0a1  
**Tujuan jangka panjang:** Membangun bahasa pemrograman yang mampu bersaing secara performa dengan Zig, Rust, dan C.

---

## 1. Visi

RANCAGE harus dikembangkan menjadi bahasa pemrograman yang memiliki tiga karakteristik utama:

- **Lightweight:** penggunaan memori efisien, runtime ringan, startup cepat, dan dependensi minimal.
- **Safe:** sistem tipe kuat, null safety, bounds checking, serta batas sumber daya yang terkontrol.
- **Strong:** compiler yang matang, optimisasi efektif, dan kemampuan menghasilkan program berkinerja tinggi.

Performa tinggi merupakan sasaran strategis, tetapi tidak boleh dicapai dengan mengorbankan ketiga prinsip tersebut.

Target jangka panjang adalah membuat RANCAGE kompetitif pada benchmark komputasi, bukan hanya membuat interpreter berjalan lebih cepat.

## 2. Sasaran benchmark

### 2.1 Benchmark utama: Nested Loop dan Array Update

Referensi:

- https://benjdd.com/languages/
- https://benjdd.com/languages2/
- https://github.com/bddicken/languages

Benchmark ini menguji pekerjaan komputasi yang berulang, dengan operasi sederhana dan pembaruan array.

Angka historis yang menjadi motivasi penelitian:

| Bahasa | Waktu historis |
|---|---:|
| Zig | 510,5 ms |
| Rust | 515,1 ms |
| C | 518,8 ms |

Angka tersebut bukan target waktu universal. Hasil berasal dari perangkat, versi compiler, konfigurasi, dan metode pengujian tertentu.

### 2.2 Dua profil benchmark

RANCAGE tidak boleh mencampur dua generasi pengujian.

**RPB-001-L — Legacy Compatibility**

Tujuan: mereproduksi benchmark historis yang menjadi asal angka Zig 510,5 ms, Rust 515,1 ms, dan C 518,8 ms.

Aturan:
- Menggunakan kode dan operasi yang sama dengan implementasi historis.
- Menggunakan argumen yang sama.
- Mempertahankan jumlah iterasi, operasi aritmetika, tipe data, serta cara pembaruan array.
- Mempertahankan metode pengukuran yang sesuai dengan hasil historis.
- Menyimpan versi sumber benchmark dan hash berkas yang diuji.

Source code dan revisi upstream yang tepat harus dikunci sebelum benchmark dinyatakan kompatibel. Jangan merekonstruksi workload hanya dari judul atau angka di halaman web.

**RPB-001-N — Current Upstream Compatibility**

Tujuan: mengikuti versi benchmark terbaru dari repositori `bddicken/languages`.

Aturan:
- Mengikuti implementasi benchmark terbaru, bukan menganggapnya identik dengan versi historis.
- Mengikuti runner in-process dan ketentuan warm-up.
- Mengukur fungsi yang menjadi objek benchmark, bukan mencampur waktu startup dengan waktu komputasi.
- Melaporkan mean, standard deviation, minimum, maksimum, jumlah pengulangan, dan hasil komputasi.
- Mempertahankan input dan aturan validasi hasil dari versi upstream yang dipilih.

Kedua profil menghasilkan laporan terpisah. Tidak boleh menggunakan hasil satu profil untuk mengklaim posisi pada profil lainnya.

## 3. Standar pengujian RANCAGE

Setiap pengujian harus mencatat setidaknya:

| Data | Keterangan |
|---|---|
| Benchmark ID | Identitas workload dan profil |
| Source revision | Versi sumber benchmark |
| Source hash | SHA-256 kode yang diuji |
| Language version | Versi RANCAGE atau bahasa pembanding |
| Compiler version | Versi compiler dan toolchain |
| Build flags | Seluruh konfigurasi optimisasi |
| CPU | Model prosesor |
| RAM | Kapasitas memori |
| OS | Sistem operasi dan versinya |
| Architecture | x64, ARM64, dan sebagainya |
| Runtime | Interpreter, VM, JIT, atau native |
| Input | Argumen benchmark |
| Result | Hasil komputasi untuk validasi |
| Timing | Mean, median, standard deviation, min, max |
| Repetitions | Jumlah pengujian |

### Aturan pengukuran

1. Semua bahasa harus dijalankan pada mesin yang sama untuk perbandingan lokal.
2. Jangan membandingkan waktu mentah MacBook M3 dengan komputer Windows yang berbeda dan menyebutnya sebagai peringkat yang setara.
3. Catat waktu build secara terpisah dari waktu eksekusi.
4. Catat waktu startup secara terpisah dari waktu komputasi.
5. Gunakan jam monotonic untuk pengukuran internal.
6. Jalankan beberapa pengulangan dan simpan data mentah.
7. Lakukan warm-up jika metode benchmark mengharuskannya.
8. Hindari aktivitas lain yang mengganggu pengujian.
9. Jangan memilih hanya satu hasil tercepat untuk menyembunyikan variasi pengujian.
10. Validasi hasil komputasi sebelum menerima angka performa.

Untuk reproduksi angka historis, metode lama tetap harus diikuti. Untuk evaluasi internal RANCAGE, gunakan laporan statistik yang lebih lengkap.

## 4. Tiga kategori pengukuran

Performa RANCAGE harus diukur dalam tiga kategori berbeda.

### A. Source-to-run

Mengukur waktu dari perintah menjalankan source code hingga program selesai.

Contoh konseptual:

`cage run benchmark.cage`

Pengukuran ini dapat melibatkan:
- Startup proses.
- Lexing dan parsing.
- Type checking.
- Kompilasi ke bytecode.
- Inisialisasi VM.
- Eksekusi program.

### B. Precompiled bytecode execution

Mengukur waktu menjalankan bytecode yang sebelumnya sudah dibuat.

Contoh konseptual:

`cage run benchmark.rcb`

Kategori ini membantu memisahkan biaya compiler frontend dari biaya runtime VM.

### C. Native execution

Mengukur waktu eksekusi program yang telah dikompilasi menjadi executable native.

Kategori ini menjadi sasaran utama kompetisi performa dengan bahasa compiled seperti Zig, Rust, dan C.

Ketiga kategori tidak boleh digabung menjadi satu angka tanpa penjelasan.

## 5. Strategi arsitektur performa

### 5.1 Mempertahankan frontend RANCAGE

Frontend yang sudah dibangun tetap menjadi fondasi:

- Lexer.
- Parser.
- AST.
- Type checker.
- Semantic validation.

Optimisasi backend tidak boleh mengubah semantik bahasa secara diam-diam.

### 5.2 Pengembangan typed intermediate representation

Typed IR menjadi penghubung antara frontend dan backend.

Tujuan:
- Mempertahankan informasi tipe.
- Mempermudah analisis data.
- Menyederhanakan optimisasi.
- Menghasilkan instruksi yang lebih dekat dengan operasi mesin.
- Memungkinkan lebih dari satu backend di masa depan.

### 5.3 Optimizing compiler

Optimisasi yang dapat diteliti secara bertahap:

1. Constant folding.
2. Dead code elimination.
3. Common subexpression elimination.
4. Loop-invariant code motion.
5. Induction variable optimization.
6. Function inlining.
7. Register allocation.
8. Bounds-check elimination yang terbukti aman.
9. Pengurangan overhead pemanggilan fungsi.
10. Vectorization atau SIMD jika didukung dan terbukti menguntungkan.

Optimisasi harus didasarkan pada pengukuran dan correctness test. Jangan menambahkan optimisasi hanya karena populer di bahasa lain.

### 5.4 Native backend

RANCAGE perlu mengevaluasi jalur menuju executable native.

Alternatif penelitian:

- LLVM backend.
- Cranelift backend.
- Backend native yang dirancang sendiri.

Belum ada keputusan untuk memilih salah satunya.

Setiap alternatif harus dievaluasi berdasarkan:
- Kualitas kode mesin.
- Waktu kompilasi.
- Ukuran binary.
- Penggunaan memori.
- Kemudahan debugging.
- Dukungan platform.
- Integrasi dengan sistem tipe dan aturan keamanan RANCAGE.
- Biaya pemeliharaan jangka panjang.

VM tetap berguna sebagai execution reference, debugging path, dan sarana pengujian konsistensi hasil.

### 5.5 Data structure dan memory layout

Benchmark nested loop menguji pembaruan elemen array secara berulang. Karena itu, representasi struktur data sangat penting.

Area penelitian:
- Array bertipe dengan penyimpanan kontigu.
- Pengurangan boxing dan unboxing.
- Pengurangan dynamic dispatch.
- Akses memori yang efisien.
- Pengurangan alokasi objek sementara.
- Locality dan cache behavior.

RANCAGE tidak boleh mengganti array dengan representasi yang secara material berbeda lalu mengklaim hasilnya sebagai reproduksi identik tanpa dokumentasi.

Dukungan tipe integer dan layout harus mengikuti desain bahasa yang disetujui. Setiap perbedaan ukuran elemen atau aturan overflow harus dicatat.

## 6. Tahapan pengembangan yang diusulkan

Semua tahapan di bawah ini merupakan usulan penelitian. Tidak ada tahap implementasi yang otomatis disetujui oleh dokumen ini.

### R0 — Benchmark Specification

Tujuan: menetapkan dasar pengukuran yang sah.

Deliverables:
- RPB-001-L specification.
- RPB-001-N specification.
- Source revision yang dikunci.
- Source hash.
- Referensi implementasi C, Rust, dan Zig.
- Aturan validasi hasil.
- Format laporan benchmark.

Exit criteria:
- Workload dapat direproduksi.
- Input dan output telah diverifikasi.
- Perbedaan benchmark historis dan terbaru terdokumentasi.
- Metode pengukuran tidak ambigu.

### R1 — Local Baseline

Tujuan: mengukur kondisi perangkat pengembangan RANCAGE.

Pengujian:
- C reference.
- Rust reference.
- Zig reference.
- RANCAGE VM pada skala yang aman dan terukur.

Deliverables:
- Benchmark report.
- Data mentah setiap pengujian.
- Profil biaya komputasi.
- Identifikasi hambatan utama RANCAGE.

Catatan: hasil dari komputer lokal hanya menjadi baseline lokal, bukan perbandingan langsung dengan MacBook M3 di publikasi.

### R2 — VM Performance Analysis

Tujuan: mengetahui bagian VM yang paling banyak menghabiskan waktu.

Area analisis:
- Dispatch opcode.
- Stack operations.
- Loop control.
- Arithmetic operations.
- Array access.
- Runtime allocation.
- Function calls.

Tidak boleh mengubah batas default VM hanya untuk menyelesaikan benchmark besar.

Pengujian skala besar harus opt-in, terisolasi, dan memiliki timeout.

### R3 — Native Backend Feasibility

Tujuan: mengevaluasi jalur native execution.

Deliverables:
- Perbandingan LLVM, Cranelift, dan backend mandiri.
- Prototype terbatas jika kelak diizinkan.
- Evaluasi ukuran binary.
- Evaluasi startup.
- Evaluasi throughput.
- Evaluasi kompatibilitas semantik dan keamanan.

Belum ada komitmen untuk memilih backend tertentu.

### R4 — Native Code Generation

Tujuan: menghasilkan executable native yang konsisten dengan semantik RANCAGE.

Acceptance criteria:
- Program native menghasilkan output sama dengan VM.
- Error dan aturan tipe tetap konsisten.
- Optimisasi tidak menghilangkan pemeriksaan keamanan yang diperlukan.
- Binary dapat dijalankan tanpa interpreter Python sebagai dependency runtime.
- Hasil benchmark dapat direproduksi.

### R5 — Performance Optimization

Tujuan: meningkatkan performa berdasarkan data profiling nyata.

Prioritas optimisasi ditentukan dari hasil pengukuran, bukan asumsi.

Setiap optimisasi harus mempunyai:
- Hipotesis.
- Pengujian correctness sebelum dan sesudah.
- Pengukuran performa.
- Evaluasi penggunaan memori.
- Audit keamanan.
- Dokumentasi trade-off.

### R6 — Competitive Benchmarking

Tujuan: mengukur posisi RANCAGE terhadap bahasa lain.

Bahasa pembanding minimal:
- C.
- Rust.
- Zig.

Pengujian dilakukan pada perangkat keras dan aturan yang sama.

Laporan harus menampilkan:
- Waktu eksekusi.
- Variasi hasil.
- Ukuran binary.
- Waktu kompilasi.
- Penggunaan memori.
- Mode eksekusi.
- Hasil correctness.

Target akhirnya adalah performa kompetitif dan, jika hasil pengujian mendukung, mengejar posisi pertama pada benchmark yang sama.

## 7. Menjaga prinsip keamanan RANCAGE

Optimisasi performa tidak boleh menjadi alasan untuk menghapus prinsip keselamatan.

Ketentuan:

1. Type safety tetap berlaku.
2. Null safety tidak boleh dihilangkan.
3. Bounds checking tetap dilakukan kecuali compiler dapat membuktikan akses aman.
4. Arithmetic semantics harus tetap konsisten.
5. Optimisasi tidak boleh melewati batas resource secara diam-diam.
6. VM tetap memiliki batas default yang telah disetujui.
7. Mode benchmark khusus tidak boleh mengubah konfigurasi produksi secara global.
8. Setiap fitur unsafe, bila kelak ada, harus mempunyai rancangan dan persetujuan terpisah.

Benchmark besar bukan alasan untuk menghilangkan proteksi runtime.

## 8. Hubungan dengan OATS-016

OATS-016 dan RPB-001 mempunyai tujuan berbeda.

**OATS-016:**
- Menguji kemampuan VM menghadapi iterasi nested loop sangat besar.
- Memeriksa perilaku batas instruksi dan penghentian yang aman.
- Menjadi pengujian stress dan resource control.

**RPB-001:**
- Menguji performa komputasi dan pembaruan array.
- Mengikuti workload benchmark referensi.
- Mengukur kecepatan eksekusi dan kualitas optimisasi.

Keduanya tidak boleh dianggap sebagai tes yang sama.

RPB-001 tidak boleh dijadikan bagian dari test suite reguler yang otomatis menjalankan workload miliaran iterasi.

## 9. Indikator keberhasilan

Kemajuan tidak hanya dinilai dari satu angka waktu.

| Indikator | Sasaran |
|---|---|
| Correctness | Hasil identik dengan reference |
| Native execution | Dapat menghasilkan executable native |
| Runtime overhead | Semakin rendah |
| Compilation overhead | Terukur dan semakin efisien |
| Memory usage | Terukur dan terkendali |
| Binary size | Terukur dan kompetitif |
| Benchmark reproducibility | Konsisten |
| Security | Tidak menurunkan jaminan keamanan |
| Portability | Bertambah secara bertahap |
| Performance ranking | Meningkat berdasarkan pengujian adil |

Target angka performa baru ditentukan setelah R1 menghasilkan baseline lokal yang valid.

## 10. Batas perubahan dan governance

Rancangan ini tidak mengubah status proyek saat ini.

- RANCAGE 0.2.0a1 tetap menjadi baseline Stage 0.
- Commit `03c6ec15b31eeddf8210223c32ca98793abe4222` tetap tidak diubah.
- Tag `v0.2.0a1` tidak dipindahkan.
- RPB-001 tidak otomatis masuk ke Stage 0.
- Stage 1 tetap belum dimulai dan belum mendapat otorisasi implementasi.
- Tidak ada perubahan source code yang disetujui oleh dokumen ini.
- Setiap milestone memerlukan proposal dan persetujuan pemilik proyek.

Urutan governance tetap:

**Architect → Developer → Auditor → QA Engineer → Owner Approval**

Tidak ada implementasi sebelum spesifikasi arsitektur dan ruang lingkupnya disetujui.

## 11. Keputusan yang masih harus ditetapkan

Sebelum implementasi, pemilik proyek dan Architect harus menetapkan:

1. Revisi upstream mana yang akan digunakan sebagai referensi historis.
2. Apakah RPB-001-L dan RPB-001-N keduanya akan dipelihara.
3. Toolchain native pertama yang didukung.
4. Target platform awal.
5. Pilihan backend setelah feasibility study.
6. Kebijakan pengukuran waktu dan memori.
7. Batas resource untuk benchmark opt-in.

---

## Kesimpulan

RANCAGE tidak akan mencoba mengejar posisi pertama hanya dengan mempercepat Python VM.

Strategi jangka panjangnya adalah membangun compiler yang mampu menghasilkan kode native berkualitas tinggi, dengan representasi data yang efisien, optimisasi yang terukur, dan semantik yang tetap aman.

**Visi performanya: RANCAGE harus ringan saat dijalankan, efisien saat menggunakan memori, dan kuat saat menghasilkan kode mesin.**

Posisi pertama merupakan sasaran kompetitif jangka panjang, bukan klaim yang boleh dibuat sebelum hasil benchmark membuktikannya.