import socket
import threading
import time

# constants
HOST = ""
PORT = 8080

# all clients data
client_usernames = {}

def get_timestamp():
    utc_struct = time.gmtime()
    formatted_utc = time.strftime("%Y-%m-%d %H:%M:%S", utc_struct)
    return formatted_utc


# broadcast messages to everyone
def broadcast_message(message, sender_socket):
    disconnected_clients = []  # Collect dead clients first
    for client_socket in client_usernames:
        if client_socket != sender_socket:
            try:
                full_message = f"[{get_timestamp()}] {message}"
                client_socket.sendall(full_message.encode())
            except:
                disconnected_clients.append(client_socket)
                
    # Remove after iteration is done
    for client in disconnected_clients:
        if client in client_usernames:
            del client_usernames[client]
            client.close()


def handle_commands(message, sender):
    if message.startswith("/"):
        
        message_list = message.split(" ")
        if message.lower() == "/users":  # ✓ Added parentheses
            users = list(client_usernames.values())  # Convert to list
            users_list = ", ".join(users)  # Format nicely
            sender.sendall(f"[{get_timestamp()}] Online users: {users_list}".encode())
        
        elif message.lower() == "/help":
            help_text = """=== CHAT COMMANDS ===
            /help  - Show this help message
            /users - List all online users
            /msg <username> <message> - Send private message
            /quit  - Leave the chat

            Examples:
            /msg Alice Hello there!

            Type any message to broadcast to everyone"""
            sender.sendall(help_text.encode())
            
        elif message.lower().startswith("/msg"):
            if len(message_list) < 3:
                sender.sendall("Usage: /msg <username> <message>".encode())
                return
            target_name = message_list[1]
            private_message = " ".join(message_list[2:])
            
            target_socket = None
            sender_username = None
            
            for sock, name in client_usernames.items():
                if name == target_name:
                    target_socket = sock
                if sock == sender:
                    sender_username = name
                
            if target_socket:
                try:
                    target_socket.sendall(f"[{get_timestamp()}] [Private from {sender_username}]: {private_message}".encode())
                    sender.sendall(f"[{get_timestamp()}] [Private to {target_name}]: {private_message}".encode())
                except:
                    sender.sendall(f"[{get_timestamp()}] Error: Could not send message to {target_name}".encode())
            else:
                sender.sendall(f"[{get_timestamp()}] Error: User '{target_name}' not found".encode())
        
        elif message.lower() == "/quit":
            return True  # Signal to disconnect
        return True
    return False


            
            


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
            is_command = handle_commands(message, active_client)
            if is_command and message.lower() == "/quit":
                break
            if not is_command:
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
        conn, addr = server.accept()
        threading.Thread(target=handle_client, args=(conn,)).start()
