import tkinter as tk
import alice
from tkinter import *
import socket
import pyDHE
import sys
import math
# from server import start_server

HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = "127.0.0.1"  # socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)

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
        # Establishing connection and generating shared key

        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(ADDR)

        # Diffie-Hellman function for key generation
        bob = pyDHE.new(14)
        bob_pub_key = bob.getPublicKey()
        bob_pub_key_bytes = bob_pub_key.to_bytes(math.ceil(bob_pub_key.bit_length() / 8), sys.byteorder, signed=False)
        client.sendall(bob_pub_key_bytes)
        alice_pub_key_bytes = client.recv(2048)  # may need to change to 1024
        alice_pub_key = int.from_bytes(alice_pub_key_bytes, sys.byteorder, signed=False)
        shared_key = bob.update(alice_pub_key)
        small_key = int(str(shared_key)[:128])

        top = Toplevel()
        # alice.main(top, client, shared_key, small_key)
        alice.main(top, client, small_key)
        # alice.main(top)
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

# if __name__ == '__main__':
# start_server()
