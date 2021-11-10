from flask import render_template, redirect, url_for, jsonify, request, Blueprint
from sqlalchemy import or_
from library_manager import get_new_books
from model import Book, db

library_app = Blueprint('library_app', __name__)


@library_app.route('/')
def home():
    return render_template("index.html")


@library_app.route('/books')
def show_all_books():
    """Shows all entries from DB. Route can get following arguments:
    sort_by - used to sort entries, in current application only sort by published date is implemented.
    authors - a list of authors, used to filter entries related to specific authors.
    published_date - used to filter entreis related to specific date. The date must be given in a specific format,
                     otherwise the user will be informed. Allowed parameter formats: YYYY-MM-DD, YYYY-MM, YYYY."""
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
            return jsonify(response=dict(failure=f"Date should have format: YYYY-MM-DD or YYYY-MM or YYYY"))
    else:
        all_books = Book.query.order_by(sort_by)
    return render_template("all-books.html", books=all_books)


@library_app.route('/books/<int:bookid>')
def book_details(bookid):
    """Shows book detials in JSON format."""
    selected_book = Book.query.get(bookid)
    return jsonify(title=selected_book.title,
                   authors=selected_book.authors,
                   published_date=selected_book.published_date,
                   categories=selected_book.categories,
                   average_rating=selected_book.average_rating,
                   ratings_count=selected_book.ratings_count,
                   thumbnail=selected_book.thumbnail
                   )


@library_app.route('/library', methods=['POST'])
def add_books():
    """Adds book to library. Required parameters:
    q - query to Google Books API.
    The user will be informed if a request is not fulfilled. (JSON massage)
    """
    download_link = 'https://www.googleapis.com/books/v1/volumes?q='
    if request.method == 'POST':
        query = request.form.get('q')
        link = download_link + query
        try:
            get_new_books(book=Book, link=link, db=db)
        except KeyError:
            return jsonify(response=dict(failure=f"Sorry we don't have {query} in our library :("))
    return redirect(url_for('library_app.show_all_books'))
