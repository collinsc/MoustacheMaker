"""
The flask application package.
"""

from flask import Flask
from flask_session import Session
import os
app = Flask(__name__)
app.static_folder = f"{os.path.dirname(__file__)}{os.path.sep}static"
SESSION_TYPE = "filesystem"
SESSION_PERMANENT = False
Session(app)

import application.views
