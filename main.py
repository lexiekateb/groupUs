import tkinter as tk
import alice
from tkinter import *
import socket
import pyDHE
import sys
import math


gus = tk.Tk()
gus.title("GroupUs")

# Making it full screen
width = gus.winfo_screenwidth()
height = gus.winfo_screenheight()
gus.geometry("%dx%d" % (width, height))
Label(gus, text="GroupUs", font=("Lato", 60)).place(x=500, y=100)


def openAlice():
    truePass = "alicewuzhere"
    givenPass = e1.get()

    if truePass == givenPass:
        top = Toplevel()
        alice.main(top)
    else:
        Label(gus, text='WRONG PASSWORD', fg="red").place(x=300, y=300)


def openBob():
    truePass = "bobwuzhere"
    givenPass = e2.get()

    if truePass == givenPass:
        gus.withdraw()
        exec(open("./bob.py").read())
    else:
        Label(gus, text='WRONG PASSWORD', fg="red").place(x=300, y=300)


# Buttons to enter password
Label(gus, text='Alice, enter password', font=("Lato", 16)).place(x=300, y=240)
Label(gus, text='Bob, enter password', font=("Lato", 16)).place(x=700, y=240)
e1 = Entry(gus)
e2 = Entry(gus)
e1.place(x=300, y=270)
e2.place(x=700, y=270)
bA = Button(gus, text="Enter", command=openAlice)
bB = Button(gus, text="Enter", command=openBob)
bA.place(x=500, y=270)
bB.place(x=900, y=270)

gus.mainloop()
