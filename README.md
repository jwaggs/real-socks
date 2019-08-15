# real-socks

This repo was merely intended to be a POC for a micro-serviced realtime socket.io cloud architecture written in multiple languages.

The goal was to determine whether or not socket.io processes written with the original [node implementation](https://socket.io/) would end up being compatible
with socket.io processes written via the [flask-socketio](https://github.com/miguelgrinberg/Flask-SocketIO) port written in python.

In my attempts, I discovered that the message format of the redis queue pub/sub events are not compatible between these two socket.io implementations. Therefor, events emitted into the message queue via a
node socket.io process cannot be decoded by a python socket.io process. Similarly, flask-socketio processes do not currently emit messages in a compatible way for the node socket.io processes.

I learned via posting [this issue](https://github.com/miguelgrinberg/Flask-SocketIO/issues/1024) that the reason for this is simply: "the redis pub/sub format is not part of the Socket.IO protocol".
Had the message format been included in the socket.io protocol, my attempts to distribute messages across servers written in both environments would have been successful.
But instead the results unfortunately indicate that the different socket.io libraries don't use a compatible message format, and therefor do not work well together.

I would be curious to inquire why a standardized message format was not considered within the scope of the socket.io protocol, but such inquiries are outside of the scope of my own efforts, and therefor I will not be finishing this POC.

For anyone curious, you can get both of the provided node processes running via `npm install` then `node index.js`. To get both of the python environments up, just run `pip3 install -r requirements.txt` then `python3 app.py`. The node service runs on port 3000, python service runs on port 5000, they expect redis to be available on the default port 6379, and each service is using the redis channel `socket.io#/#` for it's pub/sub key.

To see the versions installed check the committed package-lock.json and requirements.txt files correspondingly. 
