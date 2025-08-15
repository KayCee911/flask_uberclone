# app/main/routes.py
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from ..extensions import db
from ..models import Ride, User
from .forms import RideRequestForm
from functools import wraps

main_bp = Blueprint('main', __name__)

def role_required(role):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            if not current_user.is_authenticated:
                flash('Please log in first.', 'warning')
                return redirect(url_for('auth.login'))
            if current_user.role != role:
                flash("You don't have access to that page.", 'danger')
                return redirect(url_for('main.home'))
            return fn(*args, **kwargs)
        return wrapper
    return decorator

@main_bp.route('/')
def home():
    return render_template('home.html')

# Rider: request a ride
@main_bp.route('/request-ride', methods=['GET', 'POST'])
@login_required
def request_ride():
    if current_user.role != 'rider':
        flash('Only riders can request rides.', 'danger')
        return redirect(url_for('main.home'))

    form = RideRequestForm()
    if form.validate_on_submit():
        ride = Ride(
            rider_id=current_user.id,
            pickup_address=form.pickup.data,
            pickup_lat=float(form.pickup_lat.data) if form.pickup_lat.data else None,
            pickup_lng=float(form.pickup_lng.data) if form.pickup_lng.data else None,
            dropoff_address=form.dropoff.data,
            dropoff_lat=float(form.dropoff_lat.data) if form.dropoff_lat.data else None,
            dropoff_lng=float(form.dropoff_lng.data) if form.dropoff_lng.data else None,
            status='requested'
        )
        db.session.add(ride)
        db.session.commit()
        flash('Ride requested! Waiting for a driver to accept.', 'success')
        return redirect(url_for('main.home'))

    return render_template('request_ride.html', form=form)

# Driver: dashboard (see open rides)
@main_bp.route('/driver/dashboard')
@login_required
@role_required('driver')
def driver_dashboard():
    open_rides = Ride.query.filter_by(status='requested').order_by(Ride.created_at.desc()).all()
    my_active = Ride.query.filter(Ride.driver_id == current_user.id, Ride.status.in_(['accepted','en_route'])).all()
    return render_template('driver_dashboard.html', open_rides=open_rides, my_active=my_active)

# Driver: accept a ride
@main_bp.route('/driver/rides/<int:ride_id>/accept', methods=['POST'])
@login_required
@role_required('driver')
def accept_ride(ride_id):
    ride = Ride.query.get_or_404(ride_id)
    if ride.status != 'requested':
        flash('Ride already taken or not available.', 'warning')
        return redirect(url_for('main.driver_dashboard'))

    ride.status = 'accepted'
    ride.driver_id = current_user.id
    db.session.commit()
    flash(f'Ride {ride.id} accepted. Contact rider at {ride.rider.phone}.', 'success')
    return redirect(url_for('main.driver_dashboard'))

# Driver: update status (optional simple flow)
@main_bp.route('/driver/rides/<int:ride_id>/status', methods=['POST'])
@login_required
@role_required('driver')
def update_ride_status(ride_id):
    ride = Ride.query.get_or_404(ride_id)
    next_status = request.form.get('status')  # expected: en_route | completed | cancelled
    if next_status not in ['en_route', 'completed', 'cancelled']:
        flash('Invalid status.', 'danger')
        return redirect(url_for('main.driver_dashboard'))

    ride.status = next_status
    db.session.commit()
    flash(f'Ride {ride.id} marked as {next_status}.', 'info')
    return redirect(url_for('main.driver_dashboard'))
