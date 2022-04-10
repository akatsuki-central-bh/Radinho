import socket

def start():
  print('iniciado')
  HOST = ''
  PORT = 5000
  # with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as udp:
  udp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  orig = (HOST, PORT)
  udp.bind(orig)
  udp.listen(5)

  while True:
    conn, addr = udp.accept()
    print(f"conectado por {addr}")
    # msg, cliente = udp.recvfrom(1024)
    data = conn.recv(1024)
    if not data:
      break

    file_size = len(data)
    while(data):
      print(f'sending data: {file_size}')
      conn.sendall(data)
      data = conn.recv(1024)
      file_size += len(data)

    print('data sended')
    udp.shutdown(socket.SHUT_WR)
    udp.close()

start()
