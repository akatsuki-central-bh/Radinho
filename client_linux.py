import socket
HOST = '192.168.1.255'  # Endereco IP do Servidor
PORT = 5000            # Porta que o Servidor esta

udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
breakpoint()

dest = (HOST, PORT)
print('Conectado\n')

msg = 'leanddro conectado..'

while True:
  udp.sendto (msg.encode(), dest)
  msg = input()
