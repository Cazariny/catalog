from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine
import random
import string
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer,
                          BadSignature, SignatureExpired)

Base = declarative_base()
secret_key = ''.join(random.choice(string.ascii_uppercase + string.digits)
                     for x in xrange(32))


class User(Base):
    """
    Registered user information is stored in db
    """
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    username = Column(String(50), index=True)
    picture = Column(String)
    email = Column(String)

    @staticmethod
    def verify_auth_token(token):
        """
         Gets a token for the user login
        """
        s = Serializer(secret_key)
        try:
            data = s.loads(token)
        except SignatureExpired:
            # Valid Token, but expired
            return None
        except BadSignature:
            # Invalid Token
            return None
        user_id = data['id']
        return user_id


class Categories(Base):
    """
    Registered categories information is stored in db
    """
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    name = Column(String(40), index=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User, cascade="delete")

    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
            'id': self.id,
            'name': self.name,
        }


class Items(Base):
    """
    Registered items information is stored in db
    """
    __tablename__ = 'items'

    name = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
    description = Column(String(250))
    categories_id = Column(Integer, ForeignKey('categories.id'))
    categories = relationship(Categories, cascade="delete")
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User, cascade="delete")

    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
            'name': self.name,
            'description': self.description,
            'id': self.id,
        }


engine = create_engine('sqlite:///catalog.db')

Base.metadata.create_all(engine)
