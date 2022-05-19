from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash          # use hashing to store our passwords (never store in plain text)
from . import db
from flask_login import login_user, login_required, logout_user, current_user      # functions that make logins/logouts easier 


auth = Blueprint('auth', __name__)    # set up a auth blueprint for our flask application


@auth.route('/login', methods=['GET', 'POST'])    # url has a /login at the end, brings us to login pg (the @ indicates a decorator)
                                                  # HTTP has several methods to communicate with the server (GET and POST are two of them)
                                                  # we can now accept these requests: GET is for retrieving info, POST is for updating/creating 
def login():  
    if request.method == 'POST':
        email = request.form.get('email')         # get info from the form so we can check that it's valid
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()    # query the database for all users with the inputted email (for this app it has to be unique)
        if user:    # aka if valid user found in db
            if check_password_hash(user.password, password):       # hash password, check against user.password
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)                    # remember to keep user signed in until the session data is wiped. So when the flask server is restarted, this will become False
                return redirect(url_for('views.recommend'))
            else:
                flash('Incorrect password, try again.', category='error')    # wrong password
        else:
            flash('Email does not exist.', category='error')                 # email not in db yet

    return render_template("login.html", user=current_user)          # this is where we pass variables (here it's user), which we can use in login.html


@auth.route('/logout')
@login_required           # a 2nd decorator, makes sure the user is logged in b4 they can log out
def logout():
    logout_user()
    return redirect(url_for('auth.login'))   # after logging out, redirect to login pg



@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':                   # if there was a POST request (aka form was submitted)
        email = request.form.get('email')          # get all 4 inputs from the form (use the get() function)
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        # below, we're making sure the inputted info is valid. If all the info passes the requirements, we add the user to the database
        if user:
            flash('Email already exists.', category='error')      #  message flash displays a message to the user (shows up at top of screen). Here, a new/unique email must be inputted when signing up
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(password1, method='sha256'))    # sha256 is a hashing algorithm, output is always 256 bits long. These parameters are the fields we've defined for a user in models.py
            db.session.add(new_user)            # add new user to db (created in __init__.py)
            db.session.commit()                 # commit changes to db
            login_user(new_user, remember=True)
            flash('Account created! Welcome!', category='success')
            return redirect(url_for('views.home'))    # redirect to home page since sign up was successful (and we'll log the user in automatically). views.home is in format: blueprint.function

    return render_template("sign_up.html", user=current_user)
