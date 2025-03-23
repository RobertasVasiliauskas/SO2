import socket
from threading import Thread

def handle_client(client_socket: socket.socket, addr: tuple) -> None:
    print(f"Connection from {addr}")
    try:
        while True:
            message = client_socket.recv(1024).decode()
            if not message:
                break
            print(f"Received message: {message}")
    except ConnectionResetError:
        print(f"Connection with {addr} was reset.")
    finally:
        client_socket.close()

def run_server(port: int) -> None:
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('localhost', port))
    server.listen(5)
    print(f"Server started on port {port}")

    while True:
        client_socket, addr = server.accept()
        client_handler = Thread(target=handle_client, args=(client_socket, addr))
        client_handler.start()

if __name__ == "__main__":
    run_server(8080)