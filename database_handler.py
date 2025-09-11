from db_config import get_db_connection

def insert_alert(alert):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO alerts (driver_id, location, status, image_path)
            VALUES (%s, %s, %s, %s)
        """, (alert["driver_id"], alert["location"], alert["status"], alert["image_path"]))
        conn.commit()
        cur.close()
        conn.close()
        print("✅ Alert saved to DB:", alert)
    except Exception as e:
        print("❌ Database Error:", e)
