# The implementation Al Madi and us came up with requires global GOOGLE
# pylint: disable=global-variable-not-assigned
'''Uses flask to manage user login, logout, and flow. 
Uses Google OAuth2 for login.'''
from flask import Blueprint, render_template, redirect, url_for, session
# from flask import request
from flask_login import login_user, logout_user
from website import db, GOOGLE
from .models import User

# Create a blueprint
auth_blueprint = Blueprint('auth', __name__)

@auth_blueprint.route('/login')
def login():
    '''Login page'''
    global GOOGLE
    return render_template('login.html')

@auth_blueprint.route('/google_login')
def google_login():
    '''Redirect to Google login page'''
    global GOOGLE
    return GOOGLE.authorize(callback=url_for('auth.authorized', _external=True))

@auth_blueprint.route('/login/authorized')
def authorized():
    '''Callback page after Google login. Calls loginUser() to finish login process.'''
    global GOOGLE
    response = GOOGLE.authorized_response()
    if response is None or response.get('access_token') is None:
        return 'Login failed.'

    session['google_token'] = (response['access_token'], '')
    userinfo = GOOGLE.get('userinfo')
    print(userinfo.data)
    email = userinfo.data['email']
    existing_user = User.query.filter_by(email=email).first()
    if not existing_user:
        existing_user = User(email=email)
    db.session.add(existing_user)
    db.session.commit()
    login_user(existing_user)
    return redirect(url_for('views.main_page'))

@auth_blueprint.route('/logout')
def logout():
    '''Logout page'''
    logout_user()
    session.pop('google_token', None)
    session.clear()
    return redirect(url_for('auth.login'))

@GOOGLE.tokengetter
def get_google_oauth_token():
    '''Get Google token'''
    return session.get('google_token')
