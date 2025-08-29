from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
import json, os, sqlite3, datetime

app = Flask(__name__)
app.config["SECRET_KEY"] = "change-me"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

MONASTERIES_PATH = os.path.join(BASE_DIR, "data", "monasteries.json")
EVENTS_PATH = os.path.join(BASE_DIR, "data", "events.json")
ARCHIVES_PATH = os.path.join(BASE_DIR, "data", "archives.json")

# Ensure DB exists
DB_PATH = os.path.join(BASE_DIR, "submissions.db")
def init_db():
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            phone TEXT,
            monastery TEXT,
            visit_date TEXT,
            message TEXT,
            created_at TEXT
        )
    """)
    con.commit()
    con.close()

init_db()

@app.route("/")
def index():
    monasteries = load_json(MONASTERIES_PATH)
    featured = monasteries[:9]
    return render_template("index.html", monasteries=monasteries, featured=featured)

@app.route("/")
def home():
    monasteries = load_json(MONASTERIES_PATH)
    featured = monasteries[:4]  # first 4 as example
    return render_template("index.html", featured=featured)

@app.route("/monasteries")
def monastery_list():
    monasteries = load_json(MONASTERIES_PATH)
    q = request.args.get("q", "").lower().strip()
    district = request.args.get("district", "").lower().strip()
    results = []
    for m in monasteries:
        if q and q not in (m["name"] + " " + m.get("summary","")).lower():
            continue
        if district and district != m.get("district","").lower():
            continue
        results.append(m)
    return render_template("monasteries.html", monasteries=results, q=q, district=district)

@app.route("/monastery/<monastery_id>")
def monastery_detail(monastery_id):
    monasteries = load_json(MONASTERIES_PATH)
    m = next((x for x in monasteries if x["id"] == monastery_id), None)
    if not m:
        return render_template("404.html"), 404
    return render_template("monastery_detail.html", m=m, monasteries=monasteries)

@app.route("/archives")
def archives():
    try:
        archives = load_json(ARCHIVES_PATH)
    except FileNotFoundError:
        archives = []
    return render_template("archives.html", archives=archives)

@app.route("/events")
def events():
    events = load_json(EVENTS_PATH)
    # sort by date if parsable
    def parse_date(d):
        try:
            return datetime.datetime.fromisoformat(d)
        except Exception:
            return datetime.datetime.max
    events_sorted = sorted(events, key=lambda e: parse_date(e.get("date","9999-12-31T00:00:00")))
    return render_template("events.html", events=events_sorted)

@app.route("/submit", methods=["GET", "POST"])
def submit():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        phone = request.form.get("phone")
        monastery = request.form.get("monastery")
        visit_date = request.form.get("visit_date")
        message = request.form.get("message")
        con = sqlite3.connect(DB_PATH)
        cur = con.cursor()
        cur.execute("""INSERT INTO bookings (name,email,phone,monastery,visit_date,message,created_at)
                       VALUES (?,?,?,?,?,?,?)""",
                    (name, email, phone, monastery, visit_date, message, datetime.datetime.utcnow().isoformat()))
        con.commit()
        con.close()
        flash("Thanks! Your submission has been recorded.", "success")
        return redirect(url_for("submit"))
    monasteries = load_json(MONASTERIES_PATH)
    return render_template("submit.html", monasteries=monasteries)

@app.route("/api/monasteries.json")
def api_monasteries():
    return jsonify(load_json(MONASTERIES_PATH))

@app.errorhandler(404)
def not_found(e):
    return render_template("404.html"), 404

if __name__ == "__main__":
    app.run(debug=True)
