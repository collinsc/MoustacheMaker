"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template, Response
from application import app
from application.streaming_loop import Streamer


@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'index.html',
        title='Moustache Maker',
        year=datetime.now().year,
    )


@app.route('/video_feed')
def video_feed():
    streamer = Streamer()
    return Response(streamer.loop(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
