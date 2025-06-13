import socket
import threading

HEADER = 64
PORT = 6782
SERVER = socket.gethostbyname(socket.gethostname())
ADDRESS = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDRESS)

def handle_client(connection, address):
    print(f"[NEW CONNECTION] {address} connected.")
    connected = True
    while connected:
      try:
          message_length = connection.recv(HEADER).decode(FORMAT)
          if message_length:
              message_length = int(message_length)
              message = connection.recv(message_length).decode(FORMAT)
              if message == DISCONNECT_MESSAGE:
                  connected = False
                  print(f"[{address}] disconnected!")
              else:
                  print(f"[{address}] {message}")
      except ValueError:
          print(f"[ERROR] Invalid message length received from {address}.")
          break
      except Exception as e:
          print(f"[ERROR] An error occurred with {address}: {e}")
          break

    connection.close()

def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}!")
    while True:
        connection, address = server.accept()
        thread = threading.Thread(target=handle_client, args=(connection, address))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

print("[STARTING] server is starting...")
start()