from flask import Flask, request, render_template, session, redirect, url_for
from google.cloud import bigquery
import os
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

# יצירת מופע Flask
app = Flask(__name__, template_folder="templates")
app.secret_key = "your_secret_key"

# חיבור ל-BigQuery
secrets_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS", "/etc/secrets/telephones-449210-ea0631866678.json")
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = secrets_path
client = bigquery.Client()

# יצירת חיבור למסד נתונים SQLite
DATABASE = 'users.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

# מסך הבית (מוגן בסיסמה)
@app.route('/')
def home():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('index.html')

# דף הרשמה
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        hashed_password = generate_password_hash(password)
        
        db = get_db()
        try:
            db.execute("INSERT INTO users (email, password, approved) VALUES (?, ?, ?)", (email, hashed_password, False))
            db.commit()
        except sqlite3.IntegrityError:
            return "האימייל כבר קיים במערכת."
        db.close()
        
        return "נרשמת בהצלחה, המתן לאישור המנהל."
    
    return render_template('register.html')

# דף התחברות
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        db = get_db()
        user = db.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
        db.close()
        
        if user and check_password_hash(user['password'], password):
            if user['approved']:
                session['user'] = email
                return redirect(url_for('home'))
            else:
                return "החשבון שלך ממתין לאישור המנהל."
        
        return "פרטי ההתחברות שגויים."
    
    return render_template('login.html')

# דף ניתוק משתמש
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

# ממשק מנהל לאישור משתמשים
@app.route('/admin')
def admin_panel():
    db = get_db()
    users = db.execute("SELECT * FROM users WHERE approved = FALSE").fetchall()
    db.close()
    return render_template('admin.html', users=users)

@app.route('/approve/<email>')
def approve_user(email):
    db = get_db()
    db.execute("UPDATE users SET approved = TRUE WHERE email = ?", (email,))
    db.commit()
    db.close()
    return redirect(url_for('admin_panel'))

# נתיב חיפוש בבסיס הנתונים
@app.route('/search', methods=['GET'])
def search():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    query = request.args.get('query', '').strip()
    search_type = request.args.get('search_type', 'free')

    if not query:
        return render_template('results.html', results=[], query=query, search_type=search_type)

    words = query.split()
    if search_type == "name":
        conditions = " AND ".join([f"name LIKE '%{word}%'" for word in words])
    elif search_type == "title":
        conditions = " AND ".join([f"title LIKE '%{word}%'" for word in words])
    else:
        conditions = " AND ".join([f"(name LIKE '%{word}%' OR title LIKE '%{word}%')" for word in words])

    sql = f"SELECT name, title, phone FROM telephones-449210.ALLPHONES.phones_fixed WHERE {conditions}"

    try:
        results = client.query(sql).result()
        data = [row for row in results]
    except Exception as e:
        return f"שגיאה בביצוע השאילתה: {e}", 500

    return render_template('results.html', results=data, query=query, search_type=search_type)

# נתיב בדיקת תקינות
@app.route('/health', methods=['GET'])
def health_check():
    if client is None:
        return {"status": "error", "message": "❌ חיבור ל-BigQuery נכשל"}, 500
    return {"status": "ok", "message": "✅ האפליקציה רצה בהצלחה"}, 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
