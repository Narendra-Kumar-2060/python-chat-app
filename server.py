import socket
import threading
import time

HOST = ""
PORT = 8080

client_usernames = {}
clients_lock = threading.Lock()


def get_timestamp():
    utc_struct = time.gmtime()
    formatted_utc = time.strftime("%Y-%m-%d %H:%M:%S", utc_struct)
    return formatted_utc


def broadcast_message(message, sender_socket):
    disconnected_clients = []
    with clients_lock:
        for client_socket in list(client_usernames.keys()):
            if client_socket != sender_socket:
                try:
                    full_message = f"[{get_timestamp()}] {message}"
                    client_socket.sendall(full_message.encode())
                except Exception:
                    disconnected_clients.append(client_socket)

        for client in disconnected_clients:
            if client in client_usernames:
                del client_usernames[client]
                client.close()


def handle_commands(message, sender):
    if message.startswith("/"):
        message_list = message.split(" ")
        if message.lower() == "/users":
            with clients_lock:
                users = list(client_usernames.values())
            users_list = ", ".join(users)
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
            sender.sendall(f"[{get_timestamp()}] {help_text}".encode())

        elif message.lower().startswith("/msg"):
            if len(message_list) < 3:
                sender.sendall(b"Usage: /msg <username> <message>")
                return
            target_name = message_list[1]
            private_message = " ".join(message_list[2:])

            target_socket = None
            sender_username = None
            with clients_lock:
                for sock, name in client_usernames.items():
                    if name == target_name:
                        target_socket = sock
                    if sock == sender:
                        sender_username = name

            if target_socket:
                try:
                    target_socket.sendall(
                        f"[{get_timestamp()}] [Private from {sender_username}]: {private_message}".encode()
                    )
                    sender.sendall(
                        f"[{get_timestamp()}] [Private to {target_name}]: {private_message}".encode()
                    )
                except Exception:
                    sender.sendall(
                        f"[{get_timestamp()}] Error: Could not send message to {target_name}".encode()
                    )
            else:
                sender.sendall(
                    f"[{get_timestamp()}] Error: User '{target_name}' not found".encode()
                )

        elif message.lower() == "/quit":
            return True
        return True
    return False


def handle_client(active_client):
    username = None
    try:
        username = active_client.recv(1024).decode().strip()
        with clients_lock:
            if not username or username in client_usernames.values():
                active_client.sendall(b"Username taken! Disconnecting.")
                active_client.close()
                return
            # Registered inside the same locked block as the check above,
            # so two clients connecting at the same instant can't both
            # claim the same name in the gap between check and set.
            client_usernames[active_client] = username
        print(f"{username} connected")
        broadcast_message(f"{username} joined!!!", active_client)

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

    except Exception:
        pass

    finally:
        was_registered = False
        with clients_lock:
            if active_client in client_usernames:
                username = client_usernames[active_client]
                del client_usernames[active_client]
                was_registered = True
        if was_registered:
            print(f"{username} disconnected")
            broadcast_message(f"{username} left the chat", active_client)
        active_client.close()


if __name__ == "__main__":
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    print(f"Server listening on port {PORT}...")

    while True:
        print("listening for connection...")
        conn, addr = server.accept()
        threading.Thread(target=handle_client, args=(conn,)).start()
