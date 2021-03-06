from catalog import db
import random
import string
from flask_login import UserMixin
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer,
                          BadSignature, SignatureExpired)


class User(db.Model, UserMixin):
    """
    Registered user information is stored in db
    """
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), index=True)
    picture = db.Column(db.String)
    email = db.Column(db.String)
    token = db.column(db.text)
    items = db.relationship('Items', backref="user", uselist=True)
    


class Categories(db.Model):
    """
    Registered categories information is stored in db
    """
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), index=True)
    items = db.relationship('Items', backref="category", uselist=True)


class Items(db.Model):
    """
    Registered items information is stored in db
    """
    __tablename__ = 'items'

    name = db.Column(db.String(80), nullable=False)
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(250))
    categories_id = db.Column(db.Integer, db.ForeignKey(
	'categories.id', ondelete='CASCADE'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


