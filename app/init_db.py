import sqlite3
import os

def get_db_path():
    # Obtiene el directorio de la aplicación y crea la ruta completa a la base de datos
    app_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(app_dir, 'splitter.db')

def init_db():
    db_path = get_db_path()
    print(f"Conectando a la base de datos en {db_path}...")
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    print("Creando tablas...")
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
    print("Base de datos inicializada correctamente.")

if __name__ == '__main__':
    init_db()
