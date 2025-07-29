from flask import Flask
from app.auth.routes import auth

def create_app():
    app = Flask(__name__)
    app.secret_key = 'uber_clone_secret'

    from .routes import main
    from .auth import auth

    app.register_blueprint(main)
    app.register_blueprint(auth, url_prefix='/auth')
    return app
