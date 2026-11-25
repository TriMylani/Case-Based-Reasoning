================================================================================
SISTEM PENDUKUNG KEPUTUSAN PEMILIHAN RESTORAN TERBAIK (FUZZY LOGIC - SUGENO)
Mata Kuliah : Kecerdasan Buatan (S1 Rekayasa Perangkat Lunak)
================================================================================

1. DESKRIPSI PROGRAM
Program ini mengimplementasikan sistem Fuzzy Logic Inference (Metode Sugeno Orde-Nol)
secara manual (tanpa library fuzzy) untuk mengevaluasi 100 data restoran dari file
'restoran.xlsx' berdasarkan Kualitas Servis (1-100) dan Harga (20.000-55.000),
kemudian menghasilkan 5 restoran terbaik ke dalam file 'peringkat.xlsx'.

2. STRUKTUR FOLDER
- main.py           : Source code utama program Fuzzy Logic
- restoran.xlsx     : File dataset masukan (100 data restoran)
- peringkat.xlsx    : File keluaran otomatis berisi 5 restoran terbaik
- Readme.txt        : Panduan penggunaan program

3. PRASYARAT & INSTALASI
- Python versi 3.8 atau lebih baru.
- Library untuk membaca/menulis file Excel (pandas & openpyxl):
  Jalankan perintah berikut di terminal/CMD:
  pip install pandas openpyxl

4. CARA MENJALANKAN PROGRAM
1. Buka terminal / Command Prompt (CMD).
2. Arahkan direktori ke folder tempat file program disimpan.
3. Pastikan file 'restoran.xlsx' berada di folder yang sama dengan 'main.py'.
4. Jalankan perintah:
   python main.py
5. Program akan menampilkan tabel 5 restoran terbaik di terminal dan otomatis
   menyimpan hasilnya ke file 'peringkat.xlsx'.

