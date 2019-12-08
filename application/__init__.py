"""
The flask application package.
"""

from flask import Flask
import os
app = Flask(__name__)
app.static_folder = f"{os.path.dirname(__file__)}{os.path.sep}static"
import application.views
