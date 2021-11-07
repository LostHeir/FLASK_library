import requests


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
        db.session.add(new_book)
        db.session.commit()
