# Refactoring Sistem Validasi Registrasi Mahasiswa

* **Nama**: Nikon Valent Sakaesa
* **NIM**: 2411102441215
* **Kelas**: C
* **Mata Kuliah**: Praktikum Pemrograman Berorientasi Objek (PBO)

---

## Latar Belakang Studi Kasus

Studi kasus ini membahas proses refactoring pada sistem validasi registrasi mahasiswa. Pada implementasi awal, proses validasi masih ditangani oleh satu class menggunakan percabangan `if/else`. Pola tersebut menyebabkan kode sulit dikembangkan dan tidak sesuai dengan prinsip desain berorientasi objek. Oleh karena itu, dilakukan perbaikan desain dengan menerapkan prinsip **SOLID**, khususnya SRP, OCP, dan DIP.

---

## Kondisi Kode Sebelum Refactoring

Pada tahap awal, seluruh aturan validasi ditempatkan di dalam satu class bernama `ValidatorManager`. Method `validate()` pada class tersebut bertugas untuk:

* Mengecek batas maksimal pengambilan SKS
* Memastikan prasyarat mata kuliah telah terpenuhi
* Mendeteksi kemungkinan bentrokan jadwal

Pendekatan ini membuat satu class memiliki terlalu banyak tanggung jawab dan ketergantungan langsung terhadap detail aturan validasi.

---

## Analisis Pelanggaran Prinsip SOLID

### 1. Single Responsibility Principle (SRP)

Class `ValidatorManager` menjalankan beberapa fungsi validasi sekaligus. Hal ini bertentangan dengan SRP karena satu class seharusnya hanya memiliki satu alasan untuk berubah.

### 2. Open/Closed Principle (OCP)

Setiap penambahan aturan validasi baru mengharuskan perubahan pada method `validate()`. Dengan demikian, kode tidak bersifat tertutup terhadap perubahan dan berpotensi menimbulkan bug pada logika yang sudah ada.

### 3. Dependency Inversion Principle (DIP)

`ValidatorManager` bergantung langsung pada implementasi konkret aturan validasi. Tidak terdapat lapisan abstraksi yang memisahkan antara logika tingkat tinggi dan detail implementasi.

---

## Desain Sistem Setelah Refactoring

### Aturan Validasi

Untuk mengatasi permasalahan tersebut, dibuat sebuah interface bernama `IValidationRule` yang berfungsi sebagai kontrak umum bagi seluruh aturan validasi.

### Implementasi Aturan Validasi

Aturan validasi dipisahkan ke dalam beberapa class terpisah, yaitu:

* `SksLimitRule` untuk memeriksa batas maksimum SKS
* `PrerequisiteRule` untuk memeriksa prasyarat mata kuliah
* `JadwalBentrokRule` untuk mendeteksi bentrokan jadwal (sebagai challenge)

### RegistrationService sebagai Koordinator

Class `RegistrationService` berperan sebagai pengelola proses validasi. Class ini menerima kumpulan `IValidationRule` melalui mekanisme **Dependency Injection**, sehingga tidak bergantung pada implementasi aturan tertentu.

---

## Pembuktian Prinsip Open/Closed (Challenge)

Aturan validasi baru berupa `JadwalBentrokRule` dapat ditambahkan tanpa melakukan perubahan pada kode `RegistrationService`. Cukup dengan menyuntikkan rule baru ke dalam daftar aturan, sistem dapat langsung menggunakan validasi tambahan tersebut.

---

## Refleksi

Melalui tugas ini, penulis memahami bahwa penggunaan struktur `if/else` secara berlebihan dapat menyebabkan kode sulit dipelihara dan dikembangkan. Pada implementasi awal, setiap penambahan aturan validasi mengharuskan perubahan langsung pada class utama, sehingga berisiko menimbulkan kesalahan baru.

Dengan menerapkan prinsip Dependency Injection, logika utama tidak lagi bergantung pada detail implementasi aturan validasi. Setiap aturan berdiri secara independen dan dapat ditambahkan atau dihapus tanpa memengaruhi struktur sistem secara keseluruhan. Pendekatan ini membuat kode lebih fleksibel, terstruktur, dan sesuai dengan konsep pemrograman berorientasi objek.

Selain itu, pemisahan tanggung jawab ke dalam class yang lebih kecil membantu penulis memahami pentingnya desain yang modular. Refactoring ini menunjukkan bahwa penerapan prinsip SOLID tidak hanya bersifat teoritis, tetapi sangat berguna dalam pengembangan perangkat lunak yang berkelanjutan.

---

## Kesimpulan

Melalui proses refactoring ini, sistem validasi registrasi mahasiswa menjadi lebih terstruktur, fleksibel, dan mudah dikembangkan. Penerapan prinsip SRP, OCP, dan DIP berhasil menghilangkan ketergantungan berlebih serta menghindari penggunaan `if/else` yang kompleks. Pendekatan ini juga memudahkan penambahan aturan validasi baru tanpa harus memodifikasi kode yang sudah ada.
