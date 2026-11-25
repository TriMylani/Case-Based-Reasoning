import pandas as pd

# ==============================================================================
# 1. FUNGSI KEANGGOTAAN DASAR (TRAPESIUM & SEGITIGA) - TANPA LIBRARY FUZZY
# ==============================================================================
def trapmf(x, a, b, c, d):
    """Menghitung derajat keanggotaan fungsi Trapesium [a, b, c, d]."""
    if x <= a or x >= d:
        if (a == b and x == a) or (c == d and x == d):
            return 1.0
        return 0.0
    elif b <= x <= c:
        return 1.0
    elif a < x < b:
        return (x - a) / (b - a)
    else:  # c < x < d
        return (d - x) / (d - c)

def trimf(x, a, b, c):
    """Menghitung derajat keanggotaan fungsi Segitiga [a, b, c]."""
    if x <= a or x >= c:
        return 0.0
    elif x == b:
        return 1.0
    elif a < x < b:
        return (x - a) / (b - a)
    else:  # b < x < c
        return (c - x) / (c - b)

# ==============================================================================
# 2. TAHAP FUZZIFICATION
# ==============================================================================
def fuzzify_pelayanan(p):
    """Mengubah nilai crisp Pelayanan (1-100) menjadi derajat keanggotaan fuzzy."""
    return {
        'Buruk': trapmf(p, 0, 0, 25, 45),
        'Cukup': trimf(p, 35, 55, 75),
        'Baik': trapmf(p, 65, 95, 100, 100)
    }

def fuzzify_harga(h):
    """Mengubah nilai crisp Harga (20.000-55.000) menjadi derajat keanggotaan fuzzy."""
    return {
        'Murah': trapmf(h, 20000, 20000, 23000, 33000),
        'Sedang': trimf(h, 28000, 37500, 47000),
        'Mahal': trapmf(h, 42000, 50000, 55000, 55000)
    }

# ==============================================================================
# 3. TAHAP INFERENSI (RULE BASE & IMPLIKASI MIN)
# ==============================================================================
RULES = [
    ('Baik', 'Murah', 'Sangat Layak'),
    ('Baik', 'Sedang', 'Layak'),
    ('Baik', 'Mahal', 'Cukup Layak'),
    ('Cukup', 'Murah', 'Layak'),
    ('Cukup', 'Sedang', 'Cukup Layak'),
    ('Cukup', 'Mahal', 'Tidak Layak'),
    ('Buruk', 'Murah', 'Cukup Layak'),
    ('Buruk', 'Sedang', 'Tidak Layak'),
    ('Buruk', 'Mahal', 'Tidak Layak'),
]

def inference(fp, fh):
    """Mengevaluasi 9 aturan fuzzy menggunakan operator AND (min)."""
    hasil_inferensi = []
    for r_pel, r_hrg, r_out in RULES:
        alpha = min(fp[r_pel], fh[r_hrg])  # Firing strength (alpha-predikat)
        hasil_inferensi.append((alpha, r_out))
    return hasil_inferensi

# ==============================================================================
# 4. TAHAP DEFUZZIFICATION (SUGENO WEIGHTED AVERAGE)
# ==============================================================================
OUTPUT_SINGLETON = {
    'Tidak Layak': 25.0,
    'Cukup Layak': 50.0,
    'Layak': 75.0,
    'Sangat Layak': 100.0
}

def defuzzification(hasil_inferensi):
    """Menghitung skor crisp akhir menggunakan metode Weighted Average."""
    pembilang = 0.0
    penyebut = 0.0
    for alpha, label_out in hasil_inferensi:
        z = OUTPUT_SINGLETON[label_out]
        pembilang += alpha * z
        penyebut += alpha
    return pembilang / penyebut if penyebut != 0 else 0.0

# ==============================================================================
# 5. BACA DATA, EKSEKUSI SISTEM FUZZY & SIMPAN OUTPUT
# ==============================================================================
def main():
    # Membaca dataset restoran.xlsx
    df = pd.read_excel('restoran.xlsx')
    hasil_akhir = []

    for _, row in df.iterrows():
        id_restoran = int(row['id Pelanggan'])
        pelayanan = float(row['Pelayanan'])
        harga = float(row['harga'])

        # Proses Fuzzy Logic
        fp = fuzzify_pelayanan(pelayanan)
        fh = fuzzify_harga(harga)
        inf = inference(fp, fh)
        skor = defuzzification(inf)

        hasil_akhir.append({
            'ID Restoran': id_restoran,
            'Kualitas Servis': int(pelayanan),
            'Harga': int(harga),
            'Skor Kelayakan': round(skor, 2)
        })

    # Mengurutkan berdasarkan Skor Kelayakan tertinggi (tie-breaker: Servis tertinggi, Harga termurah)
    df_hasil = pd.DataFrame(hasil_akhir)
    top_5 = df_hasil.sort_values(
        by=['Skor Kelayakan', 'Kualitas Servis', 'Harga'],
        ascending=[False, False, True]
    ).head(5)

    # Menampilkan 5 restoran terbaik di terminal
    print("=== 5 RESTORAN TERBAIK PILIHAN SISTEM FUZZY ===")
    print(top_5.to_string(index=False))

    # Menyimpan output ke file peringkat.xlsx
    top_5.to_excel('peringkat.xlsx', index=False)
    print("\nHasil berhasil disimpan ke file 'peringkat.xlsx'.")

if __name__ == '__main__':
    main()