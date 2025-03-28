import socket
from threading import Thread, Lock

chat_history = []
clients = []
lock = Lock()


def broadcast(message: str) -> None:
    with lock:
        for client in clients:
            client.send(message.encode())


def handle_client(client_socket: socket.socket, addr: tuple) -> None:
    print(f"Connection from {addr}")
    clients.append(client_socket)
    try:
        while True:
            message = client_socket.recv(1024).decode()
            if not message:
                break

            if message == "history":
                with lock:

                    history = "\n".join(chat_history) + "\n"
                    print("Sending chat history to client")
                    client_socket.send(history.encode())

            else:
                with lock:
                    chat_history.append(message)
                broadcast(message)
    except ConnectionResetError:
        print(f"Connection with {addr} was reset.")
    finally:
        clients.remove(client_socket)
        client_socket.close()


def run_server(ip: str, port: int) -> None:
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((ip, port))
    server.listen(5)
    print(f"Server started on {ip}:{port}")

    while True:
        client_socket, addr = server.accept()
        client_handler = Thread(target=handle_client, args=(client_socket, addr))
        client_handler.start()


if __name__ == "__main__":
    run_server('localhost', 8081)
