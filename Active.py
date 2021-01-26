from tkinter import *
from tkinter import messagebox, Tk
from tkinter.ttk import Progressbar
import pyautogui
import random
#pyautogui.FAILSAFE = False



class Active():
    def __init__(self,window):
        self.window = window
        self.again = True
        self.flag = False
        self.window.bind("<Escape>",self.key_pressed)

        lbl = Label(window, text="How many minutes?", font=50, bg="floral white")
        lbl.grid(column=0, row=0)

        # get input from user
        self.spin = IntVar()
        self.spin = Spinbox(window, from_=0, to=100, width=5)
        self.spin.grid(column=0, row=2)

        # trigger click event
        btn = Button(window, text="ok", font=50, command=self.clicked, bg="AntiqueWhite1")
        btn.grid(column=1, row=2)

        # display progress bar while moving mouse
        self.bar = Progressbar(window, length=200, mode='determinate')

        self.bar['value'] = 0
        self.bar.grid(column=0, row=3)

    def clicked(self):
        txt = self.spin.get()
        counter = 0
        seconds = int(txt) * 60

        # move mouse
        while self.flag is False and counter < seconds:

            pyautogui.moveTo(random.randint(0,200), random.randint(50,150), duration=1)
            pyautogui.rightClick()
            counter += 1

            self.bar['value'] += (100/seconds)
            window.update()
        sys.exit()


    def key_pressed(self, event):
        self.flag = True
        answer = messagebox.askyesnocancel('Hi', 'Do you want to start again? Click "No" to quit.')

        if answer is False:
            sys.exit()
        elif answer is True:
            Active(window)
        else:
            self.flag = False



if __name__ =='__main__':
    window = Tk()
    window.title("Active Window")

    window.geometry("+{}+{}".format(0, 0))
    window.geometry('250x150')
    window.config(bg="floral white")

    Active(window)

    window.mainloop()

