import sqlite3

# יצירת חיבור למסד הנתונים
conn = sqlite3.connect("users.db")
cursor = conn.cursor()

# יצירת טבלת משתמשים (אם היא לא קיימת)
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
)
''')

# הכנסה של משתמש ראשוני (יש להחליף את הסיסמה בערך חזק)
cursor.execute("INSERT INTO users (email, password) VALUES (?, ?)", ("admin@example.com", "1234"))

# שמירה וסגירת החיבור
conn.commit()
conn.close()

print("✅ מסד הנתונים נוצר בהצלחה!")
