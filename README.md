# Awake Guard – Driver Drowsiness Detection System

Awake Guard is an IoT-based driver monitoring system that detects drowsiness using an ESP32-CAM video feed, triggers a buzzer alarm via a separate ESP32 board, and logs alerts into a Supabase PostgreSQL database. The system includes a Flask backend API and a lightweight web dashboard to visualize driver status and alerts.
---


---

## ⚙️ Requirements
- Python 3.8+
- OpenCV
- dlib
- numpy
- sqlite3 / MySQL (for database)
- requests (for API integration)
 - Flask, Flask-CORS (for web API and frontend access)


# Contributors

Avadhut Satpute – Project Lead, Backend, Database & API Integration,  ESP32-CAM & Hardware Integration

Rajvardhan Varpe – Whatsapp and Telegram Alert Integration

Komal Sabarad – Frontend & Dashboard

Swayam Patil  – Frontend & Dashboard


## What we did until now

We successfully migrated our database from PostgreSQL to Supabase, leveraging its cloud-native capabilities for scalability and seamless integration. The backend development is nearly complete, with all major APIs and core functionalities implemented and tested. On the hardware side, we have partially completed the ESP32-CAM integration, enabling initial data capture and communication with the backend. Further refinements are planned to fully optimize the hardware interaction.



## What is remaining 

We are currently working on developing the frontend dashboard (drivers, latest status, and recent alerts), further refining the hardware integration, and improving backend performance to ensure a seamless end-to-end experience.

## 🌐 Frontend (Dashboard)

After starting the Flask API (defaults to `http://localhost:5000`), open `frontend/index.html` with a static server (e.g., VS Code Live Server or `python -m http.server` from the `frontend/` folder). The dashboard fetches from:

- `GET /drivers`
- `GET /latest_status/<driver_id>`
- `GET /alerts`
- Captured images served from `GET /captures/<filename>`

### Supabase Authentication

The dashboard uses Supabase email/password auth (via CDN). Provide your Supabase URL and anon key when prompted on first load, or pre-store them in localStorage:

```js
localStorage.setItem('AG_SB_URL', 'https://YOUR-PROJECT.supabase.co');
localStorage.setItem('AG_SB_ANON', 'YOUR_ANON_KEY');
```

- Create users in Supabase Auth. Add `role` in user metadata as either `driver` or `admin` (family).
- After login, users are redirected to the dashboard. Role controls UI visibility (filters hidden for `driver`).

### Notes

- Set the API base URL from the login card if your Flask API runs elsewhere.
- Google Map uses an embedded public maps query; no key needed. For production-grade maps, replace the iframe with Google Maps JS SDK.
