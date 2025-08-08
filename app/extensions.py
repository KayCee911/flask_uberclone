from flask_sqlalchemy import SQLAlchemy
# LoginManager lets us easily manage login/logout, session protection, and user loading
from flask_login import LoginManager
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login' 
login_manager.login_message_category = 'info'  
