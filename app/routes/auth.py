from flask import Blueprint, render_template, request, url_for, redirect, flash, session, g
from werkzeug.security import generate_password_hash, check_password_hash

from app import db

from app.models.models import User

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/register', methods = ['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User(username, generate_password_hash(password))

        error = None

        user_name = User.query.filter_by(username = username).first()

        if user_name == None:
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('auth.register'))
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