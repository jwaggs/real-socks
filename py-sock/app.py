# per the docs on flask-socketio, monkey_patching is required as the first step when balancing between multiple servers via redis
# https://flask-socketio.readthedocs.io/en/latest/#using-multiple-workers
# TODO: this crashes in debug
import eventlet
eventlet.monkey_patch()

from flask import Flask, render_template
from flask_socketio import SocketIO, join_room, emit, send, leave_room
import logging
import os
import pickle
import socketio as sio


app = Flask(__name__)
app.config['SECRET_KEY'] = 'TODO:ChangeThisSecret'  # TODO: change
redis_url = 'redis://localhost:6379'
queue = sio.RedisManager(redis_url, channel='socket.io#/#', write_only=False)
socketio = SocketIO(app, message_queue=os.getenv('REDIS_URL'), client_manager=queue, async_mode='eventlet', async_handlers=True)
print(f'initialized app with redis url: {redis_url}')


@app.route('/')
def index():
    """Serve the index HTML"""
    return render_template('index.html')


@socketio.on('connect')
def test_connect():
    print('Client connected')
    emit('my response', {'data': 'Connected'})


@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')


@socketio.on('pinger')
def on_ping(data):
    print(f'server received ping: {data}')
    emit('pinger', data, broadcast=True)


if __name__ == '__main__':
    host, port = '0.0.0.0', 5000
    print(f'running on host: {host} port: {5000}')
    socketio.run(app, host=host, port=port, debug=True)
