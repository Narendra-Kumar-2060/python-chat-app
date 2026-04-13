import socket
import threading

# constants
HOST = ""
PORT = 8080

# all clients data
client_usernames = {}


# broadcast messages to everyone
def broadcast_message(message, sender_socket):
    disconnected_clients = []  # Collect dead clients first
    for client_socket in client_usernames:
        if client_socket != sender_socket:
            try:
                client_socket.sendall(message.encode())
            except:
                disconnected_clients.append(client_socket)
                
    # Remove after iteration is done
    for client in disconnected_clients:
        if client in client_usernames:
            del client_usernames[client]
            client.close()

# handle client messages
def handle_client(active_client):
    try:
        username = active_client.recv(1024).decode()
        client_usernames[active_client] = username
        print(f"{username} connected")
        broadcast_message(f"{username} joined!!!", active_client)

        # Handle messages
        while True:
            data = active_client.recv(1024)
            if not data:
                break

            message = data.decode()
            print(f"{username}: {message}")
            # Broadcast message to everyone else
            broadcast_message(f"{username}: {message}", active_client)
    
    except:
        pass
    
    finally:
        # Clean up disconnected client
        if active_client in client_usernames:
            username = client_usernames[active_client]
            del client_usernames[active_client]
            print(f"{username} disconnected")
            broadcast_message(f"{username} left the chat", active_client)
        active_client.close()


if __name__ == "__main__":
    # socket setup
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    print(f"Server listening on port {PORT}...")

    # connection loop
    while True:
        print("listening for connection...")
        connected_client, addr = server.accept()
        threading.Thread(target=handle_client, args=(connected_client,)).start()
