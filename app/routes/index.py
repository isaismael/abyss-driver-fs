from flask import Blueprint, render_template

from app.routes.auth import login_required


bp_index = Blueprint('/', __name__)

@bp_index.route('/')
@login_required
def index():
    return render_template('home.html')