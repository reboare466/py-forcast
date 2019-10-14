#!/usr/bin/env python3

import json
import numpy as np
import tkinter
import requests as req
from tkinter import *
from tkinter import ttk
from datetime import datetime
#from scipy import optimize
from scipy import signal

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

#fetch data
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

#optimize section
window = 9
weights = np.repeat(1.0, window)/window
atl_temp = np.convolve(atl,weights,'valid')
#atl = atl_temp

#signal section
atl_smooth = signal.savgol_filter(atl,25,3)
atl_smooth = signal.savgol_filter(atl,25,3)


#z = np.polyfit(ftl_ts[:20], atl[:20],2)
#int_min = np.where(atl == np.amin(atl[:20]))
#int_max = np.where(atl == np.amax(atl[:20]))
#temp = atl[int_min[0]:int_max[0]]
z = np.polyfit(ftl_ts[:20], atl[:20],2)
f = np.poly1d(z)

#extrapolate time from most recent observation to +12h
ftl_ts_ex = np.linspace(ftl_ts[1],ftl_ts[1]+21600,12)

ftl_dt_ex = []
for t in ftl_ts_ex:
    ftl_dt_ex.append((datetime.fromtimestamp(t)))

#try fitting
#

#construct figure
fig = Figure(figsize=(8, 6), dpi=100)
sp = fig.add_subplot(111)
sp.plot_date(ftl_dt, atl)
sp.plot_date(ftl_dt, atl_smooth)
sp.plot_date(ftl_dt_ex, f(ftl_ts_ex))

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
