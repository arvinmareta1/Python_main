import cv2
import mediapipe as mp
import pyautogui
import numpy as np

# ==========================================
# KONFIGURASI AWAL & SMOOTHING
# ==========================================
# Dapatkan ukuran resolusi layar asli MacBook kamu
SCREEN_WIDTH, SCREEN_HEIGHT = pyautogui.size()

# Resolusi Kamera Webcam
CAM_WIDTH, CAM_HEIGHT = 640, 480

# Faktor peredam getaran (semakin kecil nilainya, semakin mulus tapi sedikit lambat)
SMOOTHNESS = 0.4
prev_x, prev_y = 0, 0
curr_x, curr_y = 0, 0

# Inisialisasi MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

# Inisialisasi Kamera (Indeks 0 untuk FaceTime Camera Mac)
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, CAM_WIDTH)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, CAM_HEIGHT)

# Matikan fitur fail-safe PyAutoGUI agar kursor tidak crash saat menyentuh pojok layar
pyautogui.FAILSAFE = False

print("AI Air Mouse Aktif! Tekan 'q' pada jendela kamera untuk keluar.")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Balik kamera agar searah dengan gerakan tangan kita (efek cermin)
    frame = cv2.flip(frame, 1)
    
    # Konversi warna ke RGB untuk pemrosesan MediaPipe
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Menggambar kerangka tangan di jendela monitor kamera
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Ambil koordinat Ujung Jari Telunjuk (ID 8) dan Ujung Jempol (ID 4)
            thumb = hand_landmarks.landmark[4]
            index_finger = hand_landmarks.landmark[8]
            middle_finger = hand_landmarks.landmark[12]

            # 1. Konversi koordinat normalisasi (0.0 - 1.0) ke skala resolusi layar monitor
            # Kita persempit area deteksi di kamera agar jangkauan tangan tidak perlu terlalu lebar
            margin = 100
            target_x = np.interp(index_finger.x * CAM_WIDTH, (margin, CAM_WIDTH - margin), (0, SCREEN_WIDTH))
            target_y = np.interp(index_finger.y * CAM_HEIGHT, (margin, CAM_HEIGHT - margin), (0, SCREEN_HEIGHT))

            # 2. Terapkan Rumus Smoothing (Linear Interpolation) agar kursor tidak bergetar
            curr_x = prev_x + (target_x - prev_x) * SMOOTHNESS
            curr_y = prev_y + (target_y - prev_y) * SMOOTHNESS

            # Pindahkan kursor mouse sistem operasi
            pyautogui.moveTo(curr_x, curr_y)
            prev_x, prev_y = curr_x, curr_y

            # 3. LOGIKA KLIK (Menghitung Jarak Euclidean Jari)
            # Hitung jarak antara Ujung Jempol dan Ujung Telunjuk
            dist_click = np.hypot(index_finger.x - thumb.x, index_finger.y - thumb.y)
            
            # Hitung jarak antara Ujung Jempol dan Ujung Jari Tengah
            dist_right_click = np.hypot(middle_finger.x - thumb.x, middle_finger.y - thumb.y)

            # Jika Jari Jempol dan Telunjuk berdekatan (Gestur Mencubit) -> KLIK KIRI
            if dist_click < 0.05:
                pyautogui.click()
                cv2.putText(frame, "KLIK KIRI", (5, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)
                pyautogui.sleep(0.1) # Delay singkat agar tidak double-click tidak sengaja

            # Jika Jari Jempol dan Jari Tengah berdekatan -> KLIK KANAN
            elif dist_right_click < 0.05:
                pyautogui.rightClick()
                cv2.putText(frame, "KLIK KANAN", (5, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
                pyautogui.sleep(0.2)

    # Tampilkan monitor kamera untuk melihat posisi tangan kita
    cv2.imshow("AI Air Mouse Monitor", frame)

    # Tekan 'q' untuk keluar dari program
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()