# per the docs on flask-socketio, monkey_patching is required as the first step.
# https://flask-socketio.readthedocs.io/en/latest/#using-multiple-workers
# TODO: this crashes in debug
import eventlet
eventlet.monkey_patch()

from flask import Flask, render_template
from flask_socketio import SocketIO, join_room, emit, send
from flask import request, json, g
from flask_socketio import join_room, leave_room
import logging
import os
import redis
import time
import socketio as sio

app = Flask(__name__)
app.config['SECRET_KEY'] = 'TODO:ChangeThisSecret' 

redis_url = 'redis://localhost:6379'
queue = sio.RedisManager(redis_url, channel='socket.io#/#', write_only=False)
socketio = SocketIO(app, message_queue=redis_url, client_manager=queue, async_mode='eventlet', async_handlers=True)


if __name__ == '__main__':
    print(f'beginning py-emit')
    loop = 0
    while True:
        time.sleep(5)
        loop += 1
        payload = f'PY PING {loop}'
        socketio.emit('pinger', payload)
        print(payload)
