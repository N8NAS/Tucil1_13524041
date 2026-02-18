# Solver Permainan Queens LinkedIn
Tugas Kecil 1 IF2211 Strategi Algoritma - Penyelesaian Permainan Queens dengan Algoritma Brute Force.

## Penjelasan Singkat
Program ini dirancang untuk mencari solusi dari permainan Queens yang tersedia pada platform LinkedIn. Aturan utama permainan ini adalah menempatkan tepat satu Queen pada setiap baris, kolom, dan wilayah warna yang tersedia, dengan syarat tidak ada dua Queen yang bersentuhan baik secara horizontal, vertikal, maupun diagonal.

Algoritma yang digunakan adalah Brute Force dengan pendekatan backtracking. Program akan mencoba menempatkan Queen baris demi baris dan melakukan pemeriksaan validitas terhadap posisi Queen yang sudah ada sebelumnya. Jika ditemukan kondisi yang melanggar aturan, program akan melakukan backtracking untuk mencoba kemungkinan posisi lain sehingga solusi valid dapat ditemukan atau seluruh kemungkinan habis.



## Requirement Program dan Instalasi
Program ini dikembangkan menggunakan bahasa pemrograman Python 3, beserta beberapa library lainnya.
Prasyarat program:
- Python versi 3
- Pip (Python Package Manager)
- opencv-python
- pillow
- numpy

Instalasi library opencv, pillow, dan numpy dapat dilakukan di terminal dan mengetik

pip install opencv-python pillow numpy

## Cara menjalankan program
1. Pastikan terminal Anda berada di folder Tucil1_13524041/src
2. Ketik di terminal python tucil1.py
3. Pilih metode untuk memasukan papan(Ketik langsung, file text, atau file gambar)
4. Masukan besar papan yang diinginkan
5. Jika pilih opsi masukan manual, ketiklah papan pada terminal.
6. Jika file text atau file gambar, ketikan path untuk file tersebut
7. Program akan berjalan dan menampilkan hasil akhir pencarian, waktu eksekusi, dan jumlah kasus yang ditinjau. Jika papan sama, maka tidak ada solusi untuk papan kamu
8. Program akan menanyakan apakah hasil ingin disave.
9. Jika iya, program akan menanyakan apakah hasil ingin disimpankan dalam bentuk gambar.
10. Hasil akan tersimpan di folder yang sama saat run

## Identitas
- Nama : Nathan Adhika Santosa
- Kelas : K1
- NIM : 13524041


## Catatan
- Pertunjukan algoritma hanya dilakukan setiap 1000 iterasi, yaitu ketika queen sedang ditaruhkan, baik benar atau salah