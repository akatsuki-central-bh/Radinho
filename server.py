import socket
import threading

from dotenv import load_dotenv
import os

load_dotenv()
clients = []

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
      data = client.recv(1024)
      broadcast(data)
  except:
    clients.remove(client)
    client.close()

def broadcast(message):
  for client in clients:
    client.send(message)

start()
