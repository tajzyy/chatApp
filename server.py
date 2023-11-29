import socket
import threading

HOST = '127.0.0.1'
PORT = 4444
LIMIT = 4
# List of active clients
active_clients = []


# Function listens for messages from client
def listener(username, client):
    while 1:
        # Decode the message sent from client
        message = client.recv(2048).decode('utf-8')
        if message != '':
            # Formatting the message
            msg = username + '->' + message
            global_message(msg)

        else:
            print(f"Empty message from {username}")


# Function to handle the client
def client_h(client):
    # Username to server
    while 1:
        # Decode the message sent from client
        username = client.recv(2048).decode('utf-8')
        if username != '':
            # Add username and client object to active_clients
            # if there is a valid username
            active_clients.append((username, client))
            prompt_message = "Server->" + f"{username} joined the chat"
            global_message(prompt_message)
            break
        else:
            print("Username is empty")

    threading.Thread(target=listener, args=(username, client,)).start()


# Function that sends message to all connected clients
def global_message(message):
    for user in active_clients:
        client_message(user[1], message)


# Function to send message to specific user
def client_message(client, message):
    client.sendall(message.encode())


# Main function for server
def main():
    # Socket class object
    # AF_INET is for IPv4
    # SOCK_STREAM is for TCP protocol (preferred for an application like this)
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Try catch for connecting to server
    try:
        # Providing host IP and port for server
        server.bind((HOST, PORT))
        print(f"Server running on {HOST} {PORT}")
    except:
        print(f"Unable to connect to host: {HOST} and port {PORT}")

    # Server limit
    server.listen(LIMIT)

    # While loop keeps listening for client connections
    while 1:
        client, address = server.accept()
        print(f"Connection successful {address[0]} {address[1]}")

        threading.Thread(target=client_h, args=(client,)).start()


if __name__ == "__main__":
    main()
