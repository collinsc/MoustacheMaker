"""
Routes and views for the flask application.
"""

from datetime import datetime

from flask import render_template
from flask import current_app as app
from flask_socketio import emit

from application import socketio


@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'index.html',
        title='Moustache Maker',
        year=datetime.now().year,
    )


@socketio.on('test', namespace='/video_feed')
def test_message(message):
    app.logger.debug(f"test message recieved: {message}")
    emit('message', {'data': message['data']})


@socketio.on('connect', namespace='/video_feed')
def test_connect():
    app.logger.debug("client connected")
    emit('message', {'data': 'Connected'})


@socketio.on('disconnect', namespace='/video_feed')
def test_disconnect():
    app.logger.debug('Client disconnected')
