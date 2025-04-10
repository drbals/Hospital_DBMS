import pickle
import socket

HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
# SERVER = "192.168.43.234"
SERVER = "127.0.0.1"
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)


def transact(*args):
    message = pickle.dumps(args)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)
    msg_length = client.recv(HEADER).decode(FORMAT)
    msg = None
    print("msg_length:", msg_length)
    if msg_length:
        msg_length = int(msg_length)
        msg = pickle.loads(client.recv(msg_length))
    return msg