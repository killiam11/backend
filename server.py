from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

DB_NAME = "chat.db"

def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sender TEXT NOT NULL,
                text TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')

@app.route('/messages', methods=['GET'])
def get_messages():
    try:
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT sender, text FROM messages ORDER BY id ASC")
            rows = cursor.fetchall()
            messages = [{'sender': row[0], 'text': row[1]} for row in rows]
            return jsonify(messages)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/messages', methods=['POST'])
def post_message():
    data = request.get_json()
    sender = data.get("sender")
    text = data.get("text")
    if not sender or not text:
        return jsonify({"error": "Missing sender or text"}), 400

    try:
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO messages (sender, text) VALUES (?, ?)", (sender, text))
            conn.commit()
        return jsonify({"status": "Message saved"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=10000)
