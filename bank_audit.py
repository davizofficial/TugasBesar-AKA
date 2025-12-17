"""
Aplikasi Audit Transaksi Keuangan Bank
Perbandingan Implementasi Linear Search: Iteratif vs Rekursif
"""

import time
import random
import matplotlib.pyplot as plt
from typing import Optional, Dict, List
from dataclasses import dataclass


@dataclass
class Transaction:
    """Data class untuk menyimpan informasi transaksi"""
    id: str
    tanggal: str
    jenis: str  # DEBIT / KREDIT
    nominal: float
    rekening_asal: str
    rekening_tujuan: str
    keterangan: str


def generate_transactions(n: int) -> List[Transaction]:
    """Generate data transaksi dummy untuk simulasi"""
    jenis_transaksi = ["DEBIT", "KREDIT"]
    keterangan_list = [
        "Transfer antar rekening", "Pembayaran tagihan", "Penarikan tunai",
        "Setoran tunai", "Pembayaran gaji", "Pembelian online",
        "Pembayaran pajak", "Transfer ke bank lain"
    ]
    
    transactions = []
    for i in range(n):
        trans = Transaction(
            id=f"TRX{str(i+1).zfill(6)}",
            tanggal=f"2024-{random.randint(1,12):02d}-{random.randint(1,28):02d}",
            jenis=random.choice(jenis_transaksi),
            nominal=round(random.uniform(10000, 50000000), 2),
            rekening_asal=f"{random.randint(1000000000, 9999999999)}",
            rekening_tujuan=f"{random.randint(1000000000, 9999999999)}",
            keterangan=random.choice(keterangan_list)
        )
        transactions.append(trans)
    return transactions


def linear_search_iterative(transactions: List[Transaction], target_id: str) -> Optional[Transaction]:
    """Linear Search dengan pendekatan Iteratif"""
    for transaction in transactions:
        if transaction.id == target_id:
            return transaction
    return None


def linear_search_recursive(transactions: List[Transaction], target_id: str, index: int = 0) -> Optional[Transaction]:
    """Linear Search dengan pendekatan Rekursif"""
    if index >= len(transactions):
        return None
    if transactions[index].id == target_id:
        return transactions[index]
    return linear_search_recursive(transactions, target_id, index + 1)


def measure_performance(transactions: List[Transaction], target_id: str, iterations: int = 100) -> Dict:
    """Mengukur performa kedua metode pencarian"""
    
    # Ukur waktu Iteratif
    iterative_times = []
    for _ in range(iterations):
        start = time.perf_counter()
        linear_search_iterative(transactions, target_id)
        end = time.perf_counter()
        iterative_times.append((end - start) * 1000)  # Convert to ms
    
    # Ukur waktu Rekursif
    recursive_times = []
    for _ in range(iterations):
        start = time.perf_counter()
        linear_search_recursive(transactions, target_id)
        end = time.perf_counter()
        recursive_times.append((end - start) * 1000)  # Convert to ms
    
    return {
        "iterative_avg": sum(iterative_times) / len(iterative_times),
        "iterative_min": min(iterative_times),
        "iterative_max": max(iterative_times),
        "recursive_avg": sum(recursive_times) / len(recursive_times),
        "recursive_min": min(recursive_times),
        "recursive_max": max(recursive_times),
        "iterative_times": iterative_times,
        "recursive_times": recursive_times
    }


def display_transaction(transaction: Optional[Transaction], target_id: str):
    """Menampilkan detail transaksi yang ditemukan"""
    print("\n" + "=" * 60)
    print("HASIL PENCARIAN TRANSAKSI")
    print("=" * 60)
    
    if transaction:
        print(f"✓ Transaksi dengan ID '{target_id}' DITEMUKAN!")
        print("-" * 60)
        print(f"  ID Transaksi    : {transaction.id}")
        print(f"  Tanggal         : {transaction.tanggal}")
        print(f"  Jenis           : {transaction.jenis}")
        print(f"  Nominal         : Rp {transaction.nominal:,.2f}")
        print(f"  Rekening Asal   : {transaction.rekening_asal}")
        print(f"  Rekening Tujuan : {transaction.rekening_tujuan}")
        print(f"  Keterangan      : {transaction.keterangan}")
    else:
        print(f"✗ Transaksi dengan ID '{target_id}' TIDAK DITEMUKAN!")
    print("=" * 60)


def display_performance_table(results: List[Dict]):
    """Menampilkan tabel perbandingan performa dengan berbagai ukuran N"""
    print("\n" + "+" + "-" * 58 + "+")
    print("|" + " " * 16 + "PERFORMANCE COMPARISON" + " " * 20 + "|")
    print("+" + "-" * 58 + "+")
    print("|" + "-" * 58 + "|")
    print(f"| {'n':>6} | {'Waktu Rekursif (ms)':>20} | {'Waktu Iteratif (ms)':>20} |")
    print("|" + "-" * 58 + "|")
    for r in results:
        print(f"| {r['n']:>6} | {r['recursive_avg']:>20.6f} | {r['iterative_avg']:>20.6f} |")
    print("|" + "-" * 58 + "|")
    print("+" + "-" * 58 + "+")


