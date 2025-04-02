from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"

    db.init_app(app)

    # importar BP
    from app.routes.index import bp_index
    from app.routes.home import home_bp
    from app.routes.auth import auth_bp
    
    # acá voy a registrando todos los bp
    app.register_blueprint(bp_index)
    app.register_blueprint(home_bp)
    app.register_blueprint(auth_bp)
    
    with app.app_context():
        db.create_all()
    
    return app