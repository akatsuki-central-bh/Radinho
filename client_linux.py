from tkinter import *
from tkinter import ttk

import threading

import socket

HOST = 'localhost'
PORT = 5002

udp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
author = 'leandro'.ljust(20, ' ')

dest = (HOST, PORT)
udp.connect(dest)

def send_message():
  INPUT = text_input.get("1.0", "end-1c")
  udp.send(f"mesg{author}{INPUT}".encode())
  # udp.shutdown(socket.SHUT_WR)

def send_file():
  file_name = "arquivo.docx"
  file = open(file_name, "rb")
  file_name_ljust = file_name.ljust(30, ' ')

  udp.send(f'file{author}{file_name_ljust}'.encode())
  data = file.read(1024)

  file_size = len(data)
  while(data):
    print(f'sending data: {file_size}')
    udp.send(data)
    data = file.read(1024)
    file_size += len(data)
  file.close()

  print("Done Sending")
  # udp.shutdown(socket.SHUT_WR)

def listen():
  while True:
    msg, client = udp.recvfrom(24)
    msg = msg.decode()

    msg_type = msg[0:4]
    msg_author = msg[4:24].rstrip()

    # if not msg or msg_author == author:
    if not msg:
      break

    if(msg_type == 'mesg'):
      read_message(msg_author)
    else:
      save_file(msg_author)

def read_message(author):
  text_area.insert(END, f"{author}: ")
  data = udp.recv(1024)
  while (data):
    text_area.insert(END, data)
    data = udp.recv(1024)
  text_area.insert(END, "\n")


def save_file(author):
  file_name = udp.recv(14).decode()
  # file_size = udp.recv(6)

  data = udp.recv(1024)
  file = open(file_name.rstrip(), 'wb')

  file_size = len(data)
  while (data):
    print(f'receiving data: {file_size}')
    file.write(data)
    file_size += len(data)
    data = udp.recv(1024)

  breakpoint()
  text_area.insert(END, f"{author}: new file\n")

  file.close()

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
# ttk.Button(frm, text="Baixar arquivo", command = lambda:save_file('receive2.docx')).grid(column=3, row=2)

threading.Thread(target=listen, args=[]).start()
root.mainloop()
