import cv2
import mediapipe as mp
import numpy as np

# ==========================================
# KONFIGURASI AWAL & WARNA
# ==========================================
# Warna kuas dalam format BGR (Blue, Green, Red)
colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (0, 255, 255)] # Biru, Hijau, Merah, Kuning
color_index = 0

# Membuat kanvas kosong berwarna putih untuk tempat menggambar
canvas = None

# Inisialisasi MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.8, min_tracking_confidence=0.8)
mp_draw = mp.solutions.drawing_utils

# Inisialisasi Kamera MacBook (Indeks 0 untuk FaceTime Camera)
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

# Koordinat titik gambar sebelumnya
prev_x, prev_y = 0, 0

print("Aplikasi Virtual Paint Siap! Tekan 'q' pada keyboard untuk keluar.")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Balik frame agar seperti cermin (membantu navigasi tangan)
    frame = cv2.flip(frame, 1)
    h, w, c = frame.shape

    # Inisialisasi kanvas di frame pertama
    if canvas is None:
        canvas = np.zeros_like(frame)

    # Gambar menu pilihan warna di bagian atas layar
    cv2.rectangle(frame, (30, 10), (140, 70), (255, 0, 0), -1)    # Kotak Biru
    cv2.rectangle(frame, (170, 10), (280, 70), (0, 255, 0), -1)   # Kotak Hijau
    cv2.rectangle(frame, (310, 10), (420, 70), (0, 0, 255), -1)   # Kotak Merah
    cv2.rectangle(frame, (450, 10), (560, 70), (0, 255, 255), -1) # Kotak Kuning
    cv2.rectangle(frame, (590, 10), (700, 70), (200, 200, 200), -1) # Kotak CLEAR
    
    cv2.putText(frame, "CLEAR", (615, 45), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2, cv2.LINE_AA)

    # Proses deteksi tangan
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Ambil koordinat Ujung Jari Telunjuk (ID 8) dan Jari Tengah (ID 12)
            idx_p = hand_landmarks.landmark[8]
            mid_p = hand_landmarks.landmark[12]
            
            cx, cy = int(idx_p.x * w), int(idx_p.y * h)
            mx, my = int(mid_p.x * w), int(mid_p.y * h)

            # Cek apakah Jari Tengah juga tegak berdiri (Mode Memilih / Angkat Kuas)
            # Jika jarak y ujung jari tengah di bawah pip/sendinya, artinya jari tengah ditekuk
            pip_mid = hand_landmarks.landmark[10]
            jari_tengah_berdiri = mid_p.y < pip_mid.y

            # MODE 1: GESTUR MEMILIH (Jari Telunjuk & Jari Tengah Sama-sama Tegak)
            if jari_tengah_berdiri:
                prev_x, prev_y = 0, 0 # Reset titik gambar agar tidak membuat garis lompat
                cv2.circle(frame, (cx, cy), 15, (255, 255, 255), cv2.FILLED)
                
                # Cek jika ujung jari menyentuh area tombol menu di atas
                if cy <= 70:
                    if 30 <= cx <= 140:
                        color_index = 0 # Biru
                    elif 170 <= cx <= 280:
                        color_index = 1 # Hijau
                    elif 310 <= cx <= 420:
                        color_index = 2 # Merah
                    elif 450 <= cx <= 560:
                        color_index = 3 # Kuning
                    elif 590 <= cx <= 700:
                        canvas = np.zeros_like(frame) # Clear total gambaran
            
            # MODE 2: GESTUR MENGGAMBAR (Hanya Jari Telunjuk yang Tegak)
            else:
                cv2.circle(frame, (cx, cy), 10, colors[color_index], cv2.FILLED)
                
                if prev_x == 0 and prev_y == 0:
                    prev_x, prev_y = cx, cy

                # Gambar garis tebal di kanvas
                cv2.line(canvas, (prev_x, prev_y), (cx, cy), colors[color_index], 8)
                prev_x, prev_y = cx, cy

    # Gabungkan frame kamera asli dengan coretan kanvas digital
    gray_canvas = cv2.cvtColor(canvas, cv2.COLOR_BGR2GRAY)
    _, inverse_canvas = cv2.threshold(gray_canvas, 20, 255, cv2.THRESH_BINARY_INV)
    inverse_canvas = cv2.cvtColor(inverse_canvas, cv2.COLOR_GRAY2BGR)
    
    frame = cv2.bitwise_and(frame, inverse_canvas)
    frame = cv2.bitwise_or(frame, canvas)

    # Tampilkan jendela aplikasi
    cv2.imshow("Virtual Air Canvas Paint", frame)

    # Tekan 'q' untuk menutup aplikasi
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()