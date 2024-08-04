from flask import Blueprint, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from .models import get_db_connection

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

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
            return redirect(url_for('main.index'))
        else:
            return 'Credenciales inválidas', 401
    return render_template('login.html')

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])
        conn = get_db_connection()
        conn.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
        conn.commit()
        conn.close()
        return redirect(url_for('main.login'))
    return render_template('register.html')

@bp.route('/create_group', methods=['GET', 'POST'])
def create_group():
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
    except KeyError as e:
        return f"KeyError: {e}", 400  # Return a meaningful error message
    return redirect(url_for('main.index'))


@bp.route('/add_group_expense', methods=['GET', 'POST'])
def add_group_expense():
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
    return redirect(url_for('main.index'))

@bp.route('/transactions', methods=['GET', 'POST'])
def transactions():
    # Lógica para obtener y mostrar las transacciones
    return render_template('transactions.html')


@bp.route('/add_expense', methods=['GET', 'POST'])
def add_expense():
    try:
        member = request.form['member']
        amount = float(request.form['amount'])
        description = request.form['description']
        conn = get_db_connection()
        conn.execute('INSERT INTO expenses (member, amount, description) VALUES (?, ?, ?)', 
                     (member, amount, description))
        conn.commit()
        conn.close()
    except KeyError as e:
        return f"KeyError: {e}", 400  # Return a meaningful error message
    return redirect(url_for('main.index'))


