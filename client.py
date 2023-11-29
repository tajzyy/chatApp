import socket
import threading
import tkinter

HOST = '127.0.0.1'
PORT = 4444


# Function that will listen for messages from the server
def listener(client):
    while 1:
        msg = client.recv(2048).decode('utf-8')
        if msg != '':
            username = msg.split("->")[0]
            message = msg.split("->")[1]
            print(f"[{username}] {message}")
        else:
            print(f"Message received from server is empty")


# Function that will communicate with the server
def communicate(client):
    # Send the client username to the server
    username = input("Please enter your username-> ")
    if username != '':
        client.send(username.encode())
    else:
        print("Empty is not a valid username")
        exit(0)

    threading.Thread(target=listener, args=(client, )).start()

    send_message(client)


# Function for sending messages to server
def send_message(client):
    while 1:
        msg = input("Message-> ")
        if msg != '':
            client.sendall(msg.encode())
        else:
            print("Empty message")
            exit(0)


# Main function for client
def main():
    # Socket class object
    # AF_INET is for IPv4
    # SOCK_STREAM is for TCP protocol (preferred for an application like this)
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Try connecting to the server
    try:
        # Providing host IP and port for server
        client.connect((HOST, PORT))
        print("Connection successful")
    except:
        print(f"Unable to connect {HOST} {PORT}")

    communicate(client)


if __name__ == "__main__":
    main()
