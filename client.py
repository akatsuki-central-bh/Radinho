from tkinter import *
from tkinter import ttk
from tkinter import simpledialog
from tkinter import filedialog

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
FILE_NAME_SIZE = 2000

root = Tk()
frm = ttk.Frame(root, padding=10)
frm.grid()
ttk.Label(frm, text='Chat dos menores').grid(column=0, row=0)

text_area = Text(frm, height = 20, width = 50)
text_area.grid(column=0, row=1, columnspan=3)

text_input = Text(frm, height = 1, width = 25)
text_input.grid(column=0, row=2)

ttk.Button(frm, text='enviar', command = lambda:send_message()).grid(column=1, row=2)
ttk.Button(frm, text='Anexar arquivo', command = lambda:select_files()).grid(column=2, row=2)

author = simpledialog.askstring('username', 'digite seu nome', parent=root)
author = author.ljust(AUTHOR_SIZE, ' ')

def send_message():
  try:
    input = text_input.get('1.0', 'end-1c')
    text_area.insert(END, f'você: {input}\n')
    udp.send(f'mesg{author}{input}'.encode())
    udp.send('end'.encode())
  except BrokenPipeError as e:
    print(e)

def select_files():
  filetypes = (
    ('All files', '*.*'),
    ('text files', '*.txt')
  )

  path_name = filedialog.askopenfilename(
    title='Open files',
    initialdir='/',
    filetypes=filetypes)

  file_name = os.path.basename(path_name)
  file = open(path_name, 'rb')

  file_name_ljust = file_name.ljust(FILE_NAME_SIZE, ' ')

  udp.send(f'file{author}{file_name_ljust}'.encode())
  package = file.read(1024)

  message_size = len(package)
  while(package):
    udp.send(package)
    package = file.read(1024)
    message_size += len(package)

  print(f'sended package: {message_size}')
  udp.send('end'.encode())
  file.close()

  text_area.insert(END, f'você: {file_name} enviado\n')
  print('Done Sending')

def listen():
  while True:
    msg_type = udp.recv(TYPE_SIZE).decode()
    msg_author = udp.recv(AUTHOR_SIZE).decode().rstrip()

    if(msg_type == 'mesg'):
      read_message(msg_author)
    elif(msg_type == 'file'):
      save_file(msg_author)

def read_message(msg_author):
  content = read_content()
  text_area.insert(END, f'{msg_author}: {content.decode()}\n')

def save_file(msg_author):
  file_name = udp.recv(FILE_NAME_SIZE).decode().rstrip()
  file = open(f'download/{file_name}', 'wb')
  content = read_content()

  print(f'file size: {len(content)}')
  file.write(content)
  file.close()
  text_area.insert(END, f'{msg_author} enviou um arquivo: {file_name}\n')

def read_content():
  package = udp.recv(1024)
  response = package
  print(package)

  while(True):
    end_flag = package[-3:]
    if(end_flag == b'end'):
      break

    if(len(package) < 1024):
      print(package)
    package = udp.recv(1024)
    print(len(package))
    response += package

  return response[:-3]

threading.Thread(target=listen, args=[]).start()
root.mainloop()
