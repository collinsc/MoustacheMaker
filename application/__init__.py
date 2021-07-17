"""
The flask application package.
"""
import os
from datetime import datetime


from flask import Flask
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
import eventlet

eventlet.monkey_patch()


db = SQLAlchemy()

socketio = SocketIO()


def create_app():
    """Construct the core application."""
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_pyfile('config.py')
    db.init_app(app)
    app.app_context().push()

    # Imports
    import application.views
    # Create tables for our models
    db.create_all()

    socketio.init_app(app)
    from application.sqlalchemy_log_handler import SQLAlchemyHandler
    sql_handler = SQLAlchemyHandler()
    app.logger.addHandler(sql_handler)
    app.logger.info(f"Server booted: {datetime.now()}")


    return app