# Chat Application

A real-time multi-user chat application built with Python sockets. Supports public broadcasting, private messaging, and user management.

## Features

- Real-time messaging – Instant message delivery to all connected users
- Private messaging – Send direct messages to specific users
- User list – See who's currently online
- Timestamps – All messages include UTC timestamps
- Clean CLI interface – Messages don't interrupt your typing

## Commands

| Command                     | Description                 |
| --------------------------- | --------------------------- |
| `/help`                     | Show all available commands |
| `/users`                    | List all online users       |
| `/msg <username> <message>` | Send a private message      |
| `/quit`                     | Leave the chat              |

## Tech Stack

- Python 3
- Sockets (TCP)
- Threading for concurrent connections

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/chat-app.git
cd chat-app

# Run the server
python server.py

# Run clients (in separate terminals)
python client.py
```

## Usage

1. Start the server – it will listen on port 8080
2. Launch clients and enter a username when prompted
3. Start chatting!

## Example

```
> Hello everyone!
[2026-04-29 14:30:15] Alice: Hello everyone!

> /users
[2026-04-29 14:30:20] Online users: Alice, Bob, Charlie

> /msg Bob Hey Bob, how's it going?
[2026-04-29 14:30:25] [Private to Bob]: Hey Bob, how's it going?
```

## Configuration

Edit the HOST and PORT variables in both files:

```python
HOST = ""  # Use "0.0.0.0" for network access
PORT = 8080         # Change to any available port
```

## Future Improvements

- GUI version (Tkinter/PyQt)
- Message history persistence
- Room/channel support
- File sharing
- End-to-end encryption

## License

MIT
