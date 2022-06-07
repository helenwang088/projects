# -*- coding: utf-8 -*-
"""
Created on Mon Jun  6 23:04:20 2022

@author: helen
"""

from tkinter import *
from tkinter import messagebox, Tk
from tkinter.ttk import Progressbar
import pyautogui

import time
pyautogui.FAILSAFE = True



class Active():
    def __init__(self,window):
        self.window = window

        lbl = Label(window, text="How many times?", font=50, bg="floral white")
        lbl.grid(column=0, row=0)
        
        # get input from user
        self.spin = IntVar()
        self.spin = Spinbox(window, from_=0, to=10000, width=5)
        self.spin.grid(column=0, row=2)



        # trigger click event
        btn = Button(window, text="start", font=50, command=self.clicked, bg="AntiqueWhite1")
        btn.grid(column=1, row=2)



    def clicked(self):
        txt = int(self.spin.get())

        for i in range(txt):
            pyautogui.moveTo(950,220)    
            pyautogui.leftClick()
            time.sleep(0.3)
            
            pyautogui.scroll(-1000) 
            time.sleep(0.2)
            pyautogui.leftClick(550, 180)
            time.sleep(0.2)
            
            pyautogui.scroll(-1000)
            pyautogui.leftClick(950,800)
            time.sleep(1.8)
            i += 1
    
            window.update()
        

if __name__ =='__main__':
    window = Tk()
    window.title("Active Window")

    window.geometry("+{}+{}".format(0, 0))
    window.geometry('250x150')
    window.config(bg="floral white")

    Active(window)

    window.mainloop()

