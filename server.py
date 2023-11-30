import socket
import threading

HOST = '127.0.0.1'
PORT = 3333
LIMIT = 4
active_clients = []
server_lock = threading.Lock()


def listener(username, client):
    while True:
        try:
            message = client.recv(2048).decode('utf-8')
            if not message:
                print(f"{username} disconnected.")
                prompt_message = "[SERVER]" + f"{username} left the chat"
                with server_lock:
                    global_message(prompt_message)
                    active_clients.remove((username, client))
                break
            else:
                msg = username + '->' + message
                with server_lock:
                    global_message(msg)
        except socket.error as e:
            print(f"Error reading data from {username}: {e}")
            with server_lock:
                active_clients.remove((username, client))
            break


def client_h(client):
    try:
        username = client.recv(2048).decode('utf-8')
        if username != '':
            with server_lock:
                active_clients.append((username, client))
                prompt_message = "[SERVER]" + f"{username} joined the chat"
                global_message(prompt_message)
        else:
            print("Username is empty")

        threading.Thread(target=listener, args=(username, client,)).start()
    except Exception as e:
        print(f"Error handling client: {str(e)}")
        client.close()


def global_message(message):
    for user in active_clients:
        client_message(user[1], message)


def client_message(client, message):
    try:
        client.sendall(message.encode())
    except Exception as e:
        print(f"Error sending message to client: {str(e)}")
        with server_lock:
            active_clients.remove((username, client))
        client.close()


def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        server.bind((HOST, PORT))
        print(f"Server running on {HOST} {PORT}")
    except Exception as e:
        print(f"Unable to connect to host: {HOST} and port {PORT}. Error: {str(e)}")

    server.listen(LIMIT)

    while True:
        client, address = server.accept()
        print(f"Connection successful {address[0]} {address[1]}")

        threading.Thread(target=client_h, args=(client,)).start()


if __name__ == "__main__":
    main()
