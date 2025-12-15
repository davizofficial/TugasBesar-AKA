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


def display_performance(perf: Dict, data_size: int):
    """Menampilkan hasil perbandingan performa"""
    print("\n" + "=" * 60)
    print("PERFORMANCE COMPARISON - LINEAR SEARCH")
    print(f"Data Size: {data_size:,} transaksi")
    print("=" * 60)
    print(f"{'Metode':<15} {'Avg (ms)':<12} {'Min (ms)':<12} {'Max (ms)':<12}")
    print("-" * 60)
    print(f"{'Iteratif':<15} {perf['iterative_avg']:<12.6f} {perf['iterative_min']:<12.6f} {perf['iterative_max']:<12.6f}")
    print(f"{'Rekursif':<15} {perf['recursive_avg']:<12.6f} {perf['recursive_min']:<12.6f} {perf['recursive_max']:<12.6f}")
    print("-" * 60)
    
    diff = ((perf['recursive_avg'] - perf['iterative_avg']) / perf['iterative_avg']) * 100
    if diff > 0:
        print(f"→ Iteratif lebih cepat {abs(diff):.2f}% dari Rekursif")
    else:
        print(f"→ Rekursif lebih cepat {abs(diff):.2f}% dari Iteratif")
    print("=" * 60)


def plot_performance(perf: Dict, data_size: int):
    """Membuat grafik perbandingan performa"""
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    fig.suptitle(f'Perbandingan Performa Linear Search: Iteratif vs Rekursif\n(Data: {data_size:,} transaksi)', 
                 fontsize=14, fontweight='bold')
    
    # Grafik 1: Bar Chart - Rata-rata waktu eksekusi
    methods = ['Iteratif', 'Rekursif']
    avg_times = [perf['iterative_avg'], perf['recursive_avg']]
    colors = ['#2ecc71', '#e74c3c']
    
    bars = axes[0].bar(methods, avg_times, color=colors, edgecolor='black', linewidth=1.2)
    axes[0].set_ylabel('Waktu (ms)', fontsize=11)
    axes[0].set_title('Rata-rata Waktu Eksekusi', fontsize=12)
    axes[0].set_ylim(0, max(avg_times) * 1.3)
    
    for bar, val in zip(bars, avg_times):
        axes[0].text(bar.get_x() + bar.get_width()/2, bar.get_height() + max(avg_times)*0.02,
                     f'{val:.4f} ms', ha='center', va='bottom', fontsize=10, fontweight='bold')
    
    # Grafik 2: Box Plot - Distribusi waktu
    box_data = [perf['iterative_times'], perf['recursive_times']]
    bp = axes[1].boxplot(box_data, tick_labels=methods, patch_artist=True)
    for patch, color in zip(bp['boxes'], colors):
        patch.set_facecolor(color)
        patch.set_alpha(0.7)
    axes[1].set_ylabel('Waktu (ms)', fontsize=11)
    axes[1].set_title('Distribusi Waktu Eksekusi', fontsize=12)
    
    # Grafik 3: Line Plot - Perbandingan per iterasi
    iterations = range(1, len(perf['iterative_times']) + 1)
    axes[2].plot(iterations, perf['iterative_times'], label='Iteratif', color='#2ecc71', linewidth=1.5, alpha=0.8)
    axes[2].plot(iterations, perf['recursive_times'], label='Rekursif', color='#e74c3c', linewidth=1.5, alpha=0.8)
    axes[2].set_xlabel('Iterasi ke-', fontsize=11)
    axes[2].set_ylabel('Waktu (ms)', fontsize=11)
    axes[2].set_title('Waktu Eksekusi per Iterasi', fontsize=12)
    axes[2].legend(loc='upper right')
    axes[2].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('performance_comparison.png', dpi=150, bbox_inches='tight')
    plt.show()
    print("\n→ Grafik disimpan sebagai 'performance_comparison.png'")


