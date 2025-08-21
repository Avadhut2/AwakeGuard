import cv2
from drowsiness_detector import detect_and_alert

# DroidCam URL
url = "http://192.168.168.128:4747/video" 
cap = cv2.VideoCapture(url)

if not cap.isOpened():
    print("❌ Could not open camera stream. Check IP/port.")
    exit()

frame_count = 0
counter = 0

while True:
    ret, frame = cap.read()
    if not ret:
        print("⚠️ No frame received")
        break

    counter = detect_and_alert(frame, counter, frame_count)
    frame_count += 1

    cv2.imshow("Awake Guard - Drowsiness Monitor", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
