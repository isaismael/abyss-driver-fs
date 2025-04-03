from flask import Blueprint, render_template, request, url_for, redirect, flash, session, g
from werkzeug.security import generate_password_hash, check_password_hash

from app import db

from app.models.models import User

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

# ESTA FUNCION ES LA QUE SE ENCARGA DE PROTEGER LAS RUTAS, SI INICIÓ SESSION O NO
import functools

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(*args, **kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(*args, **kwargs)
    return wrapped_view


@auth_bp.route('/register', methods=['GET', 'POST'])
@login_required
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role_id = request.form['role']

        # Create user with all three parameters
        user = User(
            username=username,
            password=generate_password_hash(password),
            role_id=role_id
        )

        error = None
        user_name = User.query.filter_by(username=username).first()

        if user_name is None:
            try:
                db.session.add(user)
                db.session.commit()
                return redirect(url_for('auth.register'))
            except Exception as e:
                db.session.rollback()
                error = f'Error al registrar usuario: {str(e)}'
        else:
            error = f'El usuario {username} ya existe'

        flash(error)

    return render_template('register.html')

@auth_bp.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        error = None

        user = User.query.filter_by(username = username).first()
        if user == None:
            error = 'Nombre de usuario incorrecto'
        elif not check_password_hash(user.password, password):
            error = 'Contraseña incorrecta'

        if error is None:
            session.clear()
            session['user_id'] = user.id
            return redirect(url_for('home.home'))
        
        flash(error)

    return render_template('login.html')

@auth_bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = User.query.get_or_404(user_id)
        
@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))

