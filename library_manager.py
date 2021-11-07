import requests
from sqlalchemy.exc import IntegrityError

def get_new_books(book, link, db):
    lib_data = requests.get(link).json()['items']

    for item in lib_data:
        new_authors = ""
        new_category = ""
        new_title = item['volumeInfo']['title']
        for author in item['volumeInfo']['authors']:
            new_authors = new_authors + author
        new_date = item['volumeInfo']['publishedDate']
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
        # book.query.filter_by(title=new_title).first()

