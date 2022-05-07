import sqlite3

import socket
import threading

from dotenv import load_dotenv
import os

import yaml

config_file = open("config.yaml", 'r')
config = yaml.safe_load(config_file)
config_sizes = config['sizes']
config_flags = config['flags']

load_dotenv()

clients = []
queue = []

def start():
  print('iniciado')
  HOST = ''
  PORT = int(os.getenv('port'))
  udp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  orig = (HOST, PORT)
  udp.bind(orig)
  udp.listen(5)

  while True:
    client, addr = udp.accept()
    print(f'conectado por {addr}')
    clients.append(client)
    threading.Thread(target=handle, args=[client]).start()

def handle(client):
  try:
    packages = []
    while True:
      msg_type = client.recv(config_sizes['type'])

      if(msg_type.decode() == config['register']):
        pass
      elif(msg_type.decode() == config['alter_password']):
        pass
      elif(msg_type.decode() == config['delete_user']):
        pass
      elif(msg_type.decode() == config['login']):
        pass
      elif(msg_type.decode() == config['logout']):
        pass
      else:
        package = client.recv(1024)
        packages.append(package)

        end_flag = package[-10:]
        if(end_flag == config_flags['end'].encode()):
          queue.append(packages)
          packages = []
          broadcast(client)

  except:
    print('sheesh')
    clients.remove(client)
    client.close()

def broadcast(client_sender):
  print('enviando para todos os clientes')
  for packages in queue:
    for package in packages:
      for client in clients:
        if(client == client_sender):
          continue

        client.send(package)
    queue.remove(packages)

start()
