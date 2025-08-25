#!/usr/bin/env python3
from app import create_app
from app.extensions import socketio

app = create_app()

if __name__ == '__main__':
    # debug=True solo si lo necesitas
    socketio.run(app, debug=True)
