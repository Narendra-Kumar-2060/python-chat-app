import socket
import threading
import sys
import time

# constants
HOST = "127.0.0.1"
PORT = 8080


# handle recieved messages
def receive_messages(client):
    while True:
        try:
            msg = client.recv(1024).decode()
            if msg:  # Only print if there's a message
                print(msg)
        except:
            print("Disconnected from server")
            break


if __name__ == "__main__":
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))
    username = input("Enter your name: ")
    client.sendall(username.encode())
    # Start receiving messages in background
    threading.Thread(target=receive_messages, args=(client,), daemon=True).start()
    # sending message to server
    while True:
        text = input()
    
        # Skip empty messages (just pressing Enter)
        if not text or text.strip() == '':
            continue  # Go back to the start of the loop
        
        # ... quit code
        if text.lower() == '/quit':
            try:
                client.sendall(text.encode())  # Send /quit to server
                time.sleep(0.1)  # Give time for send
            except:
                pass
            print("Goodbye!")
            client.close()
            sys.exit(0)
        try:
            client.sendall(text.encode())
        except:
            break
