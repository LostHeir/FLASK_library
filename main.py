import os
from flask import Flask, render_template, redirect, url_for, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy import PickleType, func
from library_manager import get_new_books


app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get('SECRET_KEY')
# Generated from terminal: python -c "import secrets; print(secrets.token_urlsafe(32))"
app.config["JSON_SORT_KEYS"] = False

# Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# Create Table
class Book(db.Model):
    __tablename__ = "library"
    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(250), nullable=False)
    authors = db.Column(MutableList.as_mutable(PickleType), default=[])
    published_date = db.Column(db.Integer,  nullable=False)
    categories = db.Column(MutableList.as_mutable(PickleType), default=[])
    average_rating = db.Column(db.Integer, nullable=True)
    ratings_count = db.Column(db.Integer, nullable=True)
    thumbnail = db.Column(db.String(250), nullable=True)

    def __repr__(self):
        return f"Book {self.title}, authors: {self.authors}, date: {self.published_date}," \
               f" categories: {self.categories}, avg_rating: {self.average_rating}," \
               f" ratings count: {self.ratings_count}, thumbnail: {self.thumbnail}"


# Run only once to create data base
db.create_all()


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/books')
def show_all_books():
    sort_by = request.args.get('sort_by')
    all_books = Book.query.order_by(sort_by)
    return render_template("all-books.html", books=all_books)


@app.route('/books/<int:bookid>')
def book_details(bookid):
    selected_book = Book.query.get(bookid)
    return jsonify(title=selected_book.title,
                   authors=selected_book.authors,
                   published_date=selected_book.published_date,
                   categories=selected_book.categories,
                   average_rating=selected_book.average_rating,
                   ratings_count=selected_book.ratings_count,
                   thumbnail=selected_book.thumbnail
                   )


@app.route('/random')
def random():
    selected_book = Book.query.order_by(func.random()).first()
    return jsonify(title=selected_book.title,
                   authors=selected_book.authors,
                   published_date=selected_book.published_date,
                   categories=selected_book.categories,
                   average_rating=selected_book.average_rating,
                   ratings_count=selected_book.ratings_count,
                   thumbnail=selected_book.thumbnail
                   )


# MAIN
if __name__ == "__main__":
    app.run(debug=True)
