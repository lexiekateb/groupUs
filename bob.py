import socket
import tkinter as tk
from functools import partial
from tkinter import *
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes


# Setting up the window
bob = tk.Tk()
bob.title("BOB")
width = bob.winfo_screenwidth()
height = bob.winfo_screenheight()
bob.geometry("%dx%d" % (width, height))

Label(bob, text='Bob works').grid(row=0)

bob.mainloop()