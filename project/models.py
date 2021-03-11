from project import Base
from datetime import datetime
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime


class User(Base):
    __tablename__ = 'User'
    id = Column(Integer, primary_key=True)
    email = Column(String(120), unique=True, nullable=False)
    username = Column(String(80), unique=True, nullable=False)
    password = Column(String(64), nullable=False)

    def __init__(self, email=None, username=None, passwd=None):
        self.email = email
        self.username = username
        self.password = passwd

    def __repr__(self):
        return f'<User {self.id}>'


class Posts(Base):
    __tablename__ = 'Posts'
    id = Column(Integer, primary_key=True)
    author_id = Column(Integer, ForeignKey('User.id'))
    title = Column(String(120), nullable=False)
    content = Column(String(1000), nullable=False)
    publication_datetime = Column(DateTime, default=datetime.utcnow())

    def __init__(self, author_id=None, title=None, content=None):
        self.author_id = author_id
        self.title = title
        self.content = content

    def __repr__(self):
        return f'<User {self.id}>'


class Comments(Base):
    __tablename__ = 'Comments'
    id = Column(Integer, primary_key=True)
    post_id = Column(Integer, ForeignKey('Posts.id'))
    author_id = Column(Integer, ForeignKey('User.id'))
    title = Column(String(120), nullable=False)
    content = Column(String(1000), nullable=False)
    publication_datetime = Column(DateTime, default=datetime.utcnow())

    def __repr__(self):
        return f'<User {self.id}>'
