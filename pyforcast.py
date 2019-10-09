#!/usr/bin/env python3

import json
import numpy as np
import tkinter
import requests as req
from tkinter import *
from tkinter import ttk
from datetime import datetime
from scipy import optimize

from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure

#sets time_str and date_str then schedules callback for self
def keep_time(*args):
    try:
        time_str.set(datetime.now().strftime('%H:%M:%S'))
        date_str.set(datetime.now().strftime('%Y-%m-%d'))
    except:
        print("Couldn't update time")
    root.after(100, keep_time)

#calls destroy function of root
def exit_program(*args):
    root.destroy()

#captures key events for toolbar
def on_key_press(event):
    print("you pressed {}".format(event.key))
    key_press_handler(event, canvas, toolbar)

#instantiate window
root = Tk()
root.title("pyForcast")

#setup main view frame within root
mainframe = ttk.Frame(root, padding="3 3 3 3", width=400, height=200)
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

#initialise date/time strings
date_str = StringVar()
time_str = StringVar()

#date/time labels
label_date = ttk.Label(mainframe, textvariable=date_str).grid(column=1, row=1, sticky=W)
label_time = ttk.Label(mainframe, textvariable=time_str).grid(column=2, row=1, sticky=W)

#quit button
button_quit = ttk.Button(mainframe, text="Quit", command=exit_program).grid(column=3, row=3, sticky=W)

#import data
with open("IDV60901.95867.json", "r") as read_file:
    json_raw = json.load(read_file)

data = json_raw['observations']['data']

request = req.get("http://www.bom.gov.au/fwo/IDV60901/IDV60901.95867.json")

live_raw = request.json()

live_data = live_raw['observations']['data']

data = live_data

#prepare data
atl = []
ftl = []
for item in data:
    try:
        atl.append(float(item['air_temp']))
        ftl.append(item['local_date_time_full'])
    except:
        print("Couldn't vectorize data")

ftl_dt = []
for t in ftl:
    ftl_dt.append(datetime.strptime(t, '%Y%m%d%H%M%S'))

ftl_ts = []
for t in ftl_dt:
    ftl_ts.append((datetime.timestamp(t)))

#try fitting
#

#construct figure
fig = Figure(figsize=(8, 6), dpi=100)
sp = fig.add_subplot(111)
sp.plot_date(ftl_dt, atl)

canvas = FigureCanvasTkAgg(fig, master=mainframe)
canvas.draw()
canvas.get_tk_widget().grid(column=2, row=2, sticky=W)
canvas.mpl_connect("key_press_event", on_key_press)

#add convenient toolbar
toolframe = ttk.Frame(root, padding="3 3 3 3")
toolframe.grid(column=0, row=1, sticky=(N, W, E, S))
toolbar = NavigationToolbar2Tk(canvas, toolframe)
toolbar.update()


#adjust child spacing for visibility
for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)

#start clock
keep_time()

#run main loop
root.mainloop()
