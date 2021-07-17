import os

SECRET_KEY = os.urandom(24)
STATIC_FOLDER = f"{os.path.dirname(__file__)}{os.path.sep}static"
SQLALCHEMY_DATABASE_URI = f"sqlite:///app.db"
SQLALCHEMY_TRACK_MODIFICATIONS = False
