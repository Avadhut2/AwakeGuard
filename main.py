import cv2
import os
from dotenv import load_dotenv
from drowsiness_detector import detect_and_alert


load_dotenv()

url = os.getenv("ESP32_CAM_URL")

if not url:
    print("❌ ESP32_CAM_URL not set in .env file")
    exit()

cap = cv2.VideoCapture(url)

if not cap.isOpened():
    print(f"❌ Could not open ESP32-CAM stream at {url}")
    exit()

frame_count = 0
counter = 0

while True:
    ret, frame = cap.read()
    if not ret:
        print("⚠️ No frame received from ESP32-CAM")
        break

    counter = detect_and_alert(frame, counter, frame_count)
    frame_count += 1

    
    cv2.imshow("Awake Guard - ESP32-CAM Drowsiness Monitor", frame)

   
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
