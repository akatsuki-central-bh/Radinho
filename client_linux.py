from tkinter import *
from tkinter import ttk

import socket

HOST = '192.168.1.255'  # Endereco IP do Servidor
PORT = 5000            # Porta que o Servidor esta

udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

dest = (HOST, PORT)

def send_message():
  INPUT = inputtxt.get("1.0", "end-1c")
  udp.sendto (INPUT.encode(), dest)
  outputtxt.insert(END, f"Você: {INPUT}\n")

root = Tk()
frm = ttk.Frame(root, padding=10)
frm.grid()
ttk.Label(frm, text="Chat dos menores").grid(column=0, row=0)

outputtxt = Text(frm, height = 20, width = 30)
outputtxt.grid(column=0, row=1)

inputtxt = Text(frm, height = 1, width = 25)
inputtxt.grid(column=0, row=2)

ttk.Button(frm, text="enviar", command = lambda:send_message()).grid(column=1, row=2)

root.mainloop()


