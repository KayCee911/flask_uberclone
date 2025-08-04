from flask import Blueprint, render_template, redirect, url_for, session

main = Blueprint('main', __name__)

@main.route('/')
def home():
    user_id = session.get('user_id')
    return render_template('home.html', user_id=user_id)

