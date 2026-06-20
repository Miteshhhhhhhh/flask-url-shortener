from flask import Flask, request, render_template, redirect, url_for, g
import sqlite3, string, random
from datetime import datetime

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


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == "POST":
        original_url = request.form["original_url"].strip()

        # Fix 1: https add kar de agar nahi hai
        if not original_url.startswith(('http://', 'https://')):
            original_url = 'https://' + original_url

        short_code = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
        db = get_db()
        db.execute("INSERT INTO urls (original_url, short_code) VALUES (?,?)",
                   (original_url, short_code))
        db.commit()

        # Fix 2: Redirect-after-POST
        return redirect(url_for('home', code=short_code))

    # GET request - naya ya purana code dikhao
    code = request.args.get('code')
    if code:
        db = get_db()
        result = db.execute("SELECT * FROM urls WHERE short_code=?", (code,)).fetchone()
        if result:
            # Fix 3: request.url_root use kar, Render pe safe hai
            full_url = request.url_root.rstrip('/') + '/' + code
            return render_template('home.html',
                                   short_code=code,
                                   full_url=full_url,
                                   clicks=result['clicks'],
                                   created_at=datetime.strptime(result['created_at'], '%Y-%m-%d %H:%M:%S').strftime(
                                       "%d %b %Y, %I:%M %p"))

    return render_template('home.html')


@app.route('/<short_code>')
def redirect_to_url(short_code):
    db = get_db()
    result = db.execute('SELECT original_url FROM urls WHERE short_code =?', (short_code,)).fetchone()
    if result:
        db.execute('UPDATE urls SET clicks = clicks + 1 WHERE short_code =?', (short_code,))
        db.commit()
        return redirect(result['original_url'])
    else:
        return "URL not found", 404

if __name__ == "__main__":
    app.run(debug=False)
