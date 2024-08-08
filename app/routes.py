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
        email = request.form['email']
        password = generate_password_hash(request.form['password'])
        conn = get_db_connection()
        try:
            conn.execute('INSERT INTO users (username, email, password) VALUES (?, ?, ?)', (username, email, password))
            conn.commit()
            flash('Usuario creado con éxito. Puedes iniciar sesión ahora.', 'success')
            return redirect(url_for('main.login'))
        except sqlite3.IntegrityError:
            flash('El nombre de usuario o el correo electrónico ya están en uso.', 'error')
        except sqlite3.Error as e:
            flash(f'Error al registrar el usuario: {e}', 'error')
        finally:
            conn.close()
    return render_template('register.html')

@bp.route('/create_group', methods=['GET', 'POST'])
def create_group():
    if request.method == 'POST':
        group_name = request.form.get('group_name')
        conn = get_db_connection()
        try:
            cur = conn.cursor()
            cur.execute('INSERT INTO groups (name, creator_id) VALUES (?, ?)', (group_name, session['user_id']))
            group_id = cur.lastrowid
            
            # Añadir el creador como administrador
            cur.execute('INSERT INTO group_members (group_id, user_id, is_admin) VALUES (?, ?, ?)', (group_id, session['user_id'], True))
            
            conn.commit()
            flash('Grupo creado con éxito', 'success')
        except sqlite3.Error as e:
            flash(f'Error al crear el grupo: {e}', 'error')
        finally:
            conn.close()
        return redirect(url_for('main.manage_groups'))

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
                conn.execute('INSERT INTO group_expenses (group_id, user_id, amount, description) VALUES (?, ?, ?, ?)', 
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
        return redirect(url_for('main.add_group_expense'))

    conn = get_db_connection()
    groups = conn.execute('SELECT id, name FROM groups').fetchall()
    conn.close()
    return render_template('add_group_expense.html', groups=groups)


@bp.route('/transactions')
def transactions():
    conn = get_db_connection()
    try:
        # Recuperar las transacciones individuales
        transactions = conn.execute('SELECT users.username, amount, description FROM transactions JOIN users ON transactions.user_id = users.id').fetchall()
    except sqlite3.Error as e:
        flash(f'Error al recuperar las transacciones: {e}', 'error')
        transactions = []
    finally:
        conn.close()
    
    return render_template('transactions.html', transactions=transactions)

@bp.route('/add_expense', methods=['GET', 'POST'])
def add_expense():
    if request.method == 'POST':
        try:
            member = request.form['member']
            amount = float(request.form['amount'])
            description = request.form['description']
            conn = get_db_connection()
            user = conn.execute('SELECT id FROM users WHERE username = ?', (member,)).fetchone()
            if user:
                user_id = user['id']
                conn.execute('INSERT INTO transactions (user_id, amount, description) VALUES (?, ?, ?)', 
                             (user_id, amount, description))
                conn.commit()
                flash('Gasto añadido exitosamente.', 'success')
            else:
                flash(f'El usuario {member} no existe.', 'warning')
        except KeyError as e:
            flash(f'Error: {e}', 'error')
        except ValueError:
            flash('Monto inválido.', 'error')
        except sqlite3.Error as e:
            flash(f'Error al añadir el gasto: {e}', 'error')
        finally:
            conn.close()
    return render_template('add_expense.html')

@bp.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('Has cerrado sesión.', 'info')
    return redirect(url_for('main.index'))

@bp.route('/manage_groups', methods=['GET', 'POST'])
def manage_groups():
    conn = get_db_connection()
    groups = conn.execute('SELECT * FROM groups').fetchall()

    if request.method == 'POST':
        action = request.form.get('action')
        group_id = request.form.get('group_id')

        if action == 'delete_group':
            try:
                conn.execute('DELETE FROM groups WHERE id = ?', (group_id,))
                conn.execute('DELETE FROM group_members WHERE group_id = ?', (group_id,))
                conn.execute('DELETE FROM group_expenses WHERE group_id = ?', (group_id,))
                flash('Grupo eliminado con éxito.', 'success')
            except sqlite3.Error as e:
                flash(f'Error al eliminar el grupo: {e}', 'error')
        elif action == 'add_member':
            member = request.form.get('new_member')
            try:
                conn.execute('INSERT INTO group_members (group_id, user_id) VALUES (?, ?)', (group_id, member))
                flash('Miembro añadido con éxito.', 'success')
            except sqlite3.Error as e:
                flash(f'Error al añadir el miembro: {e}', 'error')

        conn.commit()

    conn.close()
    return render_template('manage_groups.html', groups=groups)

@bp.route('/manage_members/<int:group_id>', methods=['GET', 'POST'])
def manage_members(group_id):
    conn = get_db_connection()
    user_id = session.get('user_id')
    
    # Verificar si el usuario es administrador del grupo
    is_admin = conn.execute('SELECT is_admin FROM group_members WHERE group_id = ? AND user_id = ?', (group_id, user_id)).fetchone()
    if not is_admin or not is_admin['is_admin']:
        flash('No tienes permisos para administrar este grupo.', 'error')
        conn.close()
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        action = request.form.get('action')
        
        if action == 'add_member':
            new_member = request.form['new_member']
            try:
                conn.execute('INSERT INTO group_members (group_id, user_id) VALUES (?, ?)', (group_id, new_member))
                conn.commit()
                flash('Miembro añadido con éxito.', 'success')
            except sqlite3.Error as e:
                flash(f'Error al añadir el miembro: {e}', 'error')
        
        elif action == 'remove_member':
            remove_member = request.form['remove_member']
            try:
                conn.execute('DELETE FROM group_members WHERE group_id = ? AND user_id = ?', (group_id, remove_member))
                conn.commit()
                flash('Miembro eliminado con éxito.', 'success')
            except sqlite3.Error as e:
                flash(f'Error al eliminar el miembro: {e}', 'error')
    
    users = conn.execute('SELECT id, username FROM users').fetchall()
    members = conn.execute('SELECT user_id, username FROM group_members JOIN users ON group_members.user_id = users.id WHERE group_id = ?', (group_id,)).fetchall()
    
    conn.close()
    return render_template('manage_members.html', group_id=group_id, users=users, members=members)



