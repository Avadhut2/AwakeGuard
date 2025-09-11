# Awake Guard – Driver Drowsiness Detection System

Awake Guard is an IoT-based driver monitoring system that detects drowsiness using an ESP32-CAM video feed, triggers a buzzer alarm via a separate ESP32 board, and logs alerts into a Supabase PostgreSQL database. The system includes a Flask backend API and a dark-theme web dashboard to visualize driver status and alerts.
---


---

## ⚙️ Requirements
- Python 3.8+
- OpenCV
- dlib
- numpy
- sqlite3 / MySQL (for database)
- requests (for API integration)


# Contributors

[Avadhut Satpute](https://github.com/Avadhut2) – Project Lead, Backend, Database & API Integration,  ESP32-CAM & Hardware Integration

[Rajvardhan Varpe](https://github.com/Rajvardhanvarpe) – Whatsapp and Telegram Alert Integration

[Komal Sabarad](https://github.com/KomalSabarad) – Frontend & Dashboard

[Swayam Patil](https://github.com/swayampatil7)  – Frontend & Dashboard


## What we did until now

We successfully migrated our database from PostgreSQL to Supabase, leveraging its cloud-native capabilities for scalability and seamless integration. The backend development is nearly complete, with all major APIs and core functionalities implemented and tested. On the hardware side, we have partially completed the ESP32-CAM integration, enabling initial data capture and communication with the backend. Further refinements are planned to fully optimize the hardware interaction.



## What is remaining 

We are currently working on developing the frontend with user authentication, further refining the hardware integration, and improving backend performance to ensure a seamless end-to-end experience.
