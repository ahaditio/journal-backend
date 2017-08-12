"""
This script runs the Sparse application using a development server.
"""

from os import environ
from Journal import app, socketio

#if __name__ == '__main__':
#    HOST = environ.get('SERVER_HOST', 'localhost')
#    try:
#        PORT = int(environ.get('SERVER_PORT', '5555'))
#    except ValueError:
#        PORT = 5555
#    app.run(HOST, PORT)

socketio.run(app, host='0.0.0.0', port=5008, debug=True)
