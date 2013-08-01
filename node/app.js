// Generated by CoffeeScript 1.6.3
(function() {
  var app, host, io, io_socket, net, port, sensor, sensor_data, server;

  app = require('express')();

  net = require('net');

  host = '127.0.0.1';

  port = 2000;

  io_socket = null;

  sensor_data = {};

  sensor = net.connect({
    port: port,
    host: host
  }, function() {
    return true;
  });

  sensor.on('data', function(data) {
    sensor_data = data.toString();
    if (io_socket != null) {
      io.sockets.emit('status', sensor_data);
    }
    return sensor.end();
  });

  sensor.on('end', function() {
    return console.log('client disconnected');
  });

  sensor.on('error', function() {
    return console.log('sensor connection error');
  });

  server = require('http').createServer(app);

  io = require('socket.io').listen(server);

  io.enable('browser client minification');

  io.enable('browser client etag');

  io.enable('browser client gzip');

  io.set('log level', 1);

  server.listen(3000);

  app.get('/', function(req, res) {
    return res.sendfile(__dirname + '/views/index.html');
  });

  io.sockets.on('connection', function(socket) {
    io_socket = socket;
    io_socket.emit('status', sensor_data);
    return io_socket.on('eror', function(data) {
      console.log('error');
      return console.log(data);
    });
  });

}).call(this);
