import sqlite3

def init_db():
    conn = sqlite3.connect('splitter.db')
    c = conn.cursor()

    # Crear tablas de base de datos
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 username TEXT UNIQUE,
                 password TEXT)''')

    c.execute('''CREATE TABLE IF NOT EXISTS groups (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 name TEXT UNIQUE)''')

    c.execute('''CREATE TABLE IF NOT EXISTS group_members (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 group_id INTEGER,
                 member TEXT,
                 FOREIGN KEY (group_id) REFERENCES groups (id))''')

    c.execute('''CREATE TABLE IF NOT EXISTS expenses (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 group_id INTEGER,
                 member TEXT,
                 amount REAL,
                 description TEXT,
                 FOREIGN KEY (group_id) REFERENCES groups (id))''')

    conn.commit()
    conn.close()
