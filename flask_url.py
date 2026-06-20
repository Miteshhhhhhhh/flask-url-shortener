import sqlite3
from datetime import datetime
from flask import Flask, g, request, render_template, redirect
import string
import random

app = Flask(__name__)

def get_db():
    if "db" not in g:
        g.db = sqlite3.connect("shortener.db")
        g.db.row_factory = sqlite3.Row
    return g.db

@app.teardown_appcontext
def close_db(error):
    db = g.pop("db", None)
    if db is not None:
        db.close()

def init_db():
    db = get_db()
    db.execute("""
    CREATE TABLE IF NOT EXISTS urls
    (id INTEGER PRIMARY KEY AUTOINCREMENT,
    original_url TEXT NOT NULL,
    short_code TEXT NOT NULL UNIQUE,
     clicks INTEGER DEFAULT 0,
     TIMESTAMP DEFAULT CURRENT_TIMESTAMP)
    """)
    db.commit()

with app.app_context():
    init_db()

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        original_url = request.form["original_url"]
        short_code = "".join(random.choices(string.ascii_letters + string.digits, k=6))
        db = get_db()
        db.execute("INSERT INTO urls (original_url, short_code) VALUES (?,?)", (original_url, short_code))
        db.commit()
        return render_template("home.html",
                               short_code=short_code,
                               full_url=request.host_url + short_code,
                               clicks=0,
                               created_at=datetime.now().strftime("%d %b %Y,%I %M %p"))
    return render_template("home.html")

@app.route("/<short_code>")
def redirect_to_url(short_code):
    db = get_db()
    result = db.execute("SELECT original_url FROM urls WHERE short_code =?", (short_code,)).fetchone()

    if result:
        db.execute("UPDATE urls SET clicks = clicks + 1 WHERE short_code =?", (short_code,))
        db.commit()

        return redirect(result["original_url"])
    else:
        return "URL not found", 404

if __name__ == "__main__":
    app.run(debug=True)
