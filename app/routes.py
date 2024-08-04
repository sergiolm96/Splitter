from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import os

bp = Blueprint('main', __name__)

def get_db_connection():
    app_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(app_dir, 'splitter.db')
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

@bp.route('/')
def index():
    logged_in = 'user_id' in session
    return render_template('index.html', logged_in=logged_in)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        conn.close()
        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            flash('Inicio de sesión exitoso.', 'success')
            return redirect(url_for('main.index'))
        else:
            flash('Credenciales inválidas.', 'error')
    return render_template('login.html')

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])
        try:
            conn = get_db_connection()
            conn.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
            conn.commit()
            conn.close()
            flash('Usuario creado con éxito. Puedes iniciar sesión ahora.', 'success')
            return redirect(url_for('main.login'))
        except sqlite3.IntegrityError:
            flash('El nombre de usuario ya está en uso.', 'error')
        except sqlite3.Error as e:
            flash(f'Error al registrar el usuario: {e}', 'error')
    return render_template('register.html')

@bp.route('/create_group', methods=['GET', 'POST'])
def create_group():
    if request.method == 'POST':
        try:
            group_name = request.form['group_name']
            members = request.form['members'].split(',')
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute('INSERT INTO groups (name) VALUES (?)', (group_name,))
            group_id = cur.lastrowid
            for member in members:
                cur.execute('INSERT INTO group_members (group_id, member) VALUES (?, ?)', (group_id, member.strip()))
            conn.commit()
            conn.close()
            flash('Grupo creado exitosamente.', 'success')
        except KeyError as e:
            flash(f'Error: {e}', 'error')
        except sqlite3.Error as e:
            flash(f'Error al crear el grupo: {e}', 'error')
    return render_template('create_group.html')

@bp.route('/add_group_expense', methods=['GET', 'POST'])
def add_group_expense():
    if request.method == 'POST':
        try:
            group_id = request.form['group_id']
            members = request.form['members'].split(',')
            amount = float(request.form['amount'])
            description = request.form['description']
            conn = get_db_connection()
            for member in members:
                conn.execute('INSERT INTO expenses (group_id, member, amount, description) VALUES (?, ?, ?, ?)', 
                             (group_id, member.strip(), amount, description))
            conn.commit()
            conn.close()
            flash('Gasto añadido exitosamente.', 'success')
        except KeyError as e:
            flash(f'Error: {e}', 'error')
        except ValueError:
            flash('Monto inválido.', 'error')
        except sqlite3.Error as e:
            flash(f'Error al añadir el gasto: {e}', 'error')
    return render_template('add_group_expense.html')

@bp.route('/transactions')
def transactions():
    conn = get_db_connection()
    expenses = conn.execute('SELECT * FROM expenses').fetchall()
    conn.close()
    return render_template('transactions.html', expenses=expenses)

@bp.route('/add_expense', methods=['GET', 'POST'])
def add_expense():
    if request.method == 'POST':
        try:
            member = request.form['member']
            amount = float(request.form['amount'])
            description = request.form['description']
            conn = get_db_connection()
            conn.execute('INSERT INTO expenses (member, amount, description) VALUES (?, ?, ?)', 
                         (member, amount, description))
            conn.commit()
            conn.close()
            flash('Gasto añadido exitosamente.', 'success')
        except KeyError as e:
            flash(f'Error: {e}', 'error')
        except ValueError:
            flash('Monto inválido.', 'error')
        except sqlite3.Error as e:
            flash(f'Error al añadir el gasto: {e}', 'error')
    return render_template('add_expense.html')

@bp.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('Has cerrado sesión.', 'info')
    return redirect(url_for('main.index'))
