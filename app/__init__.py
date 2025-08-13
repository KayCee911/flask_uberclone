from flask import Flask
from .extensions import db, login_manager
from .models import User

def create_app():
    app = Flask(__name__, instance_relative_config=True)

    # Config
    app.config.from_mapping(
        SECRET_KEY='mysecretkey',  
        SQLALCHEMY_DATABASE_URI='sqlite:///uberclone.db',
        SQLALCHEMY_TRACK_MODIFICATIONS=False
    )

    # Init extensions
    db.init_app(app)
    login_manager.init_app(app)

    # User loader for flask-login
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    login_manager.login_view = 'auth.login'  # Redirect here if login required

    # Register blueprints
    from .auth.routes import auth_bp
    from .main.routes import main_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(main_bp)

    # Create DB tables
    with app.app_context():
        db.create_all()

    return app
