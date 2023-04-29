import socket
import pyDHE
import sys
import math

HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)

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
# print(small_key)

def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)
    print(client.recv(2048).decode(FORMAT))


send(" ")
text = input()
while text:
    send(text)
    text = input()

send(DISCONNECT_MESSAGE)

