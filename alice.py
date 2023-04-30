import socket
import tkinter as tk
from functools import partial
from tkinter import *
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import sys
import math
import pyDHE
# from user import send_m

# sys.path.append("..")

# from main import top, client, shared_key, small_key

# modified arguments to grab client and small key from main.py

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

    Label(alice, text='Establishing connection...').pack()

    # ESTABLISH CONNECTION HERE
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

        # send the encrypted message to Bob
        send_msg = ciphertext + nonce
        print(send_msg)
        # send_m(message)

        dcipher = AES.new(key, AES.MODE_EAX, cipher.nonce)
        # end = dcipher.decrypt(ciphertext)
        # end = end.decode('utf-8')

    def receive(bobMess, nonce, key):
        dcipher = AES.new(key, AES.MODE_EAX, nonce)
        bitMess = dcipher.decrypt(bobMess)
        end = bitMess.decode('utf-8')
        Label(frame, text=end, fg="blue", bg="lightgrey", font=("Lato", 16)).pack(side=TOP, anchor=NE)
        return end

    Button(alice, text="Send", command=partial(send, cipher)).place(x=700, y=500)

    alice.mainloop()


# if __name__ == "__main__":
    # main(top, client, shared_key, small_key)
    # main()
