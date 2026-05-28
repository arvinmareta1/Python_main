# ==============================================================================
# 🌌 TECHNICAL NOTES & DOCUMENTATION: NEBULAHEART 3D (SPACE GESTURE CONTROLLER)
# ==============================================================================
#
# 📝 ALUR EKSEKUSI TERMINAL (CHEAT SHEET):
# ------------------------------------------------------------------------------
# 1. Matikan venv lokal yang aktif saat ini:
#    $ deactivate
#
# 2. Aktifkan lingkungan conda yang sudah lengkap library-nya:
#    $ conda activate space_gesture
#
# 3. Jalankan kodenya:
#    $ python index.py
# ------------------------------------------------------------------------------
#
# 📝 DESKRIPSI PROYEK:
# Sebuah aplikasi interaktif visualisasi 3D real-time yang mengontrol gerakan 
# dan formasi 1.500 partikel kosmis menggunakan kecerdasan buatan (AI) pelacak 
# tangan berbasis visi komputer.
#
# ⚙️ TEKNOLOGI UTAMA (TECH STACK):
# 1. Python 3.11    - Bahasa pemrograman utama (Sangat stabil untuk proyek ini).
# 2. Pygame         - Mengatur jendela aplikasi, frame-rate (60 FPS), dan input keyboard.
# 3. PyOpenGL       - Akses kartu grafis (GPU) untuk render 3D partikel secara real-time.
# 4. MediaPipe      - AI buatan Google untuk mendeteksi 21 titik koordinat kerangka tangan.
# 5. OpenCV (cv2)   - Mengakses webcam, memproses frame video, dan menampilkan monitor kamera.
# 6. NumPy 1.26.4   - Komputasi matriks kilat untuk kalkulasi posisi rumus matematika 3D.
#
# 🎛️ PANDUAN KONTROL GESTUR TANGAN (MAPPED GESTURES):
# ------------------------------------------------------------------------------
# | JARI TANGAN          | MODE | NAMA MODE             | EFEK VISUAL PARTIKEL |
# ------------------------------------------------------------------------------
# | Terbuka Lebar        |  1   | ROTASI ANGCOSMOS      | Partikel biru acak   |
# |                      |      |                       | berputar lambat.     |
# |                      |      |                       |                      |
# | 1 Jari Telunjuk Tegak|  2   | SATURNUS 3D           | Mengumpul jadi bola  |
# | (Jari lain menekuk)  |      |                       | oranye & cincin emas.|
# |                      |      |                       |                      |
# | 2 Jari (Peace Sign)  |  3   | TEKS I LOVE YOU       | Berbaris membentuk   |
# |                      |      |                       | tulisan biru neon.   |
# |                      |      |                       |                      |
# | Kepal/Genggam Tangan |  4   | BENTUK HATI (LOVE)    | Mengalir membentuk   |
# |                      |      |                       | ikon hati pink tajam.|
# ------------------------------------------------------------------------------
#
# 🛠️ CARA SETUP DI KOMPUTER WINDOWS / LINUX BARU:
# 1. Unduh & Instal Miniconda (Versi Python 3.11) serta VS Code.
# 2. Buka Terminal, buat lingkungan virtual baru:
#    $ conda create -n space_gesture python=3.11 -y
# 3. Aktifkan lingkungan baru tersebut:
#    $ conda activate space_gesture
# 4. Instal semua library (Wajib versi numpy 1.26.4 agar tidak crash dengan OpenGL):
#    $ pip install opencv-python mediapipe pygame PyOpenGL numpy==1.26.4
#
# 🍏 CARA SETUP DI MACBOOK APPLE SILICON (M1 / M2 / M3 - ARM64):
# JANGAN menginstal tanpa mengunci versi, karena OpenCV terbaru akan memaksa 
# penggunaan NumPy 2.x yang merusak PyOpenGL, dan MediaPipe versi standar akan 
# mengalami kesalahan pemuatan modul internal (solutions attribute error).
#
# Ikuti urutan instalasi sukses ini langkah demi langkah:
# 1. Buat dan aktifkan environment conda dengan Python 3.11:
#    $ conda create -n space_gesture python=3.11 -y
#    $ conda activate space_gesture
#
# 2. Instal Pygame dan PyOpenGL terlebih dahulu:
#    $ pip install pygame PyOpenGL
#
# 3. Kunci versi NumPy dan OpenCV secara spesifik agar sinkron dan stabil di ARM64:
#    $ pip install numpy==1.26.4 opencv-python==4.8.1.78 --no-cache-dir
#
# 4. Instal MediaPipe versi stabil untuk Apple Silicon yang tidak merusak susunan NumPy:
#    $ pip install mediapipe==0.10.9 --no-cache-dir
#    (Catatan: Jika ada warning merah mengenai opencv-contrib-python di akhir, abaikan saja!)
#
# 🎥 CATATAN INDEKS KAMERA MACBOOK:
# Jendela FaceTime HD Camera bawaan Mac biasanya berada pada indeks 0. Jika program 
# dibuka dan kamera tidak menyala (atau crash thread), pastikan baris kode berikut 
# di file 'index.py' disesuaikan menjadi:
#    cap = cv2.VideoCapture(0)
#
# ==============================================================================

# 1. Penambahan Blok Dokumentasi macOS Apple Silicon: Menjelaskan secara rinci runtutan perintah pip install dengan parameter versi (==) dan --no-cache-dir yang terbukti sukses melewati konflik lingkaran setan antara OpenCV, NumPy, dan MediaPipe.
# 2. Pembersihan Perintah pythonw: Sesuai permintaanmu, panduan menjalankan program di bagian atas kini seragam menggunakan perintah standar python index.py.
# 3. Pemberitahuan Peringatan Merah Pip: Menambahkan catatan kecil agar pengguna Mac tidak panik saat melihat pesan peringatan dari mediapipe di akhir instalasi, karena aplikasinya terbukti tetap berfungsi normal.
# 4. Petunjuk Mengubah Indeks Kamera: Menambahkan instruksi operasional untuk mengubah VideoCapture(2) menjadi VideoCapture(0) karena MacBook umumnya menggunakan indeks 0 untuk kamera FaceTime bawaannya.