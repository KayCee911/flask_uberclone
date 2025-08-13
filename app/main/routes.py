from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.extensions import db
from app.models import User

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def home():
    return render_template('home.html')


@main_bp.route('/request-ride', methods=['GET', 'POST'])
@login_required
def request_ride():
    if request.method == 'POST':
        pickup = request.form.get('pickup')
        dropoff = request.form.get('dropoff')
        ride_type = request.form.get('ride_type')

        # Save ride request logic here (DB insert, etc.)
        flash(f"{current_user.username}, your ride from {pickup} to {dropoff} ({ride_type}) has been requested!", "success")
        return redirect(url_for('main.home'))

    return render_template('request_ride.html')