def plot_performance_comparison(results: List[Dict]):
    """Membuat grafik perbandingan performa Iteratif vs Rekursif"""
    sizes = [r['n'] for r in results]
    iterative_times = [r['iterative_avg'] for r in results]
    recursive_times = [r['recursive_avg'] for r in results]
    
    plt.figure(figsize=(10, 6))
    plt.plot(sizes, iterative_times, 'o-', label='Iterative', color='blue', linewidth=2, markersize=8)
    plt.plot(sizes, recursive_times, 's--', label='Recursive', color='green', linewidth=2, markersize=8)
    
    plt.xlabel('Data Size', fontsize=12)
    plt.ylabel('Execution Time (ms)', fontsize=12)
    plt.title('Perbandingan Waktu Eksekusi Decision Tree: Iteratif vs Rekursif', fontsize=14, fontweight='bold')
    plt.legend(title='Pendekatan', loc='upper left', fontsize=11)
    plt.xticks(sizes)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('performance_comparison.png', dpi=150, bbox_inches='tight')
    plt.show()
    print("\n→ Grafik disimpan sebagai 'performance_comparison.png'")


def run_performance_comparison(sizes: List[int]) -> List[Dict]:
    """Menjalankan perbandingan performa dengan berbagai ukuran data"""
    import sys
    
    print("\n" + "=" * 60)
    print("PERFORMANCE COMPARISON - Berbagai Ukuran Data")
    print("=" * 60)
    
    results = []
    
    # Set recursion limit untuk ukuran data terbesar
    sys.setrecursionlimit(max(sizes) + 500)
    
    for size in sizes:
        print(f"Testing dengan n = {size:,}...", end=" ")
        transactions = generate_transactions(size)
        random.shuffle(transactions)
        target_id = transactions[-1].id  # Worst case: target di akhir
        
        perf = measure_performance(transactions, target_id, iterations=50)
        results.append({
            'n': size,
            'iterative_avg': perf['iterative_avg'],
            'recursive_avg': perf['recursive_avg']
        })
        print("Done!")
    
    return results


def main():
    """Fungsi utama program"""
    print("\n" + "=" * 60)
    print("  APLIKASI AUDIT TRANSAKSI KEUANGAN BANK")
    print("  Linear Search: Iteratif vs Rekursif")
    print("=" * 60)
    
    # Input jumlah data dari user
    print("\n" + "-" * 60)
    print("KONFIGURASI DATA")
    print("-" * 60)
    while True:
        try:
            DATA_SIZE = int(input("Masukkan jumlah transaksi (N): "))
            if DATA_SIZE <= 0:
                print("→ Jumlah harus lebih dari 0!")
                continue
            break
        except ValueError:
            print("→ Input harus berupa angka!")
    
    TEST_ITERATIONS = 100  # Jumlah iterasi untuk pengukuran performa
    
    # Generate data transaksi
    print(f"\n→ Generating {DATA_SIZE:,} data transaksi...")
    transactions = generate_transactions(DATA_SIZE)
    
    # Shuffle/acak urutan data
    random.shuffle(transactions)
    
    # Tampilkan array setelah diacak
    print("\n" + "-" * 60)
    print("List Array Acak ID Transaksi")
    print("-" * 60)
    for i, t in enumerate(transactions[:10]):
        print(f"  [{i}] {t.id}")
    if DATA_SIZE > 10:
        print(f"  ... dan {DATA_SIZE - 10} data lainnya")
    
    print(f"\n→ Data transaksi berhasil di-generate dan diacak!")
    
    # Input ID transaksi yang dicari
    print("\n" + "-" * 60)
    print("PENCARIAN TRANSAKSI")
    print("-" * 60)
    print(f"→ Rentang ID yang tersedia: TRX000001 - TRX{str(DATA_SIZE).zfill(6)}")
    
    target_id = input("\nMasukkan ID Transaksi yang dicari (contoh: TRX000001): ").strip().upper()
    if not target_id:
        target_id = f"TRX{str(DATA_SIZE//2).zfill(6)}"
        print(f"→ Menggunakan ID default: {target_id}")
    
    # Pencarian dengan kedua metode
    print("\n→ Melakukan pencarian...")
    
    # Iteratif
    result_iterative = linear_search_iterative(transactions, target_id)
    
    # Rekursif
    import sys
    sys.setrecursionlimit(max(DATA_SIZE + 100, 1000))
    result_recursive = linear_search_recursive(transactions, target_id)
    
    # Tampilkan hasil pencarian
    display_transaction(result_iterative, target_id)
    
    # Verifikasi konsistensi hasil
    if (result_iterative is None) == (result_recursive is None):
        print("✓ Kedua metode menghasilkan hasil yang konsisten!")
    
    # Performance Comparison - input sizes dari user
    print("\n" + "-" * 60)
    print("KONFIGURASI PERFORMANCE COMPARISON")
    print("-" * 60)
    print("Masukkan ukuran data (N) untuk test performa.")
    print("Pisahkan dengan koma, contoh: 10,20,100,1000,10000")
    
    while True:
        try:
            sizes_input = input("Masukkan sizes: ").strip()
            sizes = [int(x.strip()) for x in sizes_input.split(",")]
            if any(s <= 0 for s in sizes):
                print("→ Semua angka harus lebih dari 0!")
                continue
            sizes.sort()
            break
        except ValueError:
            print("→ Format salah! Gunakan angka dipisah koma, contoh: 10,20,100")
    
    print("\n→ Menjalankan Performance Comparison...")
    results = run_performance_comparison(sizes)
    
    # Tampilkan tabel performa
    display_performance_table(results)
    
    # Tampilkan grafik
    print("\n→ Membuat grafik perbandingan...")
    plot_performance_comparison(results)
    
    print("\n" + "=" * 60)
    print("  AUDIT SELESAI - Terima kasih!")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n→ Program Berhenti.")
        exit(0)
