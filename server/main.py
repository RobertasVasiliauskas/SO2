import socket
from threading import Thread

chat_history = []

def handle_client(client_socket: socket.socket, addr: tuple) -> None:
    print(f"Connection from {addr}")
    try:
        while True:
            message = client_socket.recv(1024).decode()
            if not message:
                break

            if message == "SEE CHAT HISTORY":
                for chat in chat_history:
                    print(chat)
                    client_socket.send(chat.encode())

                client_socket.send("END CHAT HISTORY".encode())
            else:
                chat_history.append(message)
    except ConnectionResetError:
        print(f"Connection with {addr} was reset.")
    finally:
        client_socket.close()

def run_server(ip: str, port: int) -> None:
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('localhost', port))
    server.listen(5)
    print(f"Server started on port {port}")

    while True:
        client_socket, addr = server.accept()
        client_handler = Thread(target=handle_client, args=(client_socket, addr))
        client_handler.start()

if __name__ == "__main__":
    run_server('localhost', 8083)