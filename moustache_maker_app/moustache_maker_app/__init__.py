"""
The flask application package.
"""

from flask import Flask
app = Flask(__name__)

import moustache_maker_app.views
