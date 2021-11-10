"""
Creates Table,
 __repr__ method was used for tests durning development, was left for future testing.
Model contains all infomration which was shown in book details example. There is one additional column date_to_disp
which is used to display date in original format.
"""

from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()


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
