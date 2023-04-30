import socket
import tkinter as tk
from functools import partial
from tkinter import *
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

def main(top):
    # Setting up the window
    bob = top
    bob.title("BOB")
    width = bob.winfo_screenwidth()
    height = bob.winfo_screenheight()
    bob.geometry("%dx%d" % (width, height))

    Label(bob, text='Establishing connection...').pack()

    # ESTABLISH CONNECTION HERE

    key = get_random_bytes(16)
    cipher = AES.new(key, AES.MODE_EAX)
    nonce = cipher.nonce

    Label(bob, text='Connection established.').pack()
    e2 = Entry(bob)
    e2.place(x=500, y=500)

    frame = Frame(bob, width=400, height=400, bg="lightgrey")
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
        message = "BOB: " + message
        Label(frame, text=message, fg="purple", bg="lightgrey", font=("Lato", 16)).pack(side=TOP, anchor=NW)

        dcipher = AES.new(key, AES.MODE_EAX, cipher.nonce)
        end = dcipher.decrypt(ciphertext)
        end = end.decode('utf-8')

    def receive(bobMess, nonce, key):
        dcipher = AES.new(key, AES.MODE_EAX, nonce)
        bitMess = dcipher.decrypt(bobMess)
        end = bitMess.decode('utf-8')
        display = "ALICE: " + end
        Label(frame, text=display, fg="blue", bg="lightgrey", font=("Lato", 16)).pack(side=TOP, anchor=NE)
        return end

    Button(bob, text="Send", command=partial(send, cipher)).place(x=700, y=500)

    bob.mainloop()


if __name__ == "__main__":
    main()
