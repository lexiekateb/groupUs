import socket
import threading
import math
import sys
import pyDHE

HEADER = 64
PORT = 5050
SERVER = "127.0.0.1"  # socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

# create a list of the clients connected to the server and list of messages to be sent to clients
connections = []
messages = []


def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")

    # Perform Diffie-Hellman key exchange
    alice = pyDHE.new(14)
    bob_pub_key_bytes = conn.recv(2048)
    bob_pub_key = int.from_bytes(bob_pub_key_bytes, sys.byteorder, signed=False)
    shared_key = alice.update(bob_pub_key)
    alice_pub_key = alice.getPublicKey()
    alice_pub_key_bytes = alice_pub_key.to_bytes(math.ceil(alice_pub_key.bit_length() / 8), sys.byteorder, signed=False)
    conn.sendall(alice_pub_key_bytes)
    small_key = int(str(shared_key)[:128])

    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE:
                connected = False
                # remove the connection when no longer active
                connections.remove((conn, addr))

            else:
                print(f"[{addr}] {msg}")
                # store message
                message = f"[{addr}] {msg}"
                messages.append(message)

                # send message to other clients
                for connection, address in connections:
                    if address != addr:
                        connection.send(f"{message}\n".encode(FORMAT))

    # disconnect the client when they leave the server
    conn.close()


def start_server():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")


print("[STARTING] server is starting...")
start_server()
