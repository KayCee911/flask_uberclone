from flask import Flask
from .extensions import db, login_manager  # Import shared extensions (SQLAlchemy, LoginManager)
from .models import User  # Needed for login_manager to query the User table
from .auth.routes import auth_bp  # Authentication-related routes (signup, login, logout)
from .main.routes import main_bp  # General app routes (home, dashboard, etc.)

def create_app():
    # 🚀 Create the Flask app instance
    # `instance_relative_config=True` allows configs to be loaded from the 'instance' folder
    app = Flask(__name__, instance_relative_config=True)

    # 🛠️ Load configuration settings for secret keys, DB, and SQLAlchemy behavior
    app.config.from_mapping(
        SECRET_KEY='mysecretkey',  # 🔐 Used for session signing (should be secure in production)
        SQLALCHEMY_DATABASE_URI='sqlite:///uberclone.db',  # 🛢️ Using SQLite for dev
        SQLALCHEMY_TRACK_MODIFICATIONS=False  # ✅ Turns off unnecessary tracking
    )

    # 🔌 Initialize our database and login manager extensions with this app instance
    db.init_app(app)
    login_manager.init_app(app)

    # 👤 Tell Flask-Login how to load a user from the database
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))  # 🔁 Return user by primary key (used in session management)

    # 🧩 Register blueprints to plug in routes from different parts of the app
    app.register_blueprint(auth_bp)  # 👉 auth/routes.py
    app.register_blueprint(main_bp)  # 👉 main/routes.py

    # ✅ Return the fully configured app instance
    return app
