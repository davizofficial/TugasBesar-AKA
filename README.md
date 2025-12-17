# Aplikasi Audit Transaksi Keuangan Bank

Tugas Besar Mata Kuliah Analisis Kompleksitas Algoritma

## Deskripsi

Program ini mensimulasikan sistem audit transaksi keuangan di bank dengan membandingkan dua pendekatan implementasi algoritma Linear Search:
- Linear Search Iteratif
- Linear Search Rekursif

Program bertujuan untuk memverifikasi keberadaan satu ID Transaksi (Target) dan mengecek isi data dari ID tersebut.

## Fitur

- Generate data transaksi dummy sesuai input user (N)
- Data transaksi diacak secara random sebelum pencarian
- Pencarian transaksi berdasarkan ID menggunakan Linear Search
- Perbandingan performa antara metode Iteratif dan Rekursif
- User dapat menentukan ukuran data untuk performance comparison
- Visualisasi grafik perbandingan performa
- Mendukung Ctrl+C untuk menghentikan program

## Struktur Data Transaksi

| Field | Deskripsi |
|-------|-----------|
| ID Transaksi | Identifier unik transaksi (format: TRX000001) |
| Tanggal | Tanggal transaksi |
| Jenis | DEBIT atau KREDIT |
| Nominal | Jumlah uang dalam Rupiah |
| Rekening Asal | Nomor rekening pengirim |
| Rekening Tujuan | Nomor rekening penerima |
| Keterangan | Deskripsi transaksi |

## Algoritma Linear Search

### Iteratif
```python
def linear_search_iterative(transactions, target_id):
    for transaction in transactions:
        if transaction.id == target_id:
            return transaction
    return None
```

### Rekursif
```python
def linear_search_recursive(transactions, target_id, index=0):
    if index >= len(transactions):
        return None
    if transactions[index].id == target_id:
        return transactions[index]
    return linear_search_recursive(transactions, target_id, index + 1)
```

## Kompleksitas Algoritma

| Metode | Time Complexity | Space Complexity |
|--------|-----------------|------------------|
| Iteratif | O(n) | O(1) |
| Rekursif | O(n) | O(n) - karena call stack |

Keterangan:
- n = jumlah data transaksi
- Kedua metode memiliki time complexity yang sama yaitu O(n) untuk worst case
- Perbedaan utama terletak pada space complexity dimana rekursif membutuhkan ruang tambahan untuk call stack

## Cara Menjalankan

### Prasyarat
- Python 3.x
- Library matplotlib

### Instalasi
```bash
pip install matplotlib
```

### Menjalankan Program
```bash
python bank_audit.py
```

## Alur Program

1. User memasukkan jumlah data transaksi (N) yang ingin di-generate
2. Program generate N data transaksi dummy dan mengacak urutannya
3. Menampilkan list array acak ID transaksi (10 data pertama)
4. Menampilkan rentang ID yang tersedia (TRX000001 - TRX00000N)
5. User memasukkan ID transaksi yang ingin dicari
6. Program melakukan pencarian dengan kedua metode (Iteratif & Rekursif)
7. Menampilkan detail transaksi jika ditemukan
8. User memasukkan ukuran data untuk performance comparison (pisahkan dengan koma, contoh: 10,20,100,1000,10000)
9. Menampilkan tabel perbandingan performa
10. Menampilkan grafik perbandingan performa

## Contoh Output

```
============================================================
  APLIKASI AUDIT TRANSAKSI KEUANGAN BANK
  Linear Search: Iteratif vs Rekursif
============================================================

------------------------------------------------------------
KONFIGURASI DATA
------------------------------------------------------------
Masukkan jumlah transaksi (N): 100

→ Generating 100 data transaksi...

------------------------------------------------------------
List Array Acak ID Transaksi
------------------------------------------------------------
  [0] TRX000047
  [1] TRX000023
  [2] TRX000089
  ...
  ... dan 90 data lainnya

→ Data transaksi berhasil di-generate dan diacak!

------------------------------------------------------------
PENCARIAN TRANSAKSI
------------------------------------------------------------
→ Rentang ID yang tersedia: TRX000001 - TRX000100

Masukkan ID Transaksi yang dicari (contoh: TRX000001): TRX000050

+----------------------------------------------------------+
|                PERFORMANCE COMPARISON                    |
+----------------------------------------------------------+
|      n |   Waktu Rekursif (ms) |   Waktu Iteratif (ms) |
|----------------------------------------------------------| 
|     10 |             0.012345 |             0.010234 |
|    100 |             0.123456 |             0.098765 |
|   1000 |             1.234567 |             0.987654 |
+----------------------------------------------------------+
```

## Hasil Perbandingan Performa

### Grafik Performance Comparison
![Performance Comparison](performance_comparison.png)

Grafik menunjukkan perbandingan waktu eksekusi kedua metode pada berbagai ukuran data yang diinput oleh user.

## Kesimpulan

Berdasarkan hasil pengujian:
- Kedua metode memiliki kompleksitas waktu O(n) yang sama
- Metode iteratif lebih efisien dalam penggunaan memori karena tidak memerlukan call stack
- Metode rekursif memiliki keterbatasan pada ukuran data besar karena limit recursion depth
- Untuk aplikasi praktis dengan data besar, metode iteratif lebih disarankan

## Teknologi

- Python 3
- Matplotlib (visualisasi grafik)
