import database

from tkinter import Tk, ttk, filedialog, messagebox, END, Text
from tkinter.ttk import Frame

from dotenv import load_dotenv
import yaml
import os

load_dotenv()

import threading
import socket

class Client(Frame):
  def __init__(self, token, master = None):
    self.master = master
    self.frame = Frame(master, padding=10)
    self.token = token

    HOST = str(os.getenv('server_host'))
    PORT = int(os.getenv('port'))

    config_file = open("config.yaml", 'r')
    config = yaml.safe_load(config_file)
    self.config_sizes = config['sizes']
    self.message_types = config['message_types']
    self.config_flags = config['flags']

    self.udp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    dest = (HOST, PORT)
    self.udp.connect(dest)

    self.frame.grid()
    ttk.Label(self.frame, text='Chat dos menores').grid(column=0, row=0)

    self.text_area = Text(self.frame, height = 20, width = 50)
    self.text_area.grid(column=0, row=1, columnspan=3)

    self.text_input = Text(self.frame, height = 1, width = 25)
    self.text_input.grid(column=0, row=2)

    ttk.Button(self.frame, text='enviar', command = lambda:self.send_message()).grid(column=1, row=2)
    ttk.Button(self.frame, text='Anexar arquivo', command = lambda:self.select_files()).grid(column=2, row=2)

    master.protocol("WM_DELETE_WINDOW", self.logout)

  def send_message(self):
    try:
      message = self.text_input.get('1.0', 'end-1c')
      self.text_area.insert(END, f'você: {message}\n')
      flag_message = self.message_types['message']
      self.udp.send(f'{flag_message}{self.token}{message}'.encode())
      self.udp.send(self.config_flags['end'].encode())
    except BrokenPipeError as e:
      print(e)

  def select_files(self):
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

    file_name_ljust = file_name.ljust(self.config_sizes['file_name'], ' ')

    flag_file = self.message_types['file']
    self.udp.send(f'{flag_file}{self.token}{file_name_ljust}'.encode())
    package = file.read(1024)

    message_size = len(package)
    while(package):
      self.udp.send(package)
      package = file.read(1024)
      message_size += len(package)

    print(f'sended package: {message_size}')
    self.udp.send(self.config_flags['end'].encode())
    file.close()

    self.text_area.insert(END, f'você: {file_name} enviado\n')
    print('Done Sending')

  def listen(self):
    while True:
      try:
        msg_type = self.udp.recv(self.config_sizes['type'])
        msg_author = self.udp.recv(self.config_sizes['username'])

        if(msg_type.decode() == self.message_types['message']):
          self.read_message(msg_author.decode().rstrip())
        elif(msg_type.decode() == self.message_types['file']):
          self.save_file(msg_author.decode().rstrip())
      except Exception as e:
        print(e)
        break

  def read_message(self, msg_author):
    content = self.read_content()
    self.text_area.insert(END, f'{msg_author}: {content.decode()}\n')

  def save_file(self, msg_author):
    file_name = self.udp.recv(self.config_sizes['file_name']).decode().rstrip()
    file = open(f'download/{file_name}', 'wb')
    content = self.read_content()

    print(f'file size: {len(content)}')

    file.write(content)
    file.close()
    self.text_area.insert(END, f'{msg_author} enviou um arquivo: {file_name}\n')

  def read_content(self):
    package = self.udp.recv(1024)
    response = package

    while(True):
      end_flag = package[-10:]
      if(end_flag == self.config_flags['end'].encode()):
        break

      package = self.udp.recv(1024)
      response += package

    return response[:-10]

  def logout(self):
    try:
      if messagebox.askokcancel("Sair", "Você realmente quer sair?"):
        database.logout(self.token)
        self.udp.close()
    finally:
      self.master.destroy()

def main(token):
  root = Tk()

  client = Client(token, root)

  threading.Thread(target=client.listen, args=[]).start()

  root.mainloop()
