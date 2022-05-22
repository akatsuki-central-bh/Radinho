from socket import socket
from tkinter import Tk, Text, TOP, BOTH, X, N, LEFT, RIGHT
from tkinter.ttk import Frame, Label, Entry, Button
import user_controller
import yaml

class SimpleDialog(Frame):

    def __init__(self):
        super().__init__()
        self.username = ""
        self.password = ""
        self.confirm_password = ""

        config_file = open("config.yaml", 'r')
        config = yaml.safe_load(config_file)
        self.config_sizes = config['sizes']
        self.message_types = config['message_types']
        self.config_flags = config['flags']

        self.initUI()

    def initUI(self):

        self.master.title("Simple Dialog")
        self.pack(fill=BOTH, expand=True)

        frame1 = Frame(self)
        frame1.pack(fill=X)

        lbl1 = Label(frame1, text="Usuário:", width=6)
        lbl1.pack(side=LEFT, padx=5, pady=10)

        self.entry1 = Entry(frame1, textvariable=self.username)
        self.entry1.pack(fill=X, padx=5, expand=True)

        frame2 = Frame(self)
        frame2.pack(fill=X)

        lbl2 = Label(frame2, text="Senha:", width=6)
        lbl2.pack(side=LEFT, padx=5, pady=10)

        self.entry2 = Entry(frame2)
        self.entry2.pack(fill=X, padx=5, expand=True)

        frame3 = Frame(self)
        frame3.pack(fill=X)

        lbl2 = Label(frame3, text="Confirmação da senha:", width=6)
        lbl2.pack(side=LEFT, padx=5, pady=10)

        self.entry3 = Entry(frame3)
        self.entry3.pack(fill=X, padx=5, expand=True)

        frame4 = Frame(self)
        frame4.pack(fill=X)

        btn = Button(frame4, text="Cadastrar", command=self.onRegister)
        btn.pack(padx=5, pady=10)

    def onRegister(self):
        socket = user_controller.connect()
        user_controller.register(
            socket, self.entry1.get(), self.entry2.get()
        )

        socket.close()

        self.master.destroy()

def main():
    SimpleDialog()

if __name__ == '__main__':
    follow_on_variable = main()
    print(follow_on_variable)
