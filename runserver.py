"""
This script runs the MoustacheMakerApplication application using a
development server.
"""

from os import environ
from application import create_app, socketio
app = create_app()


if __name__ == '__main__':
    HOST = environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    socketio.run(HOST, PORT)
