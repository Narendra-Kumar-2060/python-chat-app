import socket
import threading
import sys
import time

# constants
HOST = "127.0.0.1"
PORT = 8080

# Create a lock object to protect printing
print_lock = threading.Lock()

# handle recieved messages
def receive_messages(client):
    while True:
        try:
            msg = client.recv(1024).decode()
            if msg:  # Only print if there's a message
                # Use try/finally to safely print
                print_lock.acquire()
                try:
                    # Clear current line
                    sys.stdout.write('\r' + ' ' * 80 + '\r')
                    # Print the message
                    print(msg)
                    # Restore the prompt
                    sys.stdout.write("> ")
                    sys.stdout.flush()
                finally:
                    print_lock.release()
        except:
            print_lock.acquire()
            try:
                print("\nDisconnected from server")
            finally:
                print_lock.release()
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
        text = input("> ")  # Shows "> " so user knows where to type
    
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
