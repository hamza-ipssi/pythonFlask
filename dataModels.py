from sqlalchemy import Column, Boolean, String, Integer, Numeric
from config import getBase

base = getBase()

class User(base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    username = Column(String(16), unique=True, nullable=False)
    email = Column(String(16), unique=True, nullable=False)

class Tweet(base):
    __tablename__ = "tweet"
    id = Column(Integer, primary_key=True)
    username = Column(String(16), unique=False, nullable=False)
    tweetText = Column(String(255), unique=False, nullable=False)