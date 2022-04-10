from tkinter import *
from tkinter import ttk

import threading

import socket

HOST = 'localhost'  # Endereco IP do Servidor
PORT = 5000            # Porta que o Servidor esta

udp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# udp.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
username = 'leandro'

dest = (HOST, PORT)
udp.connect(dest)

def send_message():
  INPUT = text_input.get("1.0", "end-1c")
  udp.send(f"{username}: {INPUT}".encode())

def send_file():
  file = open("arquivo.docx", "rb")
  data = file.read()
  file.close()
  encoded = base64.b64encode(data)

  print("Sending...")
  print(f"base64: {encoded}")
  udp.send(encoded)

def listen():
  while True:
    msg, cliente = udp.recvfrom(1024)
    text_area.insert(END, f"{msg.decode()}\n")

root = Tk()
frm = ttk.Frame(root, padding=10)
frm.grid()
ttk.Label(frm, text="Chat dos menores").grid(column=0, row=0)

text_area = Text(frm, height = 20, width = 50)
text_area.grid(column=0, row=1, columnspan=3)

text_input = Text(frm, height = 1, width = 25)
text_input.grid(column=0, row=2)

ttk.Button(frm, text="enviar", command = lambda:send_message()).grid(column=1, row=2)
ttk.Button(frm, text="Anexar arquivo", command = lambda:send_file()).grid(column=2, row=2)

threading.Thread(target=listen, args=[]).start()
root.mainloop()
