import os
from flask import Flask, render_template, redirect, url_for, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_
from library_manager import get_new_books

DOWNLOAD_LINK = 'https://www.googleapis.com/books/v1/volumes?q='

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
    authors = db.Column(db.String(250), nullable=False)
    published_date = db.Column(db.Date,  nullable=False)
    date_to_disp = db.Column(db.String(1), nullable=True)
    categories = db.Column(db.String(250), nullable=False)
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
    sort_by = request.args.get('sort_by', None)
    authors = request.args.getlist('author')
    published_date = request.args.get('published_date', None)
    if authors:
        try:
            all_books = Book.query.filter(or_(Book.authors == authors[0], Book.authors == authors[1]))
        except IndexError:
            all_books = Book.query.filter(Book.authors == authors[0])
    elif published_date:
        published_date = published_date.split('-')
        if len(published_date) == 1:
            date_max = published_date[0] + "-12"
            date_min = published_date[0] + "-01"
            all_books = Book.query.filter(Book.published_date >= date_min, Book.published_date < date_max)
        elif len(published_date) == 2:
            month_max = str(int(published_date[1]) + 1)
            date_max = published_date
            date_filter = '-'.join(published_date)
            date_max[1] = month_max
            date_max_filter = '-'.join(date_max)
            all_books = Book.query.filter(Book.published_date >= date_filter, Book.published_date < date_max_filter)
        elif len(published_date) == 3:
            published_date = '-'.join(published_date)
            all_books = Book.query.filter_by(published_date=published_date)
        else:
            return jsonify(response=dict(failure=f"Date should be in format XXXX-XX-XX"))
    else:
        all_books = Book.query.order_by(sort_by)
        print(type(all_books))
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


@app.route('/library', methods=['POST'])
def add_books():
    if request.method == 'POST':
        query = request.form.get('q')
        link = DOWNLOAD_LINK + query
        try:
            get_new_books(book=Book, link=link, db=db)
        except KeyError:
            return jsonify(response=dict(failure=f"Sorry we don't have {query} in our library :("))
    return redirect(url_for('show_all_books'))


# MAIN
if __name__ == "__main__":
    app.run(debug=True)
