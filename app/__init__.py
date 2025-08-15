from flask import Flask
from .extensions import db, login_manager
from . import models
from flask_migrate import Migrate
from flask_socketio import SocketIO
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from .models import User, Ride, Car  # import models

socketio = SocketIO()
migrate = Migrate()

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
    migrate.init_app(app, db)
    socketio.init_app(app)

    # User loader for flask-login
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    login_manager.login_view = 'auth.login'

    # Register blueprints
    from .auth.routes import auth_bp
    from .main.routes import main_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(main_bp)

    # Flask-Admin
    admin = Admin(app, name='UberClone Admin', template_mode='bootstrap4')
    admin.add_view(ModelView(User, db.session))
    admin.add_view(ModelView(Ride, db.session))
    admin.add_view(ModelView(Car, db.session))

    return app
