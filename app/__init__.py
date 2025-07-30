from flask import Flask
from app.models import db
from app.routes import main
from app.auth.routes import auth

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'uber_clone-secret-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///uberclone.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ECHO'] = True


    db.init_app(app)

    app.register_blueprint(main)
    app.register_blueprint(auth)

    with app.app_context():
        db.create_all()

    return app
