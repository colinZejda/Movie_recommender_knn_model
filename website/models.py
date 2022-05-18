# purpose: to store our databaes models

from . import db          # import db object from current package (website folder)
from flask_login import UserMixin
from sqlalchemy.sql import func    # sql alchemy will take care of date/time for each Movie object in the datetime field

class Recommended(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    found_title = db.Column(db.String(1000))
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class IMDB_top_10(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

# class user inherits from UserMixin as well as our database object in __init__.py, and creates columns for each thing below
    # id, email, password, 1st name, notes
    # all users will look like this in the database:
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True) # email must be unique, 2 accounts cannot share same email
    password = db.Column(db.String(150))           # max size = 150 char
    first_name = db.Column(db.String(150))
    notes = db.relationship('Note')
    recommended = db.relationship('Recommended')
    imdb_top_10 = db.relationship('IMDB_top_10')
