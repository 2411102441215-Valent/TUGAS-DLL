# Praktikum PBO – Refactoring SOLID & Logging

* **Nama**: Nikon Valent Sakaesa
* **NIM**: 2411102441215
* **Kelas**: C
* **Mata Kuliah**: Praktikum Pemrograman Berorientasi Objek (PBO)

---
## Deskripsi

Repository ini berisi hasil **praktikum Pemrograman Berorientasi Objek (PBO)** yang membahas proses **refactoring kode** dengan menerapkan prinsip **SOLID** serta penggunaan **logging**.

Program yang dibuat merupakan simulasi **sistem validasi registrasi mahasiswa**, yang bertujuan untuk melatih penerapan konsep PBO agar kode menjadi lebih **terstruktur, modular, dan mudah dikembangkan**.

Prinsip SOLID yang diterapkan dalam praktikum ini meliputi:

* **Single Responsibility Principle (SRP)**
* **Open/Closed Principle (OCP)**
* **Dependency Inversion Principle (DIP)**

---

## Struktur Program

Program disusun ke dalam beberapa kelas dengan peran masing-masing, yaitu:

* **RegistrationData**
  Digunakan untuk menyimpan data registrasi mahasiswa.

* **ValidatorManager**
  Contoh implementasi awal yang belum menerapkan prinsip SOLID secara baik. Kelas ini disertakan sebagai bahan pembanding sebelum dilakukan refactoring.

* **IValidationRule**
  Interface yang menjadi dasar bagi seluruh aturan validasi.

* **SksLimitRule**
  Kelas untuk melakukan validasi batas maksimal SKS.

* **PrerequisiteRule**
  Kelas untuk memeriksa apakah mata kuliah prasyarat telah dipenuhi.

* **JadwalBentrokRule**
  Kelas untuk mengecek adanya bentrokan jadwal perkuliahan.

* **RegistrationService**
  Kelas utama yang bertugas menjalankan seluruh aturan validasi dengan menerapkan konsep **dependency injection**.

---

## Penerapan Prinsip SOLID

### 1️. Single Responsibility Principle (SRP)

Setiap kelas validasi hanya memiliki **satu tanggung jawab**, yaitu melakukan satu jenis pengecekan tertentu.

### 2️. Open/Closed Principle (OCP)

Jika ingin menambahkan aturan validasi baru, cukup dengan membuat kelas baru yang mengimplementasikan `IValidationRule` tanpa perlu mengubah kode yang sudah ada pada `RegistrationService`.

### 3️. Dependency Inversion Principle (DIP)

`RegistrationService` tidak bergantung langsung pada kelas validasi tertentu, melainkan pada **interface (`IValidationRule`)**, sehingga kode menjadi lebih fleksibel dan mudah dikembangkan.

---

## Logging

Dalam program ini digunakan modul **`logging`** sebagai pengganti `print()` untuk menampilkan informasi proses validasi.

Logging digunakan untuk:

* Menampilkan awal proses validasi
* Menunjukkan hasil dari setiap aturan validasi
* Menyimpulkan hasil akhir validasi (berhasil atau gagal)

Dengan logging, alur eksekusi program menjadi lebih jelas dan memudahkan proses **debugging**.

---

## Cara Menjalankan Program

Untuk menjalankan program, pastikan Python sudah terinstal, kemudian jalankan perintah berikut melalui terminal:

```bash
python refactor_registration.py
```

Hasil validasi akan ditampilkan dalam bentuk **log di terminal**.

---

## Kesimpulan

Melalui praktikum ini, saya mempelajari bagaimana menerapkan prinsip **SOLID** dalam pemrograman berorientasi objek serta pentingnya penggunaan **logging**.

Hasil refactoring membuat program menjadi:

* Lebih rapi dan terstruktur
* Mudah dikembangkan ke depannya
* Lebih sesuai dengan konsep PBO yang baik

Praktikum ini diharapkan dapat membantu pemahaman saya dalam menulis kode yang lebih profesional dan maintainable.

---

📚 Repository ini dibuat sebagai bagian dari **tugas praktikum mata kuliah Pemrograman Berorientasi Objek (PBO)**.

