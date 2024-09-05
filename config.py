import os

class Config:
    SECRET_KEY = os.urandom(24)
    SQLALCHEMY_DATABASE_URI = 'mysql://kida:Kid(79542)@localhost/test'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
