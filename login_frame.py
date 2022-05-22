from tkinter import Tk, Text, TOP, BOTH, X, N, LEFT, RIGHT
from tkinter.ttk import Frame, Label, Entry, Button
import register_frame

class SimpleDialog(Frame):

    def __init__(self):
        super().__init__()
        self.output1 = ""
        self.output2 = ""
        self.initUI()

    def initUI(self):

        self.master.title("Simple Dialog")
        self.pack(fill=BOTH, expand=True)

        frame1 = Frame(self)
        frame1.pack(fill=X)

        lbl1 = Label(frame1, text="Usuário:", width=6)
        lbl1.pack(side=LEFT, padx=5, pady=10)

        self.entry1 = Entry(frame1, textvariable=self.output1)
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

    def onLogin(self):

        self.output1 = self.entry1.get()
        self.output2 = self.entry2.get()
        self.quit()
    
    def onRegister(self):
        register_frame.main()

def main():

    root = Tk()
    app = SimpleDialog()
    root.mainloop()
    user_input = (app.output1, app.output2)
    print(app.output1)
    try:
        root.destroy()
    except:
        pass
    return user_input

if __name__ == '__main__':
    follow_on_variable = main()
    print(follow_on_variable)
