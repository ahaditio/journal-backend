from os import environ
from Journal import app, socketio

socketio.run(app, host='0.0.0.0', port=5008, debug=True)
