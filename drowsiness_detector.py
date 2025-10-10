import cv2
import dlib
import os
import time
import requests
from imutils import face_utils
from scipy.spatial import distance
from alert_handler import enqueue_alert, process_alerts

# =========================
#  ESP32 and Dlib setup
# =========================
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

detector = dlib.get_frontal_face_detector()

# Path for landmark model
script_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(script_dir, "shape_predictor_68_face_landmarks.dat")
predictor = dlib.shape_predictor(model_path)

(lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
(rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]

# =========================
#  Detection Parameters
# =========================
EAR_THRESHOLD = 0.23       # slightly lower threshold to reduce false alarms
DROWSY_FRAMES = 30         # must stay below threshold for these many frames
RESET_FRAMES = 10          # frames needed to reset if eyes open again
NO_FACE_RESET_TIME = 3.0   # seconds after losing face to reset

last_face_time = time.time()


# =========================
#  EAR Calculation
# =========================
def eye_aspect_ratio(eye):
    A = distance.euclidean(eye[1], eye[5])
    B = distance.euclidean(eye[2], eye[4])
    C = distance.euclidean(eye[0], eye[3])
    return (A + B) / (2.0 * C)


# =========================
#  Detection Logic
# =========================
def detect_and_alert(frame, counter, frame_count):
    global last_face_time

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    rects = detector(gray, 0)

    # Debug: print detection status occasionally
    if frame_count % 30 == 0:
        print(f"Frame {frame_count}: {len(rects)} face(s) detected")

    if len(rects) == 0:
        # If face missing for > few seconds, reset counter
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

        # Draw contours and EAR
        cv2.drawContours(frame, [cv2.convexHull(leftEye)], -1, (0, 255, 0), 1)
        cv2.drawContours(frame, [cv2.convexHull(rightEye)], -1, (0, 255, 0), 1)
        cv2.putText(frame, f"EAR: {ear:.3f}", (10, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

        # EAR-based logic
        if ear < EAR_THRESHOLD:
            counter += 1
        else:
            # Slowly recover counter if eyes reopen
            if counter > 0:
                counter = max(0, counter - RESET_FRAMES)

        # Display current counter
        cv2.putText(frame, f"Counter: {counter}", (10, 90),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

        # Drowsiness trigger condition
        if counter >= DROWSY_FRAMES:
            print("🚨 DROWSINESS ALERT TRIGGERED!")
            trigger_buzzer()

            # Save capture
            os.makedirs("captures", exist_ok=True)
            img_path = f"captures/drowsy_{frame_count}.jpg"
            cv2.imwrite(img_path, frame)

            # Enqueue alert
            alert = {
                "driver_id": 1,
                "location": "16.704N,74.243E",
                "status": "Drowsy",
                "image_path": img_path
            }
            enqueue_alert(alert)
            process_alerts()
            print("⚠️ Drowsiness detected and alert saved!")

            counter = 0  # reset after alert

        # Display text feedback
        if counter >= DROWSY_FRAMES:
            cv2.putText(frame, "⚠️ DROWSY ⚠️", (150, 150),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 3)
        else:
            cv2.putText(frame, "Awake", (150, 150),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

    return counter
