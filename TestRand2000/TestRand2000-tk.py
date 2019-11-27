#!/usr/bin/env python3
# TestRand2000-tk.py: randomization of test positions
# Copyright 2019 Peter Kvillegård. Subject to the Unlicense.

import datetime
import numpy as np
from tkinter import *

np.random.seed(None)

mvics = ['INF','DPP','DPI']
tps = ['Ej adduktion','Adduktion']

def timestamp():
    return datetime.datetime.now().replace(microsecond=0).isoformat().replace('T',' ')    

def click():
    ts.configure(text=timestamp())
    np.random.shuffle(mvics)
    np.random.shuffle(tps)
    t = 'MVIC:\n'+'1. '+mvics[0]+'\n'+'2. '+ mvics[1]+'\n'+'3. '+mvics[2]+'\n\n'+'Testpositioner:\n'+'1. '+tps[0]+'\n'+'2. '+tps[1]
    order.configure(text=t)
    print(timestamp()+'\n'+t+'\n')
 
w = Tk()
w.configure(background='white')
w.title("TestRand2000")
w.geometry('480x227')

ts = Label(w, text=timestamp(), justify=LEFT,padx = 40)
ts.configure(background='white',font=("Courier", 12))
ts.grid(column=0, row=0)

order = Label(w, text='\n\n\n\n\n\n\n', justify=LEFT)
order.configure(background='white',font=("Courier", 12))
order.grid(column=0, row=1)

btn = Button(w, text="Ny slumpmässig ordning", command=click)
btn.configure(font=("Courier", 12))
btn.grid(column=0, row=2)

logogif = PhotoImage(file="logo.gif")
logo = Label(w, image=logogif, borderwidth=0,highlightthickness=0)
logo.grid(column=1, row=0, rowspan=10)

w.mainloop()