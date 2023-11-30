import socket
import threading
import tkinter as tk
from tkinter.font import Font
from tkinter import scrolledtext
from tkinter import messagebox

# Creation of the UI
root = tk.Tk()
root.geometry("550x600")
root.title("Chat Application")
root.resizable(False, False)

# Fonts and colors for the UI
WHITE = "#ffffff"
DARK_GRAY = "#2d3142"
GRAY = "#bfc0c0"
ORANGE = "#ef8354"
DARK_BLUE = "#4f5d75"
FONT = Font(family="Comfortaa", size=20)
BUTTON_FONT = Font(family="Comfortaa", size=14)
SMALL_FONT = Font(family="Comfortaa", size=13)

HOST = '127.0.0.1'
PORT = 3333

# Socket class object
# AF_INET is for IPv4
# SOCK_STREAM is for TCP protocol (preferred for an application like this)
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def add_message(message):
    message_box.config(state=tk.NORMAL)
    message_box.insert(tk.END, message + '\n')
    message_box.config(state=tk.NORMAL)


def connect():
    try:
        # Try connecting to the server
        client.connect((HOST, PORT))
        print("Connection successful")
        add_message("[SERVER] Connection successful")

        # Send the client username to the server
        username = username_tb.get()
        if username != '':
            client.send(username.encode())
        else:
            messagebox.showerror("Invalid username", "Empty is not a valid username")
            return

        threading.Thread(target=listener, args=(client,)).start()

        # Disable UI elements after successful connection
        username_tb.config(state=tk.DISABLED)
        join_button.config(state=tk.DISABLED)
    except Exception as e:
        messagebox.showerror("Unable to connect to server", f"Unable to connect {HOST} {PORT}. Error: {str(e)}")


def send():
    message = message_tb.get()
    if message != '':
        client.sendall(message.encode())
        message_tb.delete(0, len(message))
    else:
        messagebox.showerror("Error", "Empty message")


# Row configuration for specific width and height of frames
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=4)
root.grid_rowconfigure(2, weight=1)

# Customization of the UI
top_frame = tk.Frame(root, width=550, height=100, bg=GRAY)
top_frame.grid(row=0, column=0, sticky=tk.NSEW)

middle_frame = tk.Frame(root, width=550, height=400, bg=GRAY)
middle_frame.grid(row=1, column=0, sticky=tk.NSEW)

bottom_frame = tk.Frame(root, width=550, height=100, bg=GRAY)
bottom_frame.grid(row=2, column=0, sticky=tk.NSEW)

username_label = tk.Label(top_frame, text="Enter Username:", font=FONT, bg=GRAY, fg=DARK_BLUE)
username_label.pack(side=tk.LEFT, padx=10)

username_tb = tk.Entry(top_frame, font=SMALL_FONT, bg=WHITE, fg=DARK_BLUE, width=25)
username_tb.pack(side=tk.LEFT)

join_button = tk.Button(top_frame, text="Join Server", font=BUTTON_FONT, highlightbackground=ORANGE,
                        bg=DARK_BLUE, fg=DARK_GRAY, command=connect)
join_button.pack(side=tk.LEFT, padx=15)

message_tb = tk.Entry(bottom_frame, font=SMALL_FONT, bg=WHITE, fg=DARK_BLUE, width=48)
message_tb.pack(side=tk.LEFT, padx=10)

message_button = tk.Button(bottom_frame, text="Send", font=BUTTON_FONT, highlightbackground=ORANGE,
                           bg=DARK_BLUE, fg=DARK_GRAY, command=send)
message_button.pack(side=tk.LEFT, padx=5)

message_box = scrolledtext.ScrolledText(middle_frame, font=SMALL_FONT, bg=ORANGE, fg=DARK_BLUE,
                                        width=76, height=23)
message_box.config(state=tk.DISABLED)
message_box.pack(side=tk.TOP)


# Function that will listen for messages from the server
def listener(client):
    while 1:
        try:
            msg = client.recv(2048).decode('utf-8')
            if not msg:
                print("Server disconnected.")
                messagebox.showinfo("Disconnected", "Disconnected from the server.")
                break
            if msg.startswith("[SERVER]"):
                add_message(msg)
            else:
                parts = msg.split("->")
                if len(parts) >= 2:
                    username = parts[0]
                    message = '->'.join(parts[1:])
                    add_message(f"[{username}] {message}")
                else:
                    print("Invalid message format received:", msg)
        except socket.error as e:
            print(f"Error reading data: {e}")
            messagebox.showerror("Error", f"Error reading data from the server: {e}")
            break




# Main function for client
def main():
    try:
        root.mainloop()
    except KeyboardInterrupt:
        print("Exiting the chat application.")
        client.close()


if __name__ == "__main__":
    main()
