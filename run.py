from flaskproject import app
# from flask import Blueprint
from flaskproject.routes import socketio

if __name__ == '__main__':
    socketio.run(app, debug=True)
