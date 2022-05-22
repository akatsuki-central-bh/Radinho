from tkinter import Tk, BOTH, X, LEFT
from tkinter.ttk import Frame, Label, Entry, Button
import database
import register_frame
class loginframe(Frame):

    def __init__(self, socket):
        super().__init__()
        self.token = ''
        self.socket = socket
        self.initUI()

    def initUI(self):

        self.master.title("Simple Dialog")
        self.pack(fill=BOTH, expand=True)

        frame1 = Frame(self)
        frame1.pack(fill=X)

        lbl1 = Label(frame1, text="Usuário:", width=6)
        lbl1.pack(side=LEFT, padx=5, pady=10)

        self.entry1 = Entry(frame1)
        self.entry1.pack(fill=X, padx=5, expand=True)

        frame2 = Frame(self)
        frame2.pack(fill=X)

        lbl2 = Label(frame2, text="Senha:", width=6)
        lbl2.pack(side=LEFT, padx=5, pady=10)

        self.entry2 = Entry(frame2)
        self.entry2.pack(fill=X, padx=5, expand=True)

        frame3 = Frame(self)
        frame3.pack(fill=X)

        btn = Button(frame3, text="Entrar", command=self.onLogin)
        btn.pack(padx=5, pady=10)
        btn = Button(frame3, text="Cadastro", command=self.onRegister)
        btn.pack(padx=5, pady=10)

        # self.protocol("WM_DELETE_WINDOW", onClose)

    def onClose():
        self.token = "exit"
        self.quit

    def onLogin(self):
        self.token = database.login(
            self.entry1.get(), self.entry2.get()
        )

        self.quit()

    def onRegister(self):
        self.master.destroy()
        self.token = register_frame.main(self.socket)

def main(socket):
    root = Tk()
    app = loginframe(socket)
    root.mainloop()

    try:
        root.destroy()
    except:
        pass

    return app.token

if __name__ == '__main__':
    follow_on_variable = main()
    print(follow_on_variable)
