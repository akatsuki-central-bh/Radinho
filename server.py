import socket
import threading

clients = []

def start():
  print('iniciado')
  HOST = ''
  PORT = 5006
  udp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  orig = (HOST, PORT)
  udp.bind(orig)
  udp.listen(5)

  while True:
    client, addr = udp.accept()
    print(f"conectado por {addr}")
    clients.append(client)
    threading.Thread(target=handle, args=[client]).start()

def handle(client):
  try:
    data = client.recv(1024)

    message_size = len(data)
    while(message_size > 0):
      print(f'sending data: {message_size}')
      broadcast(data)
      data = client.recv(1024)
      message_size = len(data)

    print('data sended')
    client.shutdown(socket.SHUT_WR)
  except:
    clients.remove(client)
    client.close()

def broadcast(message):
  for client in clients:
    client.send(message)

start()