def plot_scalability_test(sizes: List[int]):
    """Test skalabilitas dengan berbagai ukuran data"""
    import sys
    
    print("\n" + "=" * 60)
    print("SCALABILITY TEST - Berbagai Ukuran Data")
    print("=" * 60)
    
    iterative_avgs = []
    recursive_avgs = []
    
    # Set recursion limit untuk ukuran data terbesar
    sys.setrecursionlimit(max(sizes) + 500)
    
    for size in sizes:
        print(f"Testing dengan {size:,} transaksi...", end=" ")
        transactions = generate_transactions(size)
        target_id = transactions[-1].id  # Worst case: target di akhir
        
        perf = measure_performance(transactions, target_id, iterations=50)
        iterative_avgs.append(perf['iterative_avg'])
        recursive_avgs.append(perf['recursive_avg'])
        print("Done!")
    
    # Plot scalability
    plt.figure(figsize=(10, 6))
    plt.plot(sizes, iterative_avgs, 'o-', label='Iteratif', color='#2ecc71', linewidth=2, markersize=8)
    plt.plot(sizes, recursive_avgs, 's-', label='Rekursif', color='#e74c3c', linewidth=2, markersize=8)
    plt.xlabel('Jumlah Transaksi', fontsize=12)
    plt.ylabel('Waktu Rata-rata (ms)', fontsize=12)
    plt.title('Scalability Test: Linear Search Iteratif vs Rekursif', fontsize=14, fontweight='bold')
    plt.legend(fontsize=11)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('scalability_test.png', dpi=150, bbox_inches='tight')
    plt.show()
    print("\n→ Grafik disimpan sebagai 'scalability_test.png'")


def main():
    """Fungsi utama program"""
    print("\n" + "=" * 60)
    print("  APLIKASI AUDIT TRANSAKSI KEUANGAN BANK")
    print("  Linear Search: Iteratif vs Rekursif")
    print("=" * 60)
    
    # Konfigurasi
    DATA_SIZE = 1000  # Jumlah transaksi
    TEST_ITERATIONS = 100  # Jumlah iterasi untuk pengukuran performa
    
    # Generate data transaksi
    print(f"\n→ Generating {DATA_SIZE:,} data transaksi...")
    transactions = generate_transactions(DATA_SIZE)
    print(f"→ Data transaksi berhasil di-generate!")
    
    # Tampilkan sample data
    print("\n" + "-" * 60)
    print("SAMPLE DATA TRANSAKSI (5 data pertama):")
    print("-" * 60)
    for i, t in enumerate(transactions[:5]):
        print(f"{i+1}. {t.id} | {t.tanggal} | {t.jenis:6} | Rp {t.nominal:>15,.2f}")
    
    # Input ID transaksi yang dicari
    print("\n" + "-" * 60)
    print("PENCARIAN TRANSAKSI")
    print("-" * 60)
    print(f"Contoh ID yang tersedia: {transactions[0].id}, {transactions[len(transactions)//2].id}, {transactions[-1].id}")
    
    target_id = input("\nMasukkan ID Transaksi yang dicari: ").strip().upper()
    if not target_id:
        target_id = transactions[len(transactions)//2].id
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
    
    # Ukur dan tampilkan performa
    print("\n→ Mengukur performa (100 iterasi)...")
    perf = measure_performance(transactions, target_id, TEST_ITERATIONS)
    display_performance(perf, DATA_SIZE)
    
    # Tampilkan grafik
    print("\n→ Membuat grafik perbandingan...")
    plot_performance(perf, DATA_SIZE)
    
    # Scalability test (opsional)
    run_scalability = input("\nJalankan Scalability Test? (y/n): ").strip().lower()
    if run_scalability == 'y':
        sizes = [100, 500, 1000, 2000, 3000, 5000]
        plot_scalability_test(sizes)
    
    print("\n" + "=" * 60)
    print("  AUDIT SELESAI - Terima kasih!")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
