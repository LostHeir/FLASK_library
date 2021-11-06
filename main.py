import os
import requests
from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get('SECRET_KEY')
# Generated from terminal: python -c "import secrets; print(secrets.token_urlsafe(32))"

# Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/books')
def all_books():
    lib_data = requests.get('https://www.googleapis.com/books/v1/volumes?q=Hobbit').json()['items']
    print(lib_data)
    return render_template("all-books.html", books=lib_data)


# MAIN
if __name__ == "__main__":
    app.run(debug=True)
