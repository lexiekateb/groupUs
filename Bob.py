# echo-client.py

import math
import socket
import sys

import pyDHE

# print("input a key:")
# msg = input()
# str_msg = str(msg)
# new_msg = bytes(msg, encoding='utf8')

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 65432  # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    # s.sendall(new_msg)
    # data = s.recv(1024)
    bob = pyDHE.new(14)
    bob_pub_key = bob.getPublicKey()
    bob_pub_key_bytes = bob_pub_key.to_bytes(math.ceil(bob_pub_key.bit_length()/8), sys.byteorder, signed=False)
    s.sendall(bob_pub_key_bytes)
    alice_pub_key_bytes = s.recv(2048)  # may need to change to 1024
    alice_pub_key = int.from_bytes(alice_pub_key_bytes, sys.byteorder, signed=False)
    shared_key = bob.update(alice_pub_key)
    small_key = int(str(shared_key)[:128])
    print(small_key)


# print(f"Received {data!r}")
