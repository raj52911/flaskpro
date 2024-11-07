# config.py
import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///namma_kadai.db'  # Use SQLite; switch to MySQL if required
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.urandom(24)
