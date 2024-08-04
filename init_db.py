import sqlite3

def init_db():
    conn = sqlite3.connect('splitter.db')
    c = conn.cursor()

    # Crear tablas
    c.execute('''CREATE TABLE IF NOT EXISTS members (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 name TEXT UNIQUE)''')

    c.execute('''CREATE TABLE IF NOT EXISTS expenses (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 member TEXT,
                 amount REAL,
                 description TEXT)''')

    conn.commit()
    conn.close()
