import cv2
import dlib
import os
import time
import requests
from imutils import face_utils
from scipy.spatial import distance
from alert_handler import enqueue_alert, process_alerts
from telegram_alert import send_telegram_alert
from datetime import datetime

# ================================
# ⚙️ ESP32 Buzzer Trigger
# ================================
def trigger_buzzer():
    try:
        esp32_ip = "http://192.168.168.254/buzz"
        r = requests.get(esp32_ip, timeout=3)
        if r.status_code == 200:
            print("🔔 Buzzer triggered on ESP32")
        else:
            print("⚠️ Failed to trigger buzzer")
    except Exception as e:
        print("❌ Error triggering buzzer:", e)


# ================================
# ⚙️ Dlib Setup
# ================================
detector = dlib.get_frontal_face_detector()

script_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(script_dir, "shape_predictor_68_face_landmarks.dat")
predictor = dlib.shape_predictor(model_path)

(lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
(rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]

# ================================
# ⚙️ Thresholds and Constants
# ================================
EAR_THRESHOLD = 0.23      # Drowsiness threshold
DROWSY_FRAMES = 30        # Frames required to trigger
RESET_FRAMES = 10         # Frames to reduce counter
NO_FACE_RESET_TIME = 3.0  # Reset if no face detected for 3 sec

last_face_time = time.time()
last_alert_time = 0
alert_count = 0
MAX_ALERTS = 3


# ================================
# 🧠 Eye Aspect Ratio
# ================================
def eye_aspect_ratio(eye):
    A = distance.euclidean(eye[1], eye[5])
    B = distance.euclidean(eye[2], eye[4])
    C = distance.euclidean(eye[0], eye[3])
    return (A + B) / (2.0 * C)


# ================================
# 🌍 Cache GPS Location (1-time)
# ================================
try:
    res = requests.get("https://ipinfo.io/json", timeout=3)
    data = res.json()
    CURRENT_LOCATION = data.get("city", "Unknown City") + ", " + data.get("region", "Unknown Region")
except:
    CURRENT_LOCATION = "Unknown Location"


# ================================
# 👁️ Drowsiness Detection Logic
# ================================
def detect_and_alert(frame, counter, frame_count):
    global last_face_time, last_alert_time, alert_count

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    rects = detector(gray, 0)

    # Debug every 30 frames
    if frame_count % 30 == 0:
        print(f"Frame {frame_count}: {len(rects)} face(s) detected")

    if len(rects) == 0:
        if time.time() - last_face_time > NO_FACE_RESET_TIME:
            counter = 0
        return counter

    last_face_time = time.time()

    for rect in rects:
        shape = predictor(gray, rect)
        shape = face_utils.shape_to_np(shape)

        leftEye = shape[lStart:lEnd]
        rightEye = shape[rStart:rEnd]
        leftEAR = eye_aspect_ratio(leftEye)
        rightEAR = eye_aspect_ratio(rightEye)
        ear = (leftEAR + rightEAR) / 2.0

        # Draw eyes
        cv2.drawContours(frame, [cv2.convexHull(leftEye)], -1, (0, 255, 0), 1)
        cv2.drawContours(frame, [cv2.convexHull(rightEye)], -1, (0, 255, 0), 1)
        cv2.putText(frame, f"EAR: {ear:.3f}", (10, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

        # EAR logic
        if ear < EAR_THRESHOLD:
            counter += 1
        else:
            counter = max(0, counter - RESET_FRAMES)

        cv2.putText(frame, f"Counter: {counter}", (10, 90),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

        # 🚨 Trigger only when threshold crossed
        if counter >= DROWSY_FRAMES:
            # Limit alerts
            if alert_count < MAX_ALERTS and time.time() - last_alert_time > 10:
                alert_count += 1
                last_alert_time = time.time()

                print("🚨 DROWSINESS ALERT TRIGGERED!")
                trigger_buzzer()

                # 🕒 Get current time
                time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                location = CURRENT_LOCATION

                # 🛰️ Send Telegram alert
                send_telegram_alert(f"🚨 Drowsiness Detected!\n🕒 Time: {time_now}\n📍 Location: {location}")

                # 💾 Save frame capture
                os.makedirs("captures", exist_ok=True)
                img_path = f"captures/drowsy_{frame_count}.jpg"
                cv2.imwrite(img_path, frame)

                # 📦 Save to database
                alert = {
                    "driver_id": 1,
                    "location": location,
                    "status": "Drowsy",
                    "image_path": img_path
                }
                enqueue_alert(alert)
                process_alerts()

                print("⚠️ Drowsiness detected and alert saved!")

            # Reset counter after alert
            counter = 0

        # 🧾 On-screen status
        if counter >= DROWSY_FRAMES:
            cv2.putText(frame, "⚠️ DROWSY ⚠️", (150, 150),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 3)
        else:
            cv2.putText(frame, "Awake", (150, 150),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

    return counter
