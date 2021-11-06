import os
import requests
from flask import Flask, render_template, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy import PickleType, func


app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get('SECRET_KEY')
# Generated from terminal: python -c "import secrets; print(secrets.token_urlsafe(32))"

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

    def to_dict(self):
        """Creat dictionary using given Model"""
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}


def get_new_books():
    lib_data = requests.get('https://www.googleapis.com/books/v1/volumes?q=Hobbit').json()['items']
    for item in lib_data:

        new_title = item['volumeInfo']['title']
        new_authors = item['volumeInfo']['authors']
        new_date = item['volumeInfo']['publishedDate']
        try:
            new_category = item['volumeInfo']['categories']
        except KeyError:
            new_category = []
        try:
            new_avg_rating = item['volumeInfo']['averageRating']
        except KeyError:
            new_avg_rating = 0
        try:
            new_rating_count = item['volumeInfo']['ratingsCount']
        except KeyError:
            new_rating_count = 0
        try:
            new_thumbnail = item['volumeInfo']['imageLinks']['thumbnail']
        except KeyError:
            new_thumbnail = ""

        new_book = Book(
            title=new_title,
            authors=new_authors,
            published_date=new_date,
            categories=new_category,
            average_rating=new_avg_rating,
            ratings_count=new_rating_count,
            thumbnail=new_thumbnail
        )
        print(new_book)
        db.session.add(new_book)
        db.session.commit()

# Run only once to create data base
db.create_all()


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/books')
def all_books():
    lib_data = requests.get('https://www.googleapis.com/books/v1/volumes?q=Hobbit').json()['items'][0]
    print(lib_data)
    get_new_books()
    return render_template("all-books.html", books=lib_data)

@app.route('/random')
def random():
    random_book = Book.query.order_by(func.random()).first()  # get random cafe from DB
    return jsonify(cafe=random_book.to_dict())

# MAIN
if __name__ == "__main__":
    app.run(debug=True)
