# auth.py

from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from . import db

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/login', methods=['POST'])
def login_post():
    # verify user has correct credentials
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()
    # check if user exists
    # take the user supplied password, hash it, and compare it to hashed password in DB
    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login'))

    # IF above successfull, create the session with login_user before the redirect to the profile
    login_user(user, remember=remember)
    name = user.name
    return redirect(url_for('main.profile', name=name))

@auth.route('/signup')
def signup():
    return render_template('signup.html')

@auth.route('/signup', methods=['POST'])
def signup_post():
    # validate and add user to DB
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')

    # if this returns a user, then the email already exists in database
    user = User.query.filter_by(email=email).first() 
    if user:
        flash('Email adress already exists')       # flash sends a message to the next request
        return redirect(url_for('auth.signup'))
    
    #create new user
    new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'))

    #add to DB
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('auth.login'))

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))
