# from tkinter import *
# from tkinter import filedialog
# import yaml
# import os
# import socket
# from Chat import main as Chat


# class ChatController():

#   def __init__(self, text_input: Text ,text_area: Text, udp: socket, author: tuple):
#     self.text_input = text_input
#     self.text_area = text_area
#     config_file = open("config.yaml", 'r')
#     config = yaml.safe_load(config_file)
#     self.config_sizes = config['sizes']
#     self.message_types = config['message_types']
#     self.config_flags = config['flags']
#     self.udp = udp
#     self.author = author
#     return

#   def send_message(self):
#     try:
#       input = self.text_input.get('1.0', 'end-1c')
#       self.text_area.insert(END, f'você: {input}\n')
#       flag_message = self.message_types['message']
#       self.udp.send(f'{flag_message}{self.author}{input}'.encode())
#       self.udp.send(self.config_flags['end'].encode())
#     except BrokenPipeError as e:
#       print(e)

#   def select_files(self):
#     filetypes = (
#       ('All files', '*.*'),
#       ('text files', '*.txt')
#     )

#     path_name = filedialog.askopenfilename(
#       title='Open files',
#       initialdir='/',
#       filetypes=filetypes)

#     file_name = os.path.basename(path_name)
#     file = open(path_name, 'rb')

#     file_name_ljust = file_name.ljust(self.config_sizes['file_name'], ' ')

#     flag_file = self.message_types['file']
#     self.udp.send(f'{flag_file}{self.author}{file_name_ljust}'.encode())
#     package = file.read(1024)

#     message_size = len(package)
#     while(package):
#       self.udp.send(package)
#       package = file.read(1024)
#       message_size += len(package)

#     print(f'sended package: {message_size}')
#     self.udp.send(self.config_flags['end'].encode())
#     file.close()

#     self.text_area.insert(END, f'você: {file_name} enviado\n')
#     print('Done Sending')

#   def listen(self):
#     while True:
#       try:
#         msg_type = self.udp.recv(self.config_sizes['type'])
#         msg_author = self.udp.recv(self.config_sizes['username'])

#         if(msg_type.decode() == self.message_types['message']):
#           self.read_message(msg_author.decode().rstrip())
#         elif(msg_type.decode() == self.message_types['file']):
#           self.save_file(msg_author.decode().rstrip())
#       except UnicodeDecodeError as e:
#         print(f'msg_type: {msg_type}, msg_author: {msg_author}')

#   def read_message(self ,msg_author):
#     content = self.read_content()
#     self.text_area.insert(END, f'{msg_author}: {content.decode()}\n')

#   def save_file(self, msg_author):
#     file_name = self.udp.recv(self.config_sizes['file_name']).decode().rstrip()
#     file = open(f'download/{file_name}', 'wb')
#     content = self.read_content()

#     print(f'file size: {len(content)}')

#     file.write(content)
#     file.close()
#     self.text_area.insert(END, f'{msg_author} enviou um arquivo: {file_name}\n')

#   def read_content(self):
#     package = self.udp.recv(1024)
#     response = package

#     while(True):
#       end_flag = package[-10:]
#       if(end_flag == self.config_flags['end'].encode()):
#         break

#       package = self.udp.recv(1024)
#       response += package

#     return response[:-10]

#   def login(self):
#     username = input.ljust(self.config_sizes['username'], ' ')
#     password = input.ljust(self.config_sizes['password'], ' ')
#     self.udp.send(f'{self.message_types["login"]}{username}{password}')
#     response_flag = self.udp.recv(self.config_sizes['type'])
#     if response_flag == self.config_flags['success']:
#       Chat()
#     else:
#       pass


from tkinter import *
from tkinter import filedialog
import yaml
import os
import socket
from Chat import main as Chat


class ChatController():

  def __init__(self, text_input ,text_area, udp, author):
    self.text_input = text_input
    self.text_area = text_area
    config_file = open("config.yaml", 'r')
    config = yaml.safe_load(config_file)
    self.config_sizes = config['sizes']
    self.message_types = config['message_types']
    self.config_flags = config['flags']
    self.udp = udp
    self.author = author
    return

  def send_message(self):
    try:
      input = self.text_input.get('1.0', 'end-1c')
      self.text_area.insert(END, f'você: {input}\n')
      flag_message = self.message_types['message']
      self.udp.send(f'{flag_message}{self.author}{input}'.encode())
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
    self.udp.send(f'{flag_file}{self.author}{file_name_ljust}'.encode())
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
      except UnicodeDecodeError as e:
        print(f'msg_type: {msg_type}, msg_author: {msg_author}')

  def read_message(self ,msg_author):
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