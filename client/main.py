import socket
import select
from threading import Thread


def receive_messages(client: socket.socket) -> None:
    client.settimeout(1)
    while True:
        try:
            message = client.recv(1024).decode()
            if message:
                print(message)
                print("> ", end="", flush=True)
            else:
                break
        except (ConnectionResetError, socket.timeout):
            continue
            


def connect_to_server(ip: str, port: int) -> None:
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client.connect((ip, port))
    except ConnectionRefusedError:
        print("Could not connect to server. Make sure the server is running.")
        return

    print(f"Connected to server {ip}:{port}")

    receive_thread = Thread(target=receive_messages, args=(client,))
    receive_thread.start()

    while True:
        user_input = handle_user_input()
        if user_input == 1:
            view_chat_history(client)
        elif user_input == 2:
            send_message(client, ip)
        elif user_input == 3:
            disconnect_from_server(client)
            break


def handle_user_input() -> int:
    while True:
        try:
            user_input = int(input("1. View history\n2. Send message\n3. Disconnect\n> "))
            if user_input in [1, 2, 3]:
                return user_input
            else:
                print("Invalid option. Please enter 1, 2, or 3.")
        except ValueError:
            print("Invalid input. Please enter a number.")


def send_message(client: socket.socket, ip: str) -> None:
    message = ip + ": " + input("Message: ") + "\n"
    client.send(message.encode())


def send_message_blank(client: socket.socket) -> None:
    message = ""
    client.send(message.encode())


def view_chat_history(client: socket.socket) -> None:
    try:
        send_message_blank(client)
        # Notify the server to send chat history
        message = "SEE CHAT HISTORY"
        client.send(message.encode())

        full_history = ""
        while True:
            chunk = client.recv(1024).decode()
            if not chunk:
                break
            full_history += chunk
            if "END CHAT HISTORY" in full_history:
                break
            else:
                print("Timeout: No data received from server.")
                break

        full_history = full_history.replace("END CHAT HISTORY", "").strip()
        print("\n--- Chat History ---")
        print(full_history)
        print("--------------------\n")
    except ConnectionResetError:
        print("Connection lost while fetching history.")
    except Exception as e:
        print(f"An error occurred: {e}")


def disconnect_from_server(client: socket.socket) -> None:
    client.close()


if __name__ == "__main__":
    connect_to_server('localhost', 8080)
