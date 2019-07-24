var io = require('socket.io-emitter')({ host: '127.0.0.1', port: 6379});
var loop = 0;
console.log('beginning node-emit')
setInterval(function(){
  loop = loop + 1;
  // data = { ping: loop }
  data = 'NODE PING ' + loop
  io.emit('pinger', data);
  console.log(data);
}, 5000);