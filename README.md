# 💤 AWAKE GUARD – AI Powered Driver Drowsiness Detection & Smart Alert System  

### 🚗 Real-time Driver Safety Powered by AI, IoT, and Machine Learning  

---

## 📑 Table of Contents

- [📘 Overview](#-overview)
- [🧠 Tech Stack](#-tech-stack)
- [🗂️ Project Structure](#️-project-structure)
- [💾 Shape Predictor](#download-shape_predictor_68_face_landmarksdat)
- [⚙️ Hardware Requirements](#️-hardware-requirements)
- [🧰 Software Requirements](#-software-requirements)
- [🔑 Environment Setup](#-environment-setup)
- [🧠 How It Works](#-how-it-works)
- [⚡ Wiring Diagram](#-wiring-diagram)
- [💻 Flashing ESP32-CAM via TTL to USB](#-flashing-esp32-cam-via-ttl-to-usb)
- [🚀 Running the Project](#-running-the-project)
- [⚡ Troubleshooting](#-troubleshooting)
- [🧑‍💻 Contributors](#%E2%80%8D-contributors)

---

## 📘 Overview  

**Awake Guard** is an advanced **AI + IoT-based driver safety system** designed to detect driver drowsiness in real-time.  
It uses **Computer Vision**, **Dlib facial landmark detection**, and **ESP32 IoT** integration to automatically detect fatigue and prevent accidents.  

When the driver becomes drowsy:
- 🚨 The system **triggers a buzzer** via ESP32  
- 📸 Captures the driver’s photo  
- 📩 Sends an alert with **location + timestamp** to a **Telegram Bot**  
- ☁️ Saves all alert data (time, date, location, image) to **Supabase**  
- 💻 Displays it on a **web dashboard**  

---

## 🧠 Tech Stack  

| Component | Technology |
|------------|-------------|
| Programming Language | Python 3.x |
| AI/ML Libraries | OpenCV, Dlib, Imutils, Scipy |
| Backend | Flask (Python) |
| Database | Supabase |
| IoT Hardware | ESP32 |
| Frontend Dashboard | HTML, CSS, JavaScript |
| APIs Used | Telegram Bot API, Google Geolocation API |
| Environment | Python Virtual Environment (venv) |

---

## 🗂️ Project Structure  

````
AwakeGuard/
│
├── esp32/                                # ESP32-related files
│ └── ESP32 sketch files
├── frontend/                             # Frontend for dashboard/UI
│ └── (HTML, CSS, JS files)
│
├── .env                                  # Git ignore file
│
├── alert_handler.py                      # Handles alert queue & saves alerts
├── api.py                                # API endpoints for communication
├── database_handler.py                   # Database interaction logic
├── db_config.py                          # Database credentials/config
├── drowsiness_detector.py                # Core ML/AI detection logic
├── main.py                               # Main entry point (AI + alert system)
├── main_webcam.py                        # Webcam control and testing
├── telegram_alert.py                     # Sends alerts via Telegram bot
├── shape_predictor_68_face_landmarks.dat # Model for facial landmark detection
│
├── requirements.txt                      # Python dependencies
├── README.md                             # Project documentation
│
└── captures/                             # Captured frames/images during detection
````


---

## Download [shape_predictor_68_face_landmarks.dat](https://drive.google.com/file/d/1MqeJUeNOUvAphKZgIdwkDLevOXj-A-Lp/view?usp=drive_link)

---


## ⚙️ Hardware Requirements  

| Component | Quantity | Description |
|------------|-----------|-------------|
| ESP32 / ESP32-CAM | 1 | IoT microcontroller |
| Buzzer | 1 | Alert signal |
| Webcam | 1 | Drowsiness detection |
| Laptop / PC | 1 | Runs Python scripts |
| Internet | 1 | For APIs and Telegram alerts |

---

## 🧰 Software Requirements  

- Python 3.8+
- Arduino IDE
- Git
- Supabase account
- Telegram Bot (via [BotFather](https://t.me/BotFather))

---

## 🔑 Environment Setup  

### 1️⃣ Clone Repository  

`git clone https://github.com/Avadhut2/AwakeGuard.git`

`cd AwakeGuard`

### 2️⃣ Create and Activate Virtual Environment
````
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
````

### 3️⃣ Install Requirements
```
pip install -r requirements.txt
```

### 4️⃣ Create .env File

Create a .env in the root folder with:
```
ESP32_IP=http://192.168.168.254/buzz
ESP32_CAM_URL=http://YOUR_LOCAL_IP:4747/video
BOT_TOKEN=YOUR_TELEGRAM_BOT_TOKEN
CHAT_ID=YOUR_TELEGRAM_CHAT_ID
PG_HOST=db.yourprojectid.supabase.co
PG_PORT=5432
PG_DB=postgres
PG_USER=postgres
PG_PASSWORD=YOUR_DB_PASSWORD
PG_SSLMODE=require
DATABASE_URL=postgresql://postgres:YOUR_DB_PASSWORD@db.yourprojectid.supabase.co:5432/postgres?sslmode=require
SUPABASE_URL=https://yourprojectid.supabase.co
SUPABASE_KEY=YOUR_SUPABASE_SERVICE_KEY
```


---

## 🧠 How It Works

1. Face Detection & Eye Aspect Ratio (EAR)
   - The system uses Dlib’s facial landmarks to calculate the EAR.
   - If the EAR drops below a threshold for a few consecutive frames, the driver is considered drowsy.

2. Trigger IoT Alert
   - Sends a request to the ESP32 endpoint to activate the buzzer.
  
3. Capture Evidence
   - Captures the driver’s image frame.

4. Send Telegram Alert
   - Sends photo, time, and GPS location to Telegram via bot.

5. Store Alert Data
   - Saves all alert info (time, location, image path) into Supabase.

6. Dashboard Monitoring
   - The dashboard fetches data from Supabase and displays alert logs in real time.

---

## ⚡ Wiring Diagram

Below is the correct wiring for flashing your ESP32-CAM using a **TTL-to-USB module**.

![ESP32-CAM Wiring](https://i0.wp.com/randomnerdtutorials.com/wp-content/uploads/2024/06/ESP32-CAM-FTDI-programmer.png?quality=100&resize=828%2C502&ssl=1&strip=all)


| ESP32-CAM Pin | TTL Module Pin |
|----------------|----------------|
| 5V             | 5V             |
| GND            | GND            |
| U0R (RX)       | TX             |
| U0T (TX)       | RX             |
| IO0 → GND      | Flash Mode     |

> 🔸 *Connect IO0 to GND only while flashing. Remove it after uploading the code.*

---

## 💻 Flashing ESP32-CAM via TTL to USB

1. Connect ESP32-CAM and TTL adapter as per the wiring above.  
2. Hold **IO0 → GND** for flash mode.  
3. Open **Arduino IDE** or **esptool**.
4. Select:
   - **Board:** ESP32 Wrover Module  
   - **Flash Size:** 4MB  
   - **Upload Speed:** 115200  
5. Choose the correct **COM port**.
6. Click **Upload**.  
7. Once done, disconnect **IO0** from **GND** and press the **RST** button.  
8. The ESP32-CAM should start running your code 🎉.

---

## 🚀 Running the Project

1️⃣ Start ESP32

1. Open Arduino IDE
2. Install ESP32 board support (via Preferences → Additional Board Manager URLs)
3. Open esp32/awake_guard.ino
4. Update Wi-Fi credentials:
 ````
const char* ssid = "Your_WiFi_Name";
const char* password = "Your_WiFi_Password";
````
5. Connect ESP32 to your PC and select correct COM port.
6. Click Upload.

---

## 2️⃣ Run Python Detection Script
`python main.py`


## ✅ Output Example:
````
Frame 128: 1 face(s) detected
Drowsiness detected!
🚨 DROWSINESS ALERT TRIGGERED!
📸 Image captured and sent to Telegram!
📍 Location saved to Supabase!
````

---

## 3️⃣ Run Dashboard

1. Navigate to /dashboard
2. Open login.html in a browser
3. Login using your Supabase credentials
4. View all alerts with time, date, location, and driver photo

Tip: Host Website on https://www.netlify.com

---

## ⚡ Troubleshooting

| Issue                        | Solution                                            |
| ---------------------------- | --------------------------------------------------- |
| ESP32 not connecting         | Check COM port and baud rate                        |
| Dlib install error           | Use prebuilt wheels: `pip install cmake dlib`       |
| Telegram not receiving alert | Verify bot token and chat ID                        |
| No image captured            | Ensure webcam is accessible (`cv2.VideoCapture(0)`) |
| Supabase error               | Check URL & API key in `.env`                       |

---

## 🧑‍💻 Contributors

| Name                | Role                                         |
| ------------------- | -------------------------------------------- |
| [**Avadhut Satpute**](https://github.com/Avadhut2) |IOT, Backend, Database, Testing|
| [**Komal Sabarad**](https://github.com/KomalSabarad) |Frontend, Dashboard, API's|
| [**Swayam Patil**](https://github.com/swayampatil7) |Frontend, Dashboard, API's|
| [**Rajvardhan Varpe**](https://github.com/Rajvardhanvarpe) |Telegram Integration|

⭐ If you find this project useful, please star this repository to support future development!
```
