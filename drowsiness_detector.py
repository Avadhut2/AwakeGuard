import cv2
import dlib
import os
import requests
from imutils import face_utils
from scipy.spatial import distance
from alert_handler import enqueue_alert, process_alerts

def trigger_buzzer():
    try:
        esp32_ip = "http://192.168.168.254/buzz"  # Replace with your ESP32 IP
        r = requests.get(esp32_ip, timeout=3)
        if r.status_code == 200:
            print("🔔 Buzzer triggered on ESP32")
        else:
            print("⚠️ Failed to trigger buzzer")
    except Exception as e:
        print("❌ Error triggering buzzer:", e)

detector = dlib.get_frontal_face_detector()

# Dynamic path for predictor
script_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(script_dir, "shape_predictor_68_face_landmarks.dat")
predictor = dlib.shape_predictor(model_path)

(lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
(rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]

EAR_THRESHOLD = 0.25
FRAME_CHECK = 60

def eye_aspect_ratio(eye):
    A = distance.euclidean(eye[1], eye[5])
    B = distance.euclidean(eye[2], eye[4])
    C = distance.euclidean(eye[0], eye[3])
    return (A + B) / (2.0 * C)

def detect_and_alert(frame, counter, frame_count):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    rects = detector(gray, 0)

    for rect in rects:
        shape = predictor(gray, rect)
        shape = face_utils.shape_to_np(shape)

        leftEye = shape[lStart:lEnd]
        rightEye = shape[rStart:rEnd]
        leftEAR = eye_aspect_ratio(leftEye)
        rightEAR = eye_aspect_ratio(rightEye)
        ear = (leftEAR + rightEAR) / 2.0

        cv2.drawContours(frame, [cv2.convexHull(leftEye)], -1, (0, 255, 0), 1)
        cv2.drawContours(frame, [cv2.convexHull(rightEye)], -1, (0, 255, 0), 1)

        if ear < EAR_THRESHOLD:
            counter += 1
            if counter >= FRAME_CHECK:
                trigger_buzzer()
                os.makedirs("captures", exist_ok=True)
                img_path = f"captures/drowsy_{frame_count}.jpg"
                cv2.imwrite(img_path, frame)
                alert = {
                    "driver_id": 1,
                    "location": "16.704N,74.243E",
                    "status": "Drowsy",
                    "image_path": img_path
                }
                enqueue_alert(alert)
                process_alerts()
                print("⚠️ Drowsiness detected and alert saved!")
        else:
            counter = 0

    return counter
