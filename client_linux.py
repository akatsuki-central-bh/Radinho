from tkinter import *
from tkinter import ttk

import threading

import socket
from tkinter import simpledialog

HOST = 'localhost'
PORT = 5006

udp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

dest = (HOST, PORT)
udp.connect(dest)

TYPE_SIZE = 4
AUTHOR_SIZE = 20
FILE_NAME_SIZE = 30

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

author = simpledialog.askstring('username', 'digite seu nome', parent=root)
author = author.ljust(AUTHOR_SIZE, ' ')

def send_message():
  try:
    udp.settimeout(10)
    INPUT = text_input.get("1.0", "end-1c")
    udp.send(f"mesg{author}{INPUT}".encode())
    udp.shutdown(socket.SHUT_WR)
  except BrokenPipeError as e:
    print(e)

def send_file():
  file_name = "arquivo.docx"
  file = open(file_name, "rb")
  file_name_ljust = file_name.ljust(30, ' ')

  udp.send(f'file{author}{file_name_ljust}'.encode())
  data = file.read(1024)

  message_size = len(data)
  while(data):
    print(f'sending data: {message_size}')
    udp.send(data)
    data = file.read(1024)
    message_size += len(data)
  file.close()

  print("Done Sending")
  udp.shutdown(socket.SHUT_WR)

def listen():
  while True:
    msg_type = udp.recv(TYPE_SIZE).decode()
    msg_author = udp.recv(AUTHOR_SIZE).decode()

    # if not msg or msg_author == author:
    if not msg_type:
      continue

    print(f'type: {msg_type}, author: {msg_author}')

    if(msg_type == 'mesg'):
      read_message(msg_author)
    elif(msg_type == 'file'):
      save_file(msg_author)
    elif msg_author == author:
      print('udp closed')
      # pass
    print('message received')


def read_message(author):
  text_area.insert(END, f"{author.rstrip()}: ")

  data = udp.recv(1024)
  message_size = len(data)

  while(message_size > 0):
    print(f'receiving data: {message_size}')
    text_area.insert(END, data)

    data = udp.recv(1024)
    message_size = len(data)
    print(f'receiving data: {message_size}')

  text_area.insert(END, "\n")

def save_file(author):
  file_name = udp.recv(FILE_NAME_SIZE).decode().rstrip()
  file = open(f"download/{file_name}", 'wb')

  data = udp.recv(1024)
  message_size = len(data)
  while(message_size > 0):
    print(f'receiving data: {message_size}')
    file.write(data)
    data = udp.recv(1024)
    message_size = len(data)

  file.close()
  text_area.insert(END, f"{author.rstrip()}: new file\n")

threading.Thread(target=listen, args=[]).start()
root.mainloop()
