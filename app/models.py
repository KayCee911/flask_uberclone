from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin
from app.extensions import db


# 🧠 This is our main user model for both riders and drivers
class User(UserMixin, db.Model):
    __tablename__ = 'users'  # Optional: explicitly define table name

    id = db.Column(db.Integer, primary_key=True)  # Unique user ID
    username = db.Column(db.String(150), nullable=False, unique=True)  # Login identifier
    email = db.Column(db.String(150), nullable=False, unique=True)  # For notifications, unique
    phone = db.Column(db.String(15), nullable=False)
    password = db.Column(db.String(200), nullable=False)  
    role = db.Column(db.String(10), nullable=False, default='rider')  
   



    def __repr__(self):
        return f'<User {self.username} ({self.role})>'



class Ride(db.Model):
    __tablename__ = 'rides'
    id = db.Column(db.Integer, primary_key=True)

    rider_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    driver_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)

    pickup_address = db.Column(db.String(255), nullable=False)
    pickup_lat = db.Column(db.Float, nullable=True)
    pickup_lng = db.Column(db.Float, nullable=True)

    dropoff_address = db.Column(db.String(255), nullable=False)
    dropoff_lat = db.Column(db.Float, nullable=True)
    dropoff_lng = db.Column(db.Float, nullable=True)

    status = db.Column(db.String(20), nullable=False, default='requested')
    # requested | accepted | en_route | completed | cancelled

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    rider = db.relationship('User', foreign_keys=[rider_id], backref='rides_requested')
    driver = db.relationship('User', foreign_keys=[driver_id], backref='rides_taken')

    def __repr__(self):
        return f'<Ride {self.id} {self.status}>'