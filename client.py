import socket

HEADER = 64
PORT = 6782
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "DISCONNECT"
SERVER = "172.31.128.56"
ADDRESS = (SERVER, PORT)

client = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
client.connect(ADDRESS)