"""
This module initializes the Flask application.
"""

import os
from flask import Flask
from website.views import views_blueprint
from website.routes import routes_blueprint

def create_app():
    """
    Creates and configures a Flask application.
    
    Returns:
        Flask app instance.
    """
    app = Flask(__name__)

    # Register blueprints with unique names
    app.register_blueprint(views_blueprint)
    app.register_blueprint(routes_blueprint)

    return app
