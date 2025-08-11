from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

# 🧠 This is our main user model for both riders and drivers
class User(UserMixin, db.Model):
    __tablename__ = 'users'  # Optional: explicitly define table name

    id = db.Column(db.Integer, primary_key=True)  # Unique user ID
    username = db.Column(db.String(150), nullable=False, unique=True)  # Login identifier
    email = db.Column(db.String(150), nullable=False, unique=True)  # For notifications, unique
    password = db.Column(db.String(200), nullable=False)  # Hashed password
    role = db.Column(db.String(10), nullable=False, default='rider')  
    # Either 'rider' or 'driver'. This allows role-based features

    # 📦 Optional: Add more fields later like phone number, profile pic, etc.

    def __repr__(self):
        return f'<User {self.username} ({self.role})>'
