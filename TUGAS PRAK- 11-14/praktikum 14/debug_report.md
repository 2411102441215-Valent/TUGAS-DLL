# debug_report.md

A. Identitas Mahasiswa :
Nama : Nikon Valent Sakaesa
NIM : 2411102441215
Kelas : C

---

## Catatan Kesalahan / Debugging Bug PPN / Diskon

### 1. Deskripsi Masalah-nya

Saat menjalankan unit test pada file `test_diskon.py`, beberapa test gagal dan menghasilkan nilai harga akhir negatif, misalnya diskon 10% dari harga 1000 menghasilkan -9000. Hal ini menunjukkan adanya kesalahan logika pada perhitungan diskon di file `diskon_services.py`.

---

### 2. Gejala Bug

Beberapa gejala yang ditemukan:

- Harga akhir menjadi negatif.
- Diskon 10% dianggap sebagai 1000%.
- Test boundary seperti diskon 100% dan diskon >100% gagal.
- Output unittest menunjukkan status **FAILED** (dengan 8 kali total percobaan pada sistem).

---

### 3. Analisis Penyebab

Bug disebabkan oleh kesalahan rumus perhitungan diskon, yaitu persentase diskon tidak dibagi 100, akibatnya kode akan kacau.  
Kode bermasalah:

```python
jumlah_diskon = harga_awal * persentase_diskon
```

---

## Debug Log Bug PPN 10% menggunakan pdb

### 1. Tujuan Debugging

Debugging dilakukan untuk menemukan penyebab kesalahan perhitungan harga akhir, khususnya bug PPN 10% yang menyebabkan nilai harga menjadi tidak sesuai dengan hasil yang diharapkan.

---

### 2. Langkah Debugging dengan pdb

Debugging dilakukan dengan menambahkan breakpoint pada fungsi `hitung_diskon()` di file `diskon_services.py`.

Kode breakpoint-nya:

```python
import pdb
pdb.set_trace()
```

---

### 3. Proses Penelusuran Bug

Sesaat program dijalankan menggunakan unittest, eksekusi berhenti pada breakpoint. Beberapa perintah `p` digunakan untuk memeriksa nilai variabel:

```python
(Pdb) p harga_awal
1000

(Pdb) p persentase_diskon
10

(Pdb) p jumlah_diskon
10000
```

Hasil di atas menunjukkan bahwa diskon 10% dihitung sebagai 10000, yang menandakan bahwa persentase tidak dibagi 100. Jika PPN dihitung kembali setelah pengurangan harga, nilai menjadi semakin tidak wajar dan menghasilkan harga akhir negatif.

---

### 4. Bukti Bug PPN / Diskon Ganda

```python
(Pdb) p harga_akhir
-9000
```

Nilai tersebut kurang sesuai dengan hasil yang seharusnya (900.0), sehingga dapat disimpulkan bahwa perhitungan diskon/PPN dilakukan secara keliru (sengaja).

---

### 5. Solusi Perbaikan Bug

Solusi perbaikan dilakukan dengan mengubah rumus perhitungan diskon di file `diskon_services.py` menjadi:

```python
jumlah_diskon = harga_awal * (persentase_diskon / 100)
```

setelah itu, nilai variabel diuji ulang menggunakan pdb dan menghasilkan nilai yang sesuai.

---

### 6. Hasil akhirnya

Setelah bug diperbaiki:
    - Perhitungan diskon menjadi benar
    - Harga akhir tidak bernilai negatif
    - Seluruh unit test pada test_diskon.py lulus (OK)

---

### 7. Kesimpulan

Penggunaan pdb, itu sangat membantu dalam menelusuri nilai variabel secara langsung dan perlu membuktikan adanya kesalahan logika dalam perhitungan diskon/PPN. Kemudian Bug berhasil ditemukan dan diperbaiki dengan validasi yang seharusnya. Dengan hasil output unittest yang menunjukkan semua test lulus (OK).

---
