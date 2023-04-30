import socket
import tkinter as tk
from functools import partial
from tkinter import *
from Crypto.Cipher import AES
import sys
import math
import pyDHE
import user

HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = "127.0.0.1"  # socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)


def main(top):
    # Setting up the window
    alice = top
    alice.title("ALICE")
    width = alice.winfo_screenwidth()
    height = alice.winfo_screenheight()
    alice.geometry("%dx%d" % (width, height))

    # ESTABLISH CONNECTION HERE
    Label(alice, text='Establishing connection...').pack()
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
    small_key = bytes(str(shared_key)[:16], 'utf-8')

    print("make it here")
    print(small_key)
    # Creating ciper using key from DH
    cipher = AES.new(small_key, AES.MODE_EAX)
    nonce = cipher.nonce

    Label(alice, text='Connection established.').pack()

    # GUI stuff
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

        # Transforming message to bytes
        bitMess = bytes(message, 'utf-8')
        ciphertext = cipher.encrypt(bitMess)

        # Putting text on screen
        message = "ALICE: " + message
        Label(frame, text=message, fg="purple", bg="lightgrey", font=("Lato", 16)).pack(side=TOP, anchor=NW)

        # send the encrypted message to Bob through socket
        send_msg = ciphertext
        # user.send_m(send_msg)  # may need to modify this line
        client.send(send_msg)
        # TODO: socket stuff to send cipher

    # When socket detects message, use this to decrypt
    def receive(nonce, small_key):
        client.setblocking(False)
        print('enters receive')
        # trying to receive message
        rec = False
        try:
            message = client.recv(1024)
            print('past message')
            if not message:
                rec = False
            else:
                rec = True
        except socket.error as e:
            print("Error receiving data: %s" % e)
        finally:
            print('exits try')
            if rec is True:
                print('message received')
            else:
                print('no message received')

        # Replicating cipher / decyphering
        if rec is True:
            dcipher = AES.new(small_key, AES.MODE_EAX, nonce)
            print(message)
            bitMess = dcipher.decrypt(message)
            print(bitMess)
            end = bitMess.decode('utf-8')

            # placing on GUI
            Label(frame, text=end, fg="blue", bg="lightgrey", font=("Lato", 16)).pack(side=TOP, anchor=NE)

    # Button to send message
    Button(alice, text="Send", command=partial(send, cipher)).place(x=700, y=500)

    # Waiting to receive a message
    alice.after(1000, receive(nonce, small_key))

    # Keeps screen open until user closes windows
    alice.mainloop()
