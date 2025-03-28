import os
import tkinter as tk
from tkinter import scrolledtext
import tkinter.simpledialog
import socket
from threading import Thread, Lock


class ServerGui:
    def __init__(self, master: tk.Tk):
        self.server = None
        self.log_area = None
        self.button_clients = None
        self.clear_history = None

        self.clients = []
        self.banned_clients = []
        self.lock = Lock()
        self.chat_history = []
        self.master = master
        self.master.title("Chat server")

        self.ip, self.port = self.prompt_server()

        self.start_button = tk.Button(master, text="Start Server", command=self.start_button_pressed)
        self.start_button.pack(side=tk.BOTTOM)
        self.parse_ban_list()

    def start_button_pressed(self):
        self.start_button.destroy()
        self.log_area = scrolledtext.ScrolledText(self.master, wrap="word", width=100, height=20)
        self.log_area.pack(padx=10, pady=10)
        self.log_area.config(state="disabled")

        self.clear_history = tk.Button(self.master, text="Clear History", command=lambda: self.chat_history.clear())
        self.clear_history.pack(side=tk.BOTTOM)

        self.button_clients = tk.Button(self.master, text="Clients", command=self.show_clients)
        self.button_clients.pack(side=tk.BOTTOM)

        server_handler = Thread(target=self.start_server, args=(self.ip, int(self.port)))
        server_handler.start()
        self.log(f"Server started on {self.ip}:{self.port}")

    def show_clients(self):
        client_window = tk.Toplevel(self.master)
        client_window.title("Connected Clients")

        for client in self.clients:
            client_frame = tk.Frame(client_window)
            client_frame.pack(fill=tk.X, padx=10, pady=5)

            client_label = tk.Label(client_frame, text=str(client.getpeername()))
            client_label.pack(side=tk.LEFT)

            disconnect_button = tk.Button(client_frame, text="Disconnect",
                                          command=lambda c=client: self.disconnect_client(c))
            disconnect_button.pack(side=tk.LEFT, padx=5)

            ban_button = tk.Button(client_frame, text="Ban", command=lambda c=client: self.ban_client(c))
            ban_button.pack(side=tk.LEFT, padx=5)

    def disconnect_client(self, client):
        client.send("You are disconnected by the server".encode())
        self.clients.remove(client)
        self.log(f"Client {client.getpeername()} disconnected")
        client.close()

    def ban_client(self, client):
        client.send("You are banned by the server".encode())
        self.banned_clients.append(client.getpeername())

        with open("banned.txt", "w") as f:
            f.write(f"{client.getpeername()[0]}\n")

        self.log(f"Client {client.getpeername()} banned")
        self.disconnect_client(client)

    def start_server(self, ip: str, port: int) -> None:
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((ip, port))
        self.server.listen(5)
        while True:
            client_socket, addr = self.server.accept()

            self.log(f"Client connected from {addr}")

            client_handler = Thread(target=self.handle_client, args=(client_socket, addr))
            client_handler.start()

    def log(self, message: str) -> None:
        self.log_area.config(state="normal")
        self.log_area.insert(tk.END, message + "\n")
        self.log_area.config(state="disabled")
        self.log_area.see(tk.END)

    def handle_client(self, client_socket, addr):

        if addr[0] in self.banned_clients:
            client_socket.send("You are banned by the server".encode())
            client_socket.close()
            return

        self.clients.append(client_socket)
        try:
            while True:
                message = client_socket.recv(1024).decode()
                if not message:
                    break

                if message == "history":
                    with self.lock:

                        history = "\n".join(self.chat_history) + "\n"
                        self.log(f"Sending chat history to client({addr})")
                        client_socket.send(history.encode())

                else:
                    with self.lock:
                        self.chat_history.append(message)
                    self.broadcast(message)
        except ConnectionResetError:
            print(f"Connection with {addr} was reset.")
        finally:
            self.clients.remove(client_socket)
            client_socket.close()

    @staticmethod
    def prompt_server():
        ip = tk.simpledialog.askstring("Server IP", "Enter server IP to start")
        port = tk.simpledialog.askinteger("Server Port", "Enter server port to start")
        return ip, port

    def broadcast(self, message):
        with self.lock:
            for client in self.clients:
                client.send(message.encode())

    def parse_ban_list(self):

        if not os.path.exists("banned.txt"):
            with open("banned.txt", "w") as f:
                f.write("")
                return

        with open("banned.txt", "r") as f:
            for line in f:
                self.banned_clients.append(line.strip())


if __name__ == "__main__":
    root = tk.Tk()
    server = ServerGui(root)
    root.mainloop()
