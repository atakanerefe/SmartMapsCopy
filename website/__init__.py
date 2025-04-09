"""
This module initializes the Flask application.
"""

import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_oauthlib.client import OAuth
from dotenv import load_dotenv

load_dotenv()
GOOGLE = None
db = SQLAlchemy()


def create_app():
    """
    Creates and configures a Flask application.

    Returns:
        Flask app instance.
    """
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get('APP_SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = (
        os.environ.get('DATABASE_URL')
        .replace("postgres", "postgresql", 1)
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    login_manager = LoginManager(app)
    login_manager.login_view = 'auth.login'

    global GOOGLE
    GOOGLE = google_auth(app)
    # pylint: disable=C0415
    from .models import User
    from .views import views_blueprint
    from .routes import routes_blueprint
    from .auth import auth_blueprint

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    # Register blueprints with unique names
    app.register_blueprint(views_blueprint)
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(routes_blueprint)

    with app.app_context():
        db.create_all()  # Create tables (if not created)

    return app


def google_auth(app):
    '''Google OAuth configuration for login.'''

    oauth = OAuth(app)

    google = oauth.remote_app(
        'google',
        consumer_key=os.environ.get('GOOGLE_CLIENT_ID'),
        consumer_secret=os.environ.get('GOOGLE_CLIENT_SECRET'),
        request_token_params={'scope': 'email', },
        base_url='https://www.googleapis.com/oauth2/v1/',
        request_token_url=None,
        access_token_method='POST',
        access_token_url='https://accounts.google.com/o/oauth2/token',
        authorize_url='https://accounts.google.com/o/oauth2/auth',
    )

    return google
