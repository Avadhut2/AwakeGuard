import cv2
import os
from dotenv import load_dotenv
from drowsiness_detector import detect_and_alert

load_dotenv()

# Try ESP32-CAM first, fallback to webcam
url = os.getenv("ESP32_CAM_URL")
use_webcam = False

if url and url.startswith("http"):
    print(f"🔗 Trying ESP32-CAM at: {url}")
    cap = cv2.VideoCapture(url)
    if not cap.isOpened():
        print(f"❌ Could not open ESP32-CAM stream at {url}")
        print("🔄 Falling back to webcam...")
        use_webcam = True
        cap = cv2.VideoCapture(0)
else:
    print("📷 Using webcam (no ESP32_CAM_URL set)")
    use_webcam = True
    cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("❌ Could not open any camera")
    exit()

print("✅ Camera opened successfully")
print("Press 'q' to quit")

frame_count = 0
counter = 0
drowsiness_detected = False

while True:
    ret, frame = cap.read()
    if not ret:
        if use_webcam:
            print("⚠️ No frame received from webcam")
        else:
            print("⚠️ No frame received from ESP32-CAM")
        break

    # Call the drowsiness detection function
    counter = detect_and_alert(frame, counter, frame_count)
    
    # Add visual feedback
    if counter > 0:
        drowsiness_detected = True
        cv2.putText(frame, f"DROWSY DETECTED! Counter: {counter}", (10, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
    else:
        drowsiness_detected = False
        cv2.putText(frame, "AWAKE", (10, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    
    # Show frame info
    cv2.putText(frame, f"Frame: {frame_count}", (10, frame.shape[0] - 20), 
               cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    
    frame_count += 1
    
    cv2.imshow("Awake Guard - Drowsiness Monitor", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
print(f"Processed {frame_count} frames")

