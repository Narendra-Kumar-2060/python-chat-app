import socket
import threading
import sys
import time

HOST = "127.0.0.1"
PORT = 8080

print_lock = threading.Lock()


def receive_messages(client):
    while True:
        try:
            msg = client.recv(1024).decode()
            if msg:

                print_lock.acquire()
                try:

                    sys.stdout.write("\r" + " " * 80 + "\r")

                    print(msg)

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
    connected = False
    for attempt in range(5):
        try:
            client.connect((HOST, PORT))
            connected = True
            break
        except:
            print(f"Connecting... (attempt {attempt+1}/5)")
            time.sleep(2)

    if not connected:
        print("Cannot connect to server")
        sys.exit(1)

    username = input("Enter your name: ")
    client.sendall(username.encode())
    threading.Thread(target=receive_messages, args=(client,), daemon=True).start()
    while True:
        text = input("> ")

        if not text or text.strip() == "":
            continue

        if text.lower() == "/quit":
            try:
                client.sendall(text.encode())
                time.sleep(0.1)
            except:
                pass
            print("Goodbye!")
            client.close()
            sys.exit(0)
        try:
            client.sendall(text.encode())
        except:
            break
