import socket
import threading

from dotenv import load_dotenv
import os

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
      package = client.recv(1024)
      packages.append(package)

      end_flag = package[-10:]
      if(end_flag == 'endmessage'.encode()):
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
