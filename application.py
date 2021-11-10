from flask import Flask
from model import db
from views import library_app
import os


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.environ.get('SECRET_KEY')
    # Generated from terminal: python -c "import secrets; print(secrets.token_urlsafe(32))"
    app.config["JSON_SORT_KEYS"] = False  # Disables alphabetical sorting
    app.config['JSON_AS_ASCII'] = False  # Supports UTF-8 enncoding
    app.config["DEBUG"] = True  # To pretty print on Heroku

    # Connect to Database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Gets rid of warnigs about SQLALCHEMY_TRACK_MODIFICATIONS
    db.init_app(app)
    with app.app_context():
        db.create_all()

    app.register_blueprint(library_app)
    return app
