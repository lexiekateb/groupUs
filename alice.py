import socket
import tkinter as tk
from functools import partial
from tkinter import *
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes


def main(top):
    # Setting up the window
    alice = top
    alice.title("ALICE")
    width = alice.winfo_screenwidth()
    height = alice.winfo_screenheight()
    alice.geometry("%dx%d" % (width, height))

    Label(alice, text='Establishing connection...').pack()

    # ESTABLISH CONNECTION HERE

    key = get_random_bytes(16)
    cipher = AES.new(key, AES.MODE_EAX)
    nonce = cipher.nonce

    Label(alice, text='Connection established.').pack()
    e2 = Entry(alice)
    e2.place(x=500, y=500)

    frame = Frame(alice, width=400, height=400, bg="lightgrey")
    frame.place(x=450, y=50)
    frame.pack_propagate(0)

    # Message sending
    def send(cipher):
        message = e2.get()
        if message == "":
            return

        # clear text entry
        e2.delete(0, END)

        bitMess = bytes(message, 'utf-8')
        ciphertext = cipher.encrypt(bitMess)
        message = "ALICE: " + message
        Label(frame, text=message, fg="purple", bg="lightgrey", font=("Lato", 16)).pack(side=TOP, anchor=NW)

        # TODO: socket stuff to send cipher

    def receive(bobMess, nonce, key):
        dcipher = AES.new(key, AES.MODE_EAX, nonce)
        bitMess = dcipher.decrypt(bobMess)
        end = bitMess.decode('utf-8')
        Label(frame, text=end, fg="blue", bg="lightgrey", font=("Lato", 16)).pack(side=TOP, anchor=NE)
        return end

    Button(alice, text="Send", command=partial(send, cipher)).place(x=700, y=500)

    alice.mainloop()

#