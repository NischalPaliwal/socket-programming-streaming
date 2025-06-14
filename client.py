import socket

HEADER = 64
PORT = 6782
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "DISCONNECT"
SERVER = "172.31.128.56"
ADDRESS = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDRESS)

def send(msg):
    message = msg.encode(FORMAT)
    message_length = len(message)
    send_length = str(message_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)

def receive_messages():
    """Function to continuously receive messages from server"""
    while True:
        try:
            message_length = client.recv(HEADER).decode(FORMAT)
            if message_length:
                message_length = int(message_length)
                message = client.recv(message_length).decode(FORMAT)
                print(f"[SERVER] {message}")
        except ValueError:
            print("[ERROR] Invalid message length received from server.")
            break
        except Exception as e:
            print(f"[ERROR] Connection lost: {e}")
            break

send("Hello, World!")
send("Hello, Everyone!")
send("How's everything going on?")