
from flask import Flask, request, jsonify
import sqlite3
import datetime
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Initialize DB#
def init_db():
    conn = sqlite3.connect("learner_logs.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            action TEXT,
            score INTEGER,
            content_type TEXT,
            time_spent INTEGER,
            topic TEXT,
            level TEXT,
            timestamp TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.route("/log", methods=["POST"])
def log_action():
    data = request.get_json()
    conn = sqlite3.connect("learner_logs.db")
    cursor = conn.cursor()
    timestamp = datetime.datetime.utcnow().isoformat()

    cursor.execute('''
        INSERT INTO logs (user_id, action, score, content_type, time_spent, topic, level, timestamp)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        data.get("user_id"),
        data.get("action"),
        data.get("score"),
        data.get("content_type"),
        data.get("time_spent"),
        data.get("topic"),
        data.get("level"),
        timestamp
    ))
    conn.commit()
    conn.close()

    return jsonify({"status": "success", "logged": {"timestamp": timestamp}})

@app.route("/history", methods=["GET"])
def get_history():
    user_id = request.args.get("user_id")
    if not user_id:
        return jsonify({"error": "Missing user_id"}), 400

    conn = sqlite3.connect("learner_logs.db")
    cursor = conn.cursor()
    cursor.execute("SELECT timestamp, topic, score, level, content_type, time_spent FROM logs WHERE user_id = ? ORDER BY timestamp DESC", (user_id,))
    rows = cursor.fetchall()
    conn.close()

    history = [
        {
            "timestamp": row[0],
            "topic": row[1],
            "score": row[2],
            "level": row[3],
            "content_type": row[4],
            "time_spent": row[5],
        }
        for row in rows
    ]
    return jsonify({"history": history})

@app.route("/", methods=["GET"])
def index():
    return {"message": "Learner Data Tracker is running"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8001)
