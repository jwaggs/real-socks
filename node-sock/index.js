var app = require('express')();
var http = require('http').createServer(app);
const io = require('socket.io')(http);
const redis = require('socket.io-redis');
io.adapter(redis({ host: 'localhost', port: 6379 }));

app.get('/', function(req, res){
  res.sendFile(__dirname + '/index.html');
});

io.on('connection', function(socket){
  console.log('a user connected');
  socket.broadcast.emit('hi');
  socket.on('disconnect', function(){
    console.log('user disconnected');
  });

  socket.on('chat message', function(msg){
    console.log('msg: ', msg);
    io.emit('chat message', msg);
  });

  socket.on('pinger', function(msg){
    console.log('ping: ', msg);
    io.emit('chat message', msg);
  });
});

io.on('pinger', function(socket){
    console.log('pinger');
});

http.listen(3000, function(){
  console.log('listening on *:3000');
});
