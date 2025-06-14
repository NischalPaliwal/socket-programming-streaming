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

active_connections = []
connections_lock = threading.Lock()

def handle_client(connection, address):
    print(f"[NEW CONNECTION] {address} connected.")
    
    # Add to active connections
    conn_info = {'connection': connection, 'address': address}
    with connections_lock:
        active_connections.append(conn_info)
    
    # Send welcome message
    send_to_client(connection, f"Welcome to the server! You are connected from {address}")
    
    # Notify other clients
    broadcast_message(f"[SERVER] New user joined from {address}", connection)
    
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
                    broadcast_message(f"[SERVER] User from {address} disconnected", connection)
                else:
                    print(f"[{address}] {message}")
                    # Echo message back to sender and broadcast to others
                    send_to_client(connection, f"Echo: {message}")
                    broadcast_message(f"[{address}] {message}", connection)
        except ValueError:
            print(f"[ERROR] Invalid message length received from {address}.")
            break
        except Exception as e:
            print(f"[ERROR] An error occurred with {address}: {e}")
            break
    
    # Remove from active connections
    with connections_lock:
        active_connections.remove(conn_info)
    
    connection.close()

def send_to_client(connection, msg):
    """Send a message to a specific client"""
    try:
        message = msg.encode(FORMAT)
        message_length = len(message)
        send_length = str(message_length).encode(FORMAT)
        send_length += b' ' * (HEADER - len(send_length))
        connection.send(send_length)
        connection.send(message)
        return True
    except Exception as e:
        print(f"[ERROR] Failed to send message: {e}")
        return False

def broadcast_message(msg, sender_connection=None):
    """Send a message to all connected clients (except sender)"""
    with connections_lock:
        disconnected = []
        for conn_info in active_connections:
            if conn_info['connection'] != sender_connection:
                if not send_to_client(conn_info['connection'], msg):
                    disconnected.append(conn_info)
        
        # Remove disconnected clients
        for conn_info in disconnected:
            active_connections.remove(conn_info)
            print(f"[CLEANUP] Removed disconnected client {conn_info['address']}")


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