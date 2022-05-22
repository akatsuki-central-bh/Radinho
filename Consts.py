import os
import socket
import yaml
from dotenv import load_dotenv

load_dotenv()

HOST = str(os.getenv('host'))
PORT = int(os.getenv('port'))
TOKEN = ''

config_file = open("config.yaml", 'r')
config = yaml.safe_load(config_file)
config_sizes = config['sizes']
udp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
dest = (HOST, PORT)
udp.connect(dest)

config_flags = config['flags']
message_types = config['message_types']