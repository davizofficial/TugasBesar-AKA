import time
import random
import matplotlib.pyplot as plt
import sys
from typing import Optional, Dict, List
from dataclasses import dataclass

@dataclass
class Transaction:
    id: str
    tanggal: str
    jenis: str
    nominal: float
    rekening_asal: str
    rekening_tujuan: str
    keterangan: str

def generate_transactions(n: int) -> List[Transaction]:
    """Membuat database transaksi berurutan tanpa angka nol di depan"""
    transactions = []
    for i in range(n):
        trans = Transaction(
            # Menghapus .zfill(6) agar ID menjadi TRX1, TRX2, dst.
            id=f"TRX{i+1}",
            tanggal="2024-12-18",
            jenis=random.choice(["DEBIT", "KREDIT"]),
            nominal=round(random.uniform(10000, 5000000), 2),
            rekening_asal=str(random.randint(10**9, 10**10-1)),
            rekening_tujuan=str(random.randint(10**9, 10**10-1)),
            keterangan="Audit Data"
        )
        transactions.append(trans)
    return transactions

def linear_search_iterative(transactions: List[Transaction], target_id: str) -> Optional[Transaction]:
    for transaction in transactions:
        if transaction.id == target_id:
            return transaction
    return None

def linear_search_recursive(transactions: List[Transaction], target_id: str, index: int = 0) -> Optional[Transaction]:
    if index >= len(transactions): return None
    if transactions[index].id == target_id: return transactions[index]
    return linear_search_recursive(transactions, target_id, index + 1)

def main():
    print("="*60)
    print("   SISTEM AUDIT BANK - KONTROL SKENARIO KOMPLEKSITAS")
    print("="*60)
    
    try:
        n_total = int(input("\nMasukkan jumlah database transaksi (N): "))
    except ValueError:
        print("Input harus angka!")
        return

    database = generate_transactions(n_total)
    
    # 2. Pengacakan Data
    random.shuffle(database)
    print(f"✓ {n_total} data transaksi telah di-generate dan diacak.")

    # 3. MEMBOCORKAN POSISI (Agar Input User Efektif)
    print("\n" + "-"*60)
    print("PANDUAN SKENARIO UNTUK ANALISIS GRAFIK:")
    print("-"*60)
    print(f"1. BEST CASE    (Awal)   : Gunakan ID {database[0].id}")
    print(f"2. AVERAGE CASE (Tengah) : Gunakan ID {database[n_total//2].id}")
    print(f"3. WORST CASE   (Akhir)  : Gunakan ID {database[-1].id}")
    print("-"*60)

    # 4. Input Target dari User
    target_id = input("\nMasukkan ID Transaksi yang ingin dicari: ").strip().upper()

    # 5. Konfigurasi Grafik (Variasi N)
    print("\nMasukkan variasi N untuk skala grafik (pisahkan koma).")
    sizes_input = input("Variasi N: ")
    try:
        sizes = [int(x.strip()) for x in sizes_input.split(",")]
        sizes.sort()
    except ValueError:
        print("Format variasi N salah!")
        return

    # 6. Jalankan Pengujian
    sys.setrecursionlimit(max(sizes) + 2000)
    results = []

    print("\n→ Sedang menghitung performa Linear Search...")
    for n in sizes:
        subset_data = database[:n]
        
        # Pengukuran Iteratif
        start = time.perf_counter()
        linear_search_iterative(subset_data, target_id)
        t_iter = (time.perf_counter() - start) * 1000
        
        # Pengukuran Rekursif
        start = time.perf_counter()
        linear_search_recursive(subset_data, target_id)
        t_rec = (time.perf_counter() - start) * 1000
        
        results.append({'n': n, 'iter': t_iter, 'rec': t_rec})

    # 7. Tampilkan Tabel
    print("\n" + "="*60)
    print(f"{'Ukuran N':<10} | {'Iteratif (ms)':<15} | {'Rekursif (ms)':<15}")
    print("-"*60)
    for r in results:
        print(f"{r['n']:<10} | {r['iter']:<15.6f} | {r['rec']:<15.6f}")

    # 8. Tampilkan Grafik
    plt.figure(figsize=(10, 6))
    plt.plot([r['n'] for r in results], [r['iter'] for r in results], 'o-', label='Iteratif', color='blue')
    plt.plot([r['n'] for r in results], [r['rec'] for r in results], 's--', label='Rekursif', color='red')
    plt.title(f"Analisis Linear Search: Mencari {target_id}")
    plt.xlabel("Jumlah Data (N)")
    plt.ylabel("Waktu (ms)")
    plt.legend()
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    main()
