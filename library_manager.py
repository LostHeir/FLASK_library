"""
Creates new set of books based on user's query.
Function is called in route: add_books with POST method.
"""

import requests
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy


def get_new_books(book, link: str, db: SQLAlchemy) -> None:
    """
    Passes the query to the Google Book API, retrieves the necessary parameters spiecified in book detial section.
    So many try-except are used, due to the incompleteness of the data received from the API.
    :param book: A Book model, which is used in DB.
    :param link: Link used with GET method to pass query to Google Book API.
    :param db:  SQLAlchemy DataBase.
    :return: None.
    """
    lib_data = requests.get(link).json()['items']

    for item in lib_data:
        new_authors = ""
        new_category = ""
        new_title = item['volumeInfo']['title']
        try:
            for author in item['volumeInfo']['authors']:
                new_authors = new_authors + ',' + author
            new_authors = new_authors[1:]
        except KeyError:
            new_authors = ""
        try:
            new_date = datetime.strptime(item['volumeInfo']['publishedDate'], '%Y-%m-%d').date()
            new_date_disp = 'd'
        except ValueError:
            try:
                new_date = datetime.strptime(item['volumeInfo']['publishedDate'], '%Y-%m').date()
                new_date_disp = 'm'
            except ValueError:
                new_date = datetime.strptime(item['volumeInfo']['publishedDate'], '%Y').date()
                new_date_disp = 'y'
        try:
            for category in item['volumeInfo']['categories']:
                new_category = new_category + category
        except KeyError:
            new_category = ""
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

        new_book = book(
            title=new_title,
            authors=new_authors,
            published_date=new_date,
            date_to_disp=new_date_disp,
            categories=new_category,
            average_rating=new_avg_rating,
            ratings_count=new_rating_count,
            thumbnail=new_thumbnail
        )
        book_exists = book.query.filter_by(title=new_title, authors=new_authors).first()
        if book_exists:
            setattr(book_exists, 'title', new_book.title)
            setattr(book_exists, 'authors', new_book.authors)
            setattr(book_exists, 'published_date', new_book.published_date)
            setattr(book_exists, 'categories', new_book.categories)
            setattr(book_exists, 'average_rating', new_book.average_rating)
            setattr(book_exists, 'ratings_count', new_book.ratings_count)
            setattr(book_exists, 'thumbnail', new_book.thumbnail)
            db.session.commit()
        else:
            db.session.add(new_book)
            db.session.commit()
