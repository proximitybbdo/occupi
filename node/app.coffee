## python socket listener

app = require('express')()
net = require 'net'

host = 'localhost'
port = 2000

io_socket = null

sensor_data = {}

sensor = net.connect {port: port, host: host}, ->
  return true

sensor.on 'data', (data) ->
  sensor_data = data.toString()

  io.sockets.emit 'status', sensor_data if io_socket?

  client.end()

client.on 'end', ->
  console.log('client disconnected')

client.on 'error', ->
  console.log 'sensor connection error'

## app

server = require('http').createServer(app)
io = require('socket.io').listen(server)

server.listen 3000

app.get '/', (req, res) ->
  res.sendfile(__dirname + '/views/index.html')

## socket.io

io.sockets.on 'connection', (socket) ->
  io_socket = socket
  io_socket.emit 'status', sensor_data

  io_socket.on 'eror', (data) ->
    console.log 'error'
    console.log data
