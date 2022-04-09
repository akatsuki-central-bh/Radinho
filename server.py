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

  conn, addr = udp.accept()
  while True:
    print(f"conectado por {addr}")
    # msg, cliente = udp.recvfrom(1024)
    data = conn.recv(1024)
    conn.sendall(data)

start()
