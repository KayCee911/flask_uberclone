from flask import Blueprint, render_template, redirect, url_for, session
from flask import render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app.forms import RideRequestForm
from app.models import RideRequest, db

main = Blueprint('main', __name__)

@main.route('/')
def home():
    user_id = session.get('user_id')
    return render_template('home.html', user_id=user_id)



