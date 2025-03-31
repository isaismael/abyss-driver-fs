from flask import Blueprint, render_template,url_for

home_bp = Blueprint('home', __name__)

@home_bp.route('/')
def home():
    return render_template('base.html', content=render_template('home.html'))

@home_bp.route('/login')
def login():
    return render_template('login.html')

@home_bp.route('/busqueda')
def busqueda():
    return render_template('busqueda.html')