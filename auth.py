from flask import Blueprint, request, session, redirect, url_for, render_template
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

auth_bp = Blueprint('auth', __name__)

DATABASE = 'users.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        hashed_password = generate_password_hash(password)

        db = get_db()
        try:
            db.execute("INSERT INTO users (email, password, approved) VALUES (?, ?, ?)", 
                       (email, hashed_password, False))
            db.commit()
        except sqlite3.IntegrityError:
            return "האימייל כבר קיים במערכת."
        db.close()

        return "נרשמת בהצלחה, ההרשאה תאושר ע״י מנהל."

    return render_template('register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
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
                return redirect(url_for('home'))  # נשלח לדף הראשי
            else:
                return "החשבון ממתין לאישור מנהל."

        return "פרטי ההתחברות שגויים."

    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('auth.login'))
