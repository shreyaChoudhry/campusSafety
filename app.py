from flask import Flask, render_template, jsonify, request
import sqlite3

app = Flask(__name__)

print("🔥 SERVER STARTED")  # test print

# 🗄️ Create database
def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            message TEXT,
            lat REAL,
            lng REAL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# 🔥 Dummy data
def add_dummy_data():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    c.execute("SELECT COUNT(*) FROM reports")
    count = c.fetchone()[0]

    if count == 0:
        dummy_reports = [
            ("Harassment near hostel", 29.8545, 77.8885),
            ("Dark area near parking", 29.8538, 77.8875),
            ("Suspicious activity", 29.8550, 77.8890)
        ]

        c.executemany(
            "INSERT INTO reports (message, lat, lng) VALUES (?, ?, ?)",
            dummy_reports
        )

    conn.commit()
    conn.close()

add_dummy_data()

# 🏠 Home
@app.route('/')
def home():
    return render_template('index.html')

# 📢 Report
@app.route('/report')
def report():
    return render_template('report.html')

# 📝 Submit
@app.route('/submit_report', methods=['POST'])
def submit_report():
    data = request.form['message']

    lat = 29.8543
    lng = 77.8880

    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute(
        "INSERT INTO reports (message, lat, lng) VALUES (?, ?, ?)",
        (data, lat, lng)
    )
    conn.commit()
    conn.close()

    return "✅ Report Submitted Successfully!"

# 🗺️ Map
@app.route('/map')
def map_view():
    return render_template('map.html')

# 🚨 SOS
@app.route('/sos', methods=['POST'])
def sos():
    return jsonify({"message": "🚨 SOS Alert Sent!"})

# 📊 Admin
@app.route('/admin')
def admin():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM reports")
    data = c.fetchall()
    conn.close()

    return render_template('admin.html', data=data)

# 📍 Reports API
@app.route('/get_reports')
def get_reports():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT message, lat, lng FROM reports")
    rows = c.fetchall()
    conn.close()

    data = []

    if len(rows) > 3:
        risk = "HIGH 🔴"
    elif len(rows) > 1:
        risk = "MEDIUM 🟡"
    else:
        risk = "LOW 🟢"

    for row in rows:
        data.append({
            "message": row[0],
            "lat": row[1],
            "lng": row[2],
            "risk": risk
        })

    return jsonify(data)

# 🔥 VERY IMPORTANT LINE
if __name__ == '__main__':
    app.run(debug=True)