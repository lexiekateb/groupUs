import math
import socket
import sys

import pyDHE

# print("this works")


HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()

    # while True: (this causes following code to be unreachable)
    conn, addr = s.accept()

    with conn:
        print(f"Connected by {addr}")

        alice = pyDHE.new(14)
        bob_pub_key_bytes = conn.recv(2048)
        bob_pub_key = int.from_bytes(bob_pub_key_bytes, sys.byteorder, signed=False)
        shared_key = alice.update(bob_pub_key)
        alice_pub_key = alice.getPublicKey()
        alice_pub_key_bytes = alice_pub_key.to_bytes(math.ceil(alice_pub_key.bit_length()/8), sys.byteorder,
                                                     signed=False)
        conn.sendall(alice_pub_key_bytes)
        
        print(shared_key)
