import socket


def connect_to_server(ip: str, port: int) -> None:
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client.connect((ip, port))
    except ConnectionRefusedError:
        print("Could not connect to server. Make sure the server is running.")
        return

    print(f"Connected to server {ip}:{port}")

    while True:
        user_input = handle_user_input()
        if user_input == 1:
            view_chat_history(client)
        elif user_input == 2:
            send_message(client)
        elif user_input == 3:
            disconnect_from_server(client)
            break


def handle_user_input() -> int:
    while True:
        try:
            user_input = int(input("1. View history\n2. Send message\n3. Disconnect\n > "))
            if user_input in [1, 2]:
                return user_input
            else:
                print("Invalid option. Please enter 1 or 2.")
        except ValueError:
            print("Invalid input. Please enter a number.")


def send_message(client: socket.socket) -> None:
    message = input("Message: ")
    client.send(message.encode())

def view_chat_history(client: socket.socket) -> None:
    message = "SEE CHAT HISTORY"
    client.send(message.encode())

    chat_history = client.recv(1024).decode()
    print(chat_history)

def disconnect_from_server(client: socket.socket) -> None:
    client.close()


if __name__ == "__main__":
    connect_to_server('localhost', 8081)
