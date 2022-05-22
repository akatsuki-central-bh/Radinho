from tkinter import *
from tkinter import ttk
import ChatController


class Chat (Frame) :
  def __init__(self):
        super().__init__()
        self.username = ""
        self.password = ""
        self.initUI()
        self.chatController = ChatController

  def initUI(self):
    frame= ttk.Frame(self, padding=10) .grid()
    self.master.title("Chat dos menores")

    Label(frame, text='Chat dos menores').grid(column=0, row=0)

    text_area = Text(frame, height = 20, width = 50)
    text_area.grid(column=0, row=1, columnspan=3)

    text_input = Text(frame, height = 1, width = 25)
    text_input.grid(column=0, row=2)

    ttk.Button(frame, text='enviar', command = lambda:self.chatController.send_message()).grid(column=1, row=2)
    ttk.Button(frame, text='Anexar arquivo', command = onClickSend( text_input, text_area  ) ).grid(column=2, row=2)
    return ( text_area, text_input )

def onClickSend ( self,  input: Text, area: Text ):
    self.chatController( input, area )
    lambda:self.chatController.send_message()

def main():
  root = Tk()
  x = Chat()

  root.mainloop()

if __name__ == '__main__':
  follow_on_variable = main()