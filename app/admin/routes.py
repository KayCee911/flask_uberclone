from flask import Blueprint, render_template
from flask_login import login_required
from ..models import User, Ride

admin_bp = Blueprint('admin', __name__, template_folder='templates')

@admin_bp.route('/')
@login_required
def dashboard():
    users = User.query.all()
    rides = Ride.query.all()
    return render_template('admin/dashboard.html', users=users, rides=rides)
