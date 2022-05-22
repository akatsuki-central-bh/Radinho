import os
import socket
import yaml
from dotenv import load_dotenv

load_dotenv()

config_file = open("config.yaml", 'r')
config = yaml.safe_load(config_file)
config_sizes = config['sizes']
message_types = config['message_types']
config_flags = config['flags']

def connect():
  HOST = str(os.getenv('host'))
  PORT = int(os.getenv('port'))

  dest = (HOST, PORT)

  conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  conn.connect(dest)

  return conn

def login(socket, username, password):
  username = username.ljust(config_sizes['username'], ' ')
  password = password.ljust(config_sizes['password'], ' ')

  socket.send(f"{message_types['login']}{username}{password}".encode())

  response = socket.recv(config_sizes['type']).decode()
  if response == config_flags['token']:
    return socket.recv(config_sizes['token'])


def register(socket, username, password):
  username = username.ljust(config_sizes['username'], ' ')
  password = password.ljust(config_sizes['password'], ' ')

  socket.send(f"{message_types['register']}{username}{password}".encode())

  response = socket.recv(config_sizes['type']).decode()
  return response == config_flags['success']

def logout(socket, token):
  socket.send(f"{message_types['logout']}{token}".encode())
