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

    # Tabla de usuarios
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 username TEXT UNIQUE,
                 email TEXT UNIQUE,
                 password TEXT)''')

    # Tabla de grupos
    c.execute('''CREATE TABLE IF NOT EXISTS groups (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 name TEXT UNIQUE,
                 creator_id INTEGER,
                 FOREIGN KEY (creator_id) REFERENCES users (id))''')

    # Tabla de miembros del grupo
    c.execute('''CREATE TABLE IF NOT EXISTS group_members (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 group_id INTEGER,
                 user_id INTEGER,
                 is_admin BOOLEAN DEFAULT FALSE,
                 FOREIGN KEY (group_id) REFERENCES groups (id),
                 FOREIGN KEY (user_id) REFERENCES users (id))''')

    # Tabla de gastos en grupo
    c.execute('''CREATE TABLE IF NOT EXISTS group_expenses (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 group_id INTEGER,
                 user_id INTEGER,
                 amount REAL,
                 description TEXT,
                 FOREIGN KEY (group_id) REFERENCES groups (id),
                 FOREIGN KEY (user_id) REFERENCES users (id))''')

    # Tabla de transacciones individuales
    c.execute('''CREATE TABLE IF NOT EXISTS transactions (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 user_id INTEGER,
                 amount REAL,
                 description TEXT,
                 FOREIGN KEY (user_id) REFERENCES users (id))''')

    conn.commit()
    conn.close()
    print("Base de datos inicializada correctamente.")
