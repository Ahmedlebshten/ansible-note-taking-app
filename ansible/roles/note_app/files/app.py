from flask import Flask, request, render_template_string
import sqlite3
from datetime import datetime
import os

app = Flask(__name__)
DB_FILE = "/home/ec2-user/notes.db"

# Initialize the database if not exists
def init_db():
    if not os.path.exists(DB_FILE):
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute("""
            CREATE TABLE IF NOT EXISTS notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content TEXT NOT NULL,
                timestamp TEXT NOT NULL
            )
        """)
        conn.commit()
        conn.close()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        note = request.form["note"]
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute("INSERT INTO notes (content, timestamp) VALUES (?, ?)", (note, timestamp))
        conn.commit()
        conn.close()

    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT content, timestamp FROM notes ORDER BY id DESC")
    notes = c.fetchall()
    conn.close()

    return render_template_string('''
        <h1>Note Taking App</h1>
        <form method="POST">
            <textarea name="note" rows="4" cols="50" placeholder="Write your note here..."></textarea><br><br>
            <button type="submit">Save Note</button>
        </form>
        <h2>Notes:</h2>
        {% for note, ts in notes %}
            <p>🕒 {{ ts }}<br>📌 {{ note }}</p>
        {% endfor %}
    ''', notes=notes)

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000)
