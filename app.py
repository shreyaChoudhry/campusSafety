from flask import Flask, render_template, jsonify, request
import sqlite3
import random

app = Flask(__name__)

# 🗄️ DB INIT
def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    c.execute('''
        CREATE TABLE IF NOT EXISTS reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            message TEXT,
            category TEXT,
            lat REAL,
            lng REAL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    conn.commit()
    conn.close()

init_db()

# 🏠 HOME
@app.route('/')
def home():
    return render_template('index.html')

# 📢 REPORT PAGE
@app.route('/report')
def report():
    return render_template('report.html')

# 📝 SUBMIT REPORT
@app.route('/submit_report', methods=['POST'])
def submit_report():
    message = request.form['message']
    category = request.form['category']
    location = request.form['location']

    # 🎓 UNIVERSITY MAPPING (PRIMARY FOCUS)
    university_coords = {
        "COER University": (29.8543, 77.8880),
        "IIT Roorkee": (29.8668, 77.8960),
        "Delhi University": (28.6863, 77.2218),
        "JNU": (28.5383, 77.1667),
        "IIT Bombay": (19.1334, 72.9133),
        "Pune University": (18.5523, 73.8243),
        "IISc Bangalore": (13.0213, 77.5670),
        "Christ University": (12.9345, 77.6050),
        "University of Rajasthan": (26.9115, 75.7873),
        "MNIT Jaipur": (26.8639, 75.8103)
    }

    # 🧠 LOCATION LOGIC
    if location in university_coords:
        lat, lng = university_coords[location]
    else:
        # 🌍 CITY MODE (SMART DISTRIBUTION)
        random.seed(location)
        lat = 20 + random.uniform(-10, 10)
        lng = 75 + random.uniform(-10, 10)

    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    c.execute(
        "INSERT INTO reports (message, category, lat, lng) VALUES (?, ?, ?, ?)",
        (message, category, lat, lng)
    )

    conn.commit()
    conn.close()

    return "✅ Report Submitted Successfully!"

# 📊 ADMIN DASHBOARD
@app.route('/admin')
def admin():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    c.execute("SELECT id, message, category, lat, lng, timestamp FROM reports")
    data = c.fetchall()

    # 🔥 INSIGHTS
    c.execute("SELECT COUNT(*) FROM reports")
    total = c.fetchone()[0]

    c.execute("""
        SELECT category, COUNT(*) as count 
        FROM reports 
        GROUP BY category 
        ORDER BY count DESC 
        LIMIT 1
    """)
    top_category = c.fetchone()

    conn.close()

    return render_template(
        'admin.html',
        data=data,
        total=total,
        top_category=top_category
    )

# ❌ DELETE / RESOLVE
@app.route('/delete/<int:id>')
def delete(id):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("DELETE FROM reports WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return "Deleted"

# 🗺️ MAP
@app.route('/map')
def map_view():
    return render_template('map.html')

# 📍 API
@app.route('/get_reports')
def get_reports():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    c.execute("SELECT message, category, lat, lng FROM reports")
    rows = c.fetchall()
    conn.close()

    data = []

    for row in rows:
        category = row[1]

        # 🎨 COLOR LOGIC
        color = "green"

        if category == "Harassment":
            color = "red"
        elif category == "Theft":
            color = "orange"
        elif category == "Lighting Issue":
            color = "yellow"

        data.append({
            "message": row[0],
            "category": category,
            "lat": row[2],
            "lng": row[3],
            "color": color
        })

    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
