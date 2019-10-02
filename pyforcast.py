#!/usr/bin/env python3

from tkinter import *
from tkinter import ttk
from datetime import datetime

def keep_time(*args):
    try:
        time_str.set(datetime.now().strftime('%H:%M:%S'))
        date_str.set(datetime.now().strftime('%Y-%m-%d'))
    except:
        print("Couldn't update time")
    root.after(100, keep_time)

def exit_program(*args):
    root.destroy()

#instantiate window
root = Tk()
root.title("pyForcast")

#setup main view frame within root
mainframe = ttk.Frame(root, padding="3 3 12 12", width=400, height=200)
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

#initialise date/time strings
date_str = StringVar()
time_str = StringVar()

#date/time labels
label_date = ttk.Label(mainframe, textvariable=date_str).grid(column=1, row=1, sticky=W)
label_time = ttk.Label(mainframe, textvariable=time_str).grid(column=1, row=2, sticky=W)

#quit button
button_quit = ttk.Button(mainframe, text="Quit", command=exit_program).grid(column=3, row=3, sticky=W)

#adjust window
for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)

#start clock
keep_time()

#run main loop
root.mainloop()
