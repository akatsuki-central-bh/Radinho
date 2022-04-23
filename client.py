from tkinter import *
from tkinter import ttk
from tkinter import simpledialog

from dotenv import load_dotenv
import os

load_dotenv()

import threading

import socket

HOST = 'localhost'
PORT = int(os.getenv('port'))

udp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

dest = (HOST, PORT)
udp.connect(dest)

TYPE_SIZE = 4
AUTHOR_SIZE = 20
FILE_NAME_SIZE = 30

root = Tk()
frm = ttk.Frame(root, padding=10)
frm.grid()
ttk.Label(frm, text='Chat dos menores').grid(column=0, row=0)

text_area = Text(frm, height = 20, width = 50)
text_area.grid(column=0, row=1, columnspan=3)

text_input = Text(frm, height = 1, width = 25)
text_input.grid(column=0, row=2)

ttk.Button(frm, text='enviar', command = lambda:send_message()).grid(column=1, row=2)
ttk.Button(frm, text='Anexar arquivo', command = lambda:send_file()).grid(column=2, row=2)

author = simpledialog.askstring('username', 'digite seu nome', parent=root)
author = author.ljust(AUTHOR_SIZE, ' ')

def send_message():
  try:
    INPUT = text_input.get('1.0', 'end-1c')
    udp.send(f'mesg{author}{INPUT}'.encode())
    udp.send('end'.encode())
  except BrokenPipeError as e:
    print(e)

def send_file():
  file_name = 'arquivo.docx'
  file = open(file_name, 'rb')
  file_name_ljust = file_name.ljust(30, ' ')

  udp.send(f'file{author}{file_name_ljust}'.encode())
  data = file.read(1024)

  message_size = len(data)
  while(data):
    print(f'sending data: {message_size}')
    udp.send(data)
    data = file.read(1024)
    message_size += len(data)

  udp.send('end'.encode())
  file.close()

  print('Done Sending')

def listen():
  while True:
    msg_type = udp.recv(TYPE_SIZE).decode()
    msg_author = udp.recv(AUTHOR_SIZE).decode()

    file = None
    if(msg_type == 'file'):
      file_name = udp.recv(FILE_NAME_SIZE).decode().rstrip()
      file = open(f'download/{file_name}', 'wb')

    data = udp.recv(1024)
    response = data

    while(data):
      end_flag = data[-3:]
      if(end_flag == b'end'):
        break

      data = udp.recv(1024)
      response += data

    print(f'type: {msg_type}, author: {msg_author}')

    if(msg_type == 'mesg'):
      text_area.insert(END, f'{msg_author.rstrip()}: {response.decode()[:-3]}\n')
    elif(msg_type == 'file'):
      print(f'file size: {len(response[:-3])}')
      file.write(response[:-3])
      file.close()
      # pass
    print('message received')

threading.Thread(target=listen, args=[]).start()
root.mainloop()
