#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  8 20:19:35 2019

@author: rodri
"""

import numpy as np
import matplotlib.pyplot as plt
import scipy as scy
import os
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk
from tkinter import PhotoImage
import serial
import struct
from PIL import Image, ImageTk

# =============================================================================
# Create a new Tkinter window and modify its geometry and title
# =============================================================================
window = tk.Tk()

window.geometry('600x350')
window.title("Gripper Control")
window.resizable(False, False)

# =============================================================================
# Define functions of system
# =============================================================================
def find_ports(directory):
    names = []
    for root, dirs, files in os.walk(directory):
        for name in files:
            if name.startswith('ttyUSB'):
                names.append(directory+name)
    return names


# =============================================================================
# Create some global variables to use through the program
# =============================================================================
baudrate = 9600
gripperPosition = 0
port_list = find_ports('/dev/')
port_list.insert(0, "-- select --")

#selected_port = '/dev/ttyUSB0'

status_colors = {"ON":"green", "OFF":"red"}
connection_status = "OFF"
open_status = "OFF"
close_status = "ON"

# =============================================================================
# Define different functions for the menu buttons
# =============================================================================

# Dummy function for the buttons
def donothing():
   filewin = tk.Toplevel(window)
   button = tk.Button(filewin, text="Do nothing button")
   button.pack()

# Function to open the claw
def open_gripper():
    if connection_status == "OFF":
       messagebox.showerror("Error", "No connection found")
    else:
        global gripperPosition
        gripperPosition = 25
        ArduinoSerial.write(struct.pack('>i', gripperPosition))
        global open_status
        global close_status
        open_status = "ON"
        close_status = "OFF"
        open_led.create_oval(coord, fill=status_colors[open_status])
        close_led.create_oval(coord, fill=status_colors[close_status])
    
# Function to close the claw    
def close_gripper():
    if connection_status == "OFF":
        messagebox.showerror("Error", "No connection found")
    else:
        global gripperPosition
        gripperPosition = 0
        ArduinoSerial.write(struct.pack('>i', gripperPosition))
        global open_status
        global close_status
        open_status = "OFF"
        close_status = "ON"
        open_led.create_oval(coord, fill=status_colors[open_status])
        close_led.create_oval(coord, fill=status_colors[close_status])
    
def ComboboxPort(event):
    global selected_port
    selected_port = port_select.get()
    
def connectToArduino():
    # =============================================================================
    # Receive and send instructions to Arduino
    # =============================================================================
    try:
        try:
            global ArduinoSerial
            ArduinoSerial = serial.Serial(selected_port, baudrate)
            if ArduinoSerial.readline():
                global connection_status
                connection_status = "ON"
                status_led.create_oval(coord, fill=status_colors[connection_status])
            else:
                messagebox.showwarning("Warning","Connection can not be stablished")
        except serial.serialutil.SerialException:
            pass
    except NameError:
        messagebox.showwarning("Warning","No port has been selected")
        
        
def closeConnection():
    ArduinoSerial.close()
    global connection_status
    connection_status = "OFF"
    status_led.create_oval(coord, fill=status_colors[connection_status])
    
# =============================================================================
# Create the drop-down menu and the drop-down buttons
# =============================================================================
menubar = tk.Menu(window)
# Create "File" menu button and all sub-buttons
filemenu = tk.Menu(menubar, tearoff=0)
filemenu.add_command(label="Close connection", command=closeConnection)
menubar.add_cascade(label="File", menu=filemenu)
# Create "Help" menu button and all sub-buttons
helpmenu = tk.Menu(menubar, tearoff=0)
helpmenu.add_command(label="Help Index", command=donothing)
helpmenu.add_command(label="About...", command=donothing)
menubar.add_cascade(label="Help", menu=donothing)

window.config(menu=menubar)

# =============================================================================
# Create main frame to place the window widgets
# =============================================================================
mainframe = tk.Frame(window)
mainframe.grid(column=0, row=0, sticky=("N", "W", "E", "S"))

window.columnconfigure(0, weight=1)
window.rowconfigure(0, weight=1)	

## Create Label frame containing the connection setup
connection_setup = tk.LabelFrame(mainframe, text="Connection Setup")
connection_setup.grid(column=0, row=0, pady=10, padx=10, columnspan=3)

port_desc = tk.Label(connection_setup, text="Port")
port_desc.grid(column=0, row=0, sticky=("N","W"), pady=10, padx=10)

port_select = ttk.Combobox(connection_setup, values=port_list)
port_select.grid(column=0, row=1, sticky=("N", "W"), pady=10, padx=10)
port_select.bind("<<ComboboxSelected>>", ComboboxPort)

baud_desc = tk.Label(connection_setup, text="Baudrate")
baud_desc.grid(column=1, row=0, sticky=("N","W"), pady=10, padx=10)

baud_var = tk.StringVar()
baud_value = tk.Entry(connection_setup, width=12,textvariable=baud_var, state="readonly")
baud_var.set(str(baudrate))
baud_value.grid(column=1, row=1, sticky=("N", "W"), pady=10, padx=10)

connect_button = tk.Button(connection_setup, text="Connect", command=connectToArduino)
connect_button.grid(column=2, row=1, sticky="W")

status_label = tk.Label(connection_setup, text="Status")
status_label.grid(column=3, row=0, sticky=("N","E"), pady=10, padx=65)

# Create connection status LED
status_led= tk.Canvas(connection_setup, height=20, width=20)
status_led.grid(column=3, row=1, sticky=("N","W"), pady=10, padx=75)

coord = 5,5,15,15
status_led.create_oval(coord, fill=status_colors[connection_status])

# Add an Arduino image to give some color to the app
canvas = tk.Canvas(mainframe, width=250, height=150)
canvas.grid(column=0, row=1, sticky=("N", "W"), pady=20, padx=20)
photo = PhotoImage(file='arduino_image_small.png')
photo_ref = photo
canvas.create_image(100,75, image=photo)


# Gripper setup frame
gripper_setup = tk.LabelFrame(mainframe, text="Gripper Setup")
gripper_setup.grid(column=1, row=1, rowspan=3,sticky=("N","W"),pady=10, padx=10)

open_button = tk.Button(gripper_setup, text="Open", command=open_gripper)
open_button.grid(column=0, row=0, sticky="W",pady=10, padx=10)

close_button = tk.Button(gripper_setup, text="Close", command=close_gripper)
close_button.grid(column=1, row=0, sticky="W",pady=10, padx=10)

# Create "OPEN" status led
open_led= tk.Canvas(gripper_setup, height=20, width=20)
open_led.grid(column=0, row=1, pady=10, padx=10)
coord = 5,5,15,15
open_led.create_oval(coord, fill=status_colors[open_status])

# Create "CLOSE" status led
close_led= tk.Canvas(gripper_setup, height=20, width=20)
close_led.grid(column=1, row=1, pady=10, padx=10)
coord = 5,5,15,15
close_led.create_oval(coord, fill=status_colors[close_status])
    


window.mainloop()