import tkinter as tk
from tkinter import scrolledtext
import tkinter.simpledialog
import socket
import threading

class ChatClientGUI:

    username = None

    def __init__(self, master: tk.Tk, server_ip: str, server_port: int):
        self.master = master
        self.master.title("Chat Client")

        self.username = self.prompt_username()
        if not self.username:
            master.destroy()
            return

        self.chat_area = scrolledtext.ScrolledText(master, wrap='word', width=50, height=15)
        self.chat_area.pack(padx=10, pady=10)
        self.chat_area.config(state='disabled')

        self.entry_field = tk.Entry(master, width=40)
        self.entry_field.pack(side=tk.LEFT, padx=5)
        self.entry_field.bind("<Return>", self.send_message)

        self.send_button = tk.Button(master, text="Send", command=self.send_message)
        self.send_button.pack(side=tk.LEFT)

        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((server_ip, server_port))

        threading.Thread(target=self.receive_messages, daemon=True).start()

    def receive_messages(self):
        while True:
            try:
                data = self.client_socket.recv(1024).decode()
                if not data:
                    break
                self.display_message(data)
            except ConnectionResetError:
                break

    def display_message(self, msg: str):
        self.chat_area.config(state='normal')
        self.chat_area.insert(tk.END, msg + "\n")
        self.chat_area.config(state='disabled')
        self.chat_area.see(tk.END)

    def send_message(self, event=None):
        message = f"{self.username}: {self.entry_field.get().strip()}"
        if message:
            self.client_socket.send(message.encode())
            self.entry_field.delete(0, tk.END)

    @staticmethod
    def prompt_username() -> str:
        return tk.simpledialog.askstring("Username", "Enter your username:")

def main():
    root = tk.Tk()
    app = ChatClientGUI(root, 'localhost', 8080)
    root.mainloop()

if __name__ == "__main__":
    main()