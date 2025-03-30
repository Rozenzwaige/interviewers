from flask import Blueprint, render_template, request, redirect, url_for
import sqlite3

admin_bp = Blueprint('admin', __name__)

DATABASE = 'users.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@admin_bp.route('/admin')
def admin_panel():
    db = get_db()
    users = db.execute("SELECT * FROM users WHERE approved = FALSE").fetchall()
    db.close()
    return render_template('admin.html', users=users)

@admin_bp.route('/approve/<email>')
def approve_user(email):
    db = get_db()
    db.execute("UPDATE users SET approved = TRUE WHERE email = ?", (email,))
    db.commit()
    db.close()
    return redirect(url_for('admin.admin_panel'))
