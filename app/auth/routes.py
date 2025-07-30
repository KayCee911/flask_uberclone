from flask import Blueprint, render_template, redirect, url_for, flash
from .forms import RegisterForm
from ..models import db, User

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        # Check if user already exists
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user:
            flash('Email already registered.')
            return redirect(url_for('auth.register'))

        new_user = User(
            username=form.username.data,
            email=form.email.data
        )
        new_user.set_password(form.password.data)
        db.session.add(new_user)
        db.session.commit()
        print("✅ User committed to database")

        flash('Registration successful. You can now log in.')
        return redirect(url_for('auth.login'))

    return render_template('register.html', form=form)
