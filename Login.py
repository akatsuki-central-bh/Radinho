from tkinter import *
# from connector import login


WIDTH_INPUT = 8

class LoginFrame(Frame):

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

        btn = Button(frame3, text="Logar", command=self.onSubmit)
        btn.pack(padx=5, pady=10)

    def onSubmit(self):

        self.username = self.entry1.get()
        self.password = self.entry2.get()
        self.quit()

def main():
    root = Tk()
    root.geometry("300x150+300+300")
    app = LoginFrame()
    root.mainloop()
    user_input = (app.username, app.password)
    # print(app.username)
    try:
        root.destroy()
        return user_input
    except:
        pass
    return user_input

if __name__ == '__main__':
    follow_on_variable = main()
    # print(follow_on_variable)