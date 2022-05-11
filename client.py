from tkinter import *
from tkinter import ttk
from tkinter import simpledialog
from tkinter import filedialog

from dotenv import load_dotenv
import yaml
import os

load_dotenv()

import threading

import socket

HOST = str(os.getenv('host'))
PORT = int(os.getenv('port'))

config_file = open("config.yaml", 'r')
config = yaml.safe_load(config_file)
config_sizes = config['sizes']
message_types = config['message_types']
config_flags = config['flags']

udp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

dest = (HOST, PORT)
udp.connect(dest)

root = Tk()
frame = ttk.Frame(root, padding=10)
frame.grid()
ttk.Label(frame, text='Chat dos menores').grid(column=0, row=0)

text_area = Text(frame, height = 20, width = 50)
text_area.grid(column=0, row=1, columnspan=3)

text_input = Text(frame, height = 1, width = 25)
text_input.grid(column=0, row=2)

ttk.Button(frame, text='enviar', command = lambda:send_message()).grid(column=1, row=2)
ttk.Button(frame, text='Anexar arquivo', command = lambda:select_files()).grid(column=2, row=2)

author = simpledialog.askstring('username', 'digite seu nome', parent=root)
author = author.ljust(config_sizes['username'], ' ')

def send_message():
  try:
    input = text_input.get('1.0', 'end-1c')
    text_area.insert(END, f'você: {input}\n')
    flag_message = message_types['message']
    udp.send(f'{flag_message}{author}{input}'.encode())
    udp.send(config_flags['end'].encode())
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

  file_name_ljust = file_name.ljust(config_sizes['file_name'], ' ')

  flag_file = message_types['file']
  udp.send(f'{flag_file}{author}{file_name_ljust}'.encode())
  package = file.read(1024)

  message_size = len(package)
  while(package):
    udp.send(package)
    package = file.read(1024)
    message_size += len(package)

  print(f'sended package: {message_size}')
  udp.send(config_flags['end'].encode())
  file.close()

  text_area.insert(END, f'você: {file_name} enviado\n')
  print('Done Sending')

def listen():
  while True:
    try:
      msg_type = udp.recv(config_sizes['type'])
      msg_author = udp.recv(config_sizes['username'])

      if(msg_type.decode() == 'mesg'):
        read_message(msg_author.decode().rstrip())
      elif(msg_type.decode() == 'file'):
        save_file(msg_author.decode().rstrip())
    except UnicodeDecodeError as e:
      print(f'msg_type: {msg_type}, msg_author: {msg_author}')

def read_message(msg_author):
  content = read_content()
  text_area.insert(END, f'{msg_author}: {content.decode()}\n')

def save_file(msg_author):
  file_name = udp.recv(config_sizes['file_name']).decode().rstrip()
  file = open(f'download/{file_name}', 'wb')
  content = read_content()

  print(f'file size: {len(content)}')

  file.write(content)
  file.close()
  text_area.insert(END, f'{msg_author} enviou um arquivo: {file_name}\n')

def read_content():
  package = udp.recv(1024)
  response = package

  while(True):
    end_flag = package[-10:]
    if(end_flag == config_flags['end'].encode()):
      break

    package = udp.recv(1024)
    response += package

  return response[:-10]

threading.Thread(target=listen, args=[]).start()
root.mainloop()
