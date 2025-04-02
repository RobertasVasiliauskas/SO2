# Server and Client Chat Application

## Overview

The Operating system 2-second project is a chat server and client application implemented in Python using the Tkinter library for the
graphical user interface. The server allows multiple clients to connect, send messages, and interact in a chat room. The
server also provides functionalities for managing clients, such as disconnecting and banning users.

## Instructions for Running the Project

### Requirements

- Python 3.13 or higher

## Problem Description

The main problem addressed by this project is to create a multi-client chat application with a graphical user interface.
The server needs to handle multiple clients simultaneously, manage client connections, and provide functionalities such
as message broadcasting, client disconnection, and banning.

## Threads and Their Representations

### Server Threads

1. **Main Thread**: Manages the Tkinter GUI for the server.
2. **Server Handler Thread**: Listens for incoming client connections and starts a new thread for each client.
3. **Client Handler Threads**: Each client connection is handled by a separate thread that manages communication with
   that client.

### Client Threads

1. **Main Thread**: Manages the Tkinter GUI for the client.
2. **Message Receiver Thread**: Continuously listens for incoming messages from the server and updates the chat area.
3. **History fetching Thread**: Handles history fetching requests from the server. Thread is created on client
   connection. Threads ends when client has received all history messages.

## Critical Sections and Their Solutions

### Critical Sections

1. **Accessing the Client List**: The server maintains a list of connected clients. Access to this list must be
   synchronized to prevent race conditions when adding or removing clients.
2. **Accessing the Chat History**: The server maintains a chat history that clients can request. Access to this history
   must be synchronized to ensure consistency.

### Solutions

1. **Locks**: The server uses a `Lock` object from the `threading` module to synchronize access to the client list and
   chat history. This ensures that only one thread can modify these resources at a time.

```python
from threading import Lock


class ServerGui:
    def __init__(self, master: tk.Tk):
        self.lock = Lock()
        self.clients = []
        self.chat_history = []

    def handle_client(self, client_socket, addr):
        with self.lock:
            self.clients.append(client_socket)
        # Handle client communication
        with self.lock:
            self.clients.remove(client_socket)
```

By using locks, the server ensures that critical sections are protected, preventing data corruption and ensuring thread
safety.

### Running the Server

1. Open a terminal or command prompt.
2. Navigate to the `server` directory of the project.
3. Run the server script:
   ```sh
   python3 server_gui.py
   ```
4. A window will appear prompting you to enter the server IP and port. Enter the desired values and start the server.

### Running the Client

1. Open a terminal or command prompt.
2. Navigate to the `client` directory of the project.
3. Run the client script:
   ```sh
   python3 client_gui.py
   ```
4. A window will appear prompting you to enter your username. Enter your username to join the chat.
5. Enter the server IP and port to connect to the server.
