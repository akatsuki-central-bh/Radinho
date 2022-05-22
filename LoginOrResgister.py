from tkinter import *

import yaml
from connector import create_user, login
from Login import main as Login
from Consts import  config_sizes, udp, config_flags, message_types

WIDTH_INPUT = 8

class LoginOrRegister(Frame):

    def __init__(self):
        super().__init__()
        self.username = ""
        self.password = ""
        self.initUI()
        

    def initUI(self):

        self.master.title("Cadastro")
        self.pack(fill=BOTH, expand=True)

        frame1 = Frame(self)
        frame1.pack(fill=X)

        lbl1 = Label(frame1, text="username", width=WIDTH_INPUT)
        lbl1.pack(side=LEFT, padx=5, pady=10)

        self.entry1 = Entry(frame1, textvariable=self.username)
        self.entry1.pack(fill=X, padx=5, expand=True)

        frame2 = Frame(self)
        frame2.pack(fill=X)

        lbl2 = Label(frame2, text="Password", width=WIDTH_INPUT)
        lbl2.pack(side=LEFT, padx=5, pady=10)

        self.entry2 = Entry(frame2)
        self.entry2.pack(fill=X, padx=5, expand=True)

        frame3 = Frame(self)
        frame3.pack(fill=X)

        btn = Button(frame3, text="Criar Conta", command=self.onSubmit)
        btn.pack(padx=5, pady=10)

        btn = Button(frame3, text="Login", command=self.login)
        btn.pack(padx=5, pady=10)

    def onSubmit(self):

        self.username = self.entry1.get()
        self.password = self.entry2.get()

        create_user( self.username, self.password )


        self.quit()

    def login(self):
        self.username = self.entry1.get()
        self.password = self.entry2.get()

        username = self.username.ljust(config_sizes["username"], ' ')
        password = self.password.ljust(config_sizes['password'], ' ')

        # udp.send(f'{message_types["login"]}{username}{password}'.encode())
        # response_flag = udp.recv(config_sizes['type']).decode()
        # if response_flag == config_flags['success']:
        #     pass
        # else:
        #     pass

        login(username, password)

def main():
    root = Tk()
    app = LoginOrRegister()
    root.mainloop()
    user_input = (app.username, app.password)
    print(app.username)
    try:
        root.destroy()
    except:
        pass
    return user_input

if __name__ == '__main__':
    follow_on_variable = main()
    print(follow_on_variable)