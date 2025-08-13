from flask import render_template, redirect, url_for, flash, request, Blueprint
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from .forms import RegisterForm, LoginForm
from ..extensions import db
from app.models import User
from . import auth

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if request.method == 'POST':
        print("📩 Form submitted")
        print("Validation result:", form.validate_on_submit())
        print("Form errors:", form.errors)
        print("Form data ->", {
            "username": form.username.data,
            "email": form.email.data,
            "phone": form.phone.data,
            "password": form.password.data,
            "role": form.role.data
        })

    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        new_user = User(
            username=form.username.data,
            email=form.email.data,
            phone=form.phone.data,
            password=hashed_password,
            role=form.role.data
        )

        print("🛠 Adding user to DB...")
        db.session.add(new_user)
        db.session.commit()
        print("✅ User saved with ID:", new_user.id)

        flash('Account created! You can now log in.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('register.html', form=form)




@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('Logged in successfully!', 'success')
            return redirect(url_for('main.home'))
        else:
            flash('Invalid email or password.', 'danger')

    return render_template('login.html', form=form)


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.home'))
