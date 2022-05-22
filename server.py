import socket
import threading
import database

from dotenv import load_dotenv
import os

import yaml

config_file = open("config.yaml", 'r')
config = yaml.safe_load(config_file)
config_sizes = config['sizes']
message_types = config['message_types']
config_flags = config['flags']

database.create_database()
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
    while True:
      msg_type = client.recv(config_sizes['type'])
      msg_type = msg_type.decode()
      default_flow(msg_type, client)
  except:
    print('sheesh')
    clients.remove(client)
    client.close()

def default_flow(msg_type, client):
  token = client.recv(config_sizes['token']).decode()
  author = database.get_username(token)
  author = author.ljust(config_sizes['username'], ' ').encode()

  packages = [msg_type.encode(), author]

  while(True):
    package = client.recv(1024)
    packages.append(package)

    end_flag = package[-10:]
    if(end_flag == config_flags['end'].encode()):
      queue.append(packages)
      broadcast(client)
      break

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
