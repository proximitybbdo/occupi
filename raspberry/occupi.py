#! /usr/bin/env python
# -*- coding: utf-8 -*-

from time import sleep, time
from multiprocessing import Process, Manager

import os
import socket
import json
import logging
import random
import RPi.GPIO as GPIO

server_ip = '0.0.0.0'
server_port = 2000
server_dest = (server_ip, server_port)

time_buffer = 30

class Logger:
  def __init__(self, message, sys=False):
    prefix = u'ە '.encode('utf-8') if sys else ''

    print '\033[94m' + prefix + message + '\033[0m'

def start_loop(in_pin, shared):
  in_room = False
  in_change = False
  last_time = time()

  while True:
    # new_check = bool(random.getrandbits(1))
    new_check = GPIO.input(in_pin) == GPIO.HIGH
    # print 'pin is ' + str(GPIO.input(in_pin))

    if new_check != in_room and not in_change:
      last_time = time()
      in_change = True

      print 'start state saving on ' + str(last_time)

    if new_check == in_room and in_room and in_change:
      last_time = time()

      print 'reset time change because our state is in_room'

    current_time = time()
    time_diff = current_time - last_time > time_buffer

    if new_check != in_room and time_diff and in_change:
      # print 'state is permanent on ' + str(current_time)

      in_room = new_check
      in_change = False

      shared.state = in_room

      if in_room:
        Logger('Somebody is in the meeting room!', True)
      else:
        Logger('Be quick! The meeting room is empty!', True)

    sleep(0.5)

def notify_state(state, client):
  answer = {'room_id': 1, 'occupied': 1 if state else 0}
  answer_formatted = json.dumps(answer).encode('utf-8')

  try:
    if client != None:
      client.sendall(answer_formatted)
  except:
    client.close()
    client = None

def handle_client(client, shared):
  current_state = shared.state

  notify_state(current_state, client)

  while True:
    new_state = shared.state

    if new_state != current_state:
      current_state = new_state

    notify_state(current_state, client)

    sleep(0.5)

def connect_server(server):
  global server_port, server_dest

  try:
    server.bind(server_dest)

    Logger('Server on port ' + json.dumps(server_port), True)
  except Exception as exc:
    server_port += 1
    server_dest = (server_ip, server_port)

    connect_server(server)

def start_server(shared):
  server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  server.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

  connect_server(server)

  server.listen(1)

  clients = []

  try:
    while True:
      client, address = server.accept()

      Logger('Got connection from ' + json.dumps(address), True)

      p = Process(target=handle_client, args=(client, shared))
      p.daemon = True
      p.start()

      clients.append(p)
  except KeyboardInterrupt:
    Logger('Server loop keyboard interrupt', True)

    for client in clients:
      client.terminate()
      client.join()

def main():
  manager = Manager()

  shared = manager.Namespace()
  shared.state = False

  in_pin = 17 # GEN 0

  GPIO.setmode(GPIO.BCM)
  GPIO.setup(in_pin, GPIO.IN)

  try:
    p_server = Process(target=start_server, args=(shared,))
    p_gpio = Process(target=start_loop, args=(in_pin, shared))

    p_server.start()
    p_gpio.start()

    p_server.join()
    p_gpio.join()
  except:
    Logger('Unexpected exception', True)
    Logger('Closing', True)

    p_server.terminate()
    p_gpio.terminate()

    p_server.join()
    p_gpio.join()

if __name__ == '__main__':
  main()
