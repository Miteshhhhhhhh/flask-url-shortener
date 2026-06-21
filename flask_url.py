from flask import Flask, request, render_template, redirect, g, url_for
import sqlite3, string, random
from datetime import datetime

app = Flask(__name__)

def init_db():
    with sqlite3.connect('shortener.db') as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS urls (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                original_url TEXT NOT NULL,
                short_code TEXT UNIQUE NOT NULL,
                clicks INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)
        ''')
init_db()

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
    if request.method == 'POST':
        original_url = request.form['original_url']
        db = get_db()
        existing = db.execute("SELECT * FROM urls WHERE original_url=?", (original_url,)).fetchone()

        if existing:
            short_code = existing['short_code']
            result = existing
        else:
            short_code = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
            db.execute("INSERT INTO urls (original_url, short_code) VALUES (?,?)",
                       (original_url, short_code))
            db.commit()
            result = db.execute("SELECT * FROM urls WHERE short_code=?", (short_code,)).fetchone()


    
        result = db.execute("SELECT * FROM urls WHERE short_code=?", (short_code,)).fetchone()

        full_url = request.host_url + short_code
        created_time = result['created_at'].split('.')[0]
        formatted_date = datetime.strptime(created_time, '%Y-%m-%d %H:%M:%S').strftime('%d %B %Y')

        return render_template('home.html',
                               short_code=short_code,
                               original_url=original_url,
                               full_url=full_url,
                               clicks=result['clicks'],
                               created_at=formatted_date)
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

@app.route('/delete/<short_code>', methods=['POST'])
def delete_url(short_code):
    db = get_db()
    db.execute("DELETE FROM urls WHERE short_code=?", (short_code,))
    db.commit()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=False)




