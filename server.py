import socket
import threading
import connector

from dotenv import load_dotenv
import os

import yaml

config_file = open("config.yaml", 'r')
config = yaml.safe_load(config_file)
config_sizes = config['sizes']
message_types = config['message_types']
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
    while True:
      msg_type = client.recv(config_sizes['type'])
      msg_type = msg_type.decode()

      if(msg_type == message_types['register']):
        register(client)
      elif(msg_type == message_types['alter_password']):
        alter_password(client)
      elif(msg_type == message_types['login']):
        login(client)
      elif(msg_type == message_types['logout']):
        logout(client)
      else:
        default_flow(msg_type, client)
  except:
    print('sheesh')
    clients.remove(client)
    client.close()

def register(client):
  username = client.recv(config_sizes['username'])
  password = client.recv(config_sizes['password'])
  connector.create_user(username, password)

  client.send(message_types['success'].encode())
def alter_password(client):
  token = client.recv(config_sizes['token'])
  new_password = client.recv(config_sizes['password'])
  current_password = client.recv(config_sizes['password'])
  connector.alter_password(token, new_password, current_password)

  client.send(message_types['success'].encode())
def login(client):
  username = client.recv(config_sizes['username'])
  password = client.recv(config_sizes['password'])
  token = connector.login(username, password)

  success_message = config_flags['token'] + token + config_flags['end']
  client.send(success_message.encode())

def logout(client):
  token = client.recv(config_sizes['token'])
  connector.logout(token)

def default_flow(msg_type, client):
  packages = [msg_type]

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
