from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import os
from db_config import get_db_connection

app = Flask(__name__)
CORS(app)

@app.route("/captures/<path:filename>")
def serve_captures(filename):
    captures_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "captures")
    return send_from_directory(captures_dir, filename)

@app.route("/alerts", methods=["GET"])
def get_alerts():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT alert_id, driver_id, status, location, timestamp, pir_status, image_path FROM alerts ORDER BY timestamp DESC LIMIT 50;")
    rows = cur.fetchall()
    cur.close()
    conn.close()

    alerts = [
        {
            "alert_id": r[0],
            "driver_id": r[1],
            "status": r[2],
            "location": r[3],
            "timestamp": r[4].isoformat(),
            "pir_status": r[5],
            "image_path": r[6]
        }
        for r in rows
    ]
    return jsonify(alerts)

@app.route("/latest_status/<int:driver_id>", methods=["GET"])
def latest_status(driver_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT status, timestamp FROM alerts WHERE driver_id=%s ORDER BY timestamp DESC LIMIT 1;", (driver_id,))
    row = cur.fetchone()
    cur.close()
    conn.close()

    if row:
        return jsonify({"driver_id": driver_id, "status": row[0], "timestamp": row[1].isoformat()})
    else:
        return jsonify({"driver_id": driver_id, "status": "Unknown"}), 404

@app.route("/drivers", methods=["GET"])
def get_drivers():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT driver_id, name, phone, email FROM drivers;")
    rows = cur.fetchall()
    cur.close()
    conn.close()

    drivers = [{"driver_id": r[0], "name": r[1], "phone": r[2], "email": r[3]} for r in rows]
    return jsonify(drivers)

@app.route("/add_alert", methods=["POST"])
def add_alert():
    data = request.json
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO alerts (driver_id, status, location, image_path, pir_status, notified)
        VALUES (%s, %s, %s, %s, %s, %s)
        RETURNING alert_id, timestamp;
    """, (data["driver_id"], data["status"], data.get("location"), data.get("image_path"), data.get("pir_status"), data.get("notified", True)))
    alert_id, ts = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"alert_id": alert_id, "timestamp": ts.isoformat()}), 201

if __name__ == "__main__":
    app.run(debug=True, port=5000)
