import tkinter as tk
from tkinter import *
from VotingPage import votingPg
import socket

def establish_connection(server_ip):
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.settimeout(5)  # Set a timeout for the connection
        print(f"Attempting to connect to {server_ip}:4001...")
        client_socket.connect((server_ip, 4001))  # Connect to the server's IP and port
        message = client_socket.recv(1024)  # Receive connection confirmation
        if message.decode() == "Connection Established":
            print("Connected to the server!")
            return client_socket
        else:
            print("Connection failed: Invalid response from server.")
            return None
    except socket.timeout:
        print("Connection failed: Timed out. Ensure the server is running and the IP is correct.")
        return None
    except Exception as e:
        print(f"Connection failed: {e}")
        return None

def voterLogin(root, frame1):
    # Replace with the server's IP address
    server_ip = "192.168.244.229"  # Change this to the actual server IP

    # Establish connection to the server
    client_socket = establish_connection(server_ip)

    if not client_socket:
        failed_return(root, frame1, None, "Connection failed")
        return

    root.title("Voter Login")
    for widget in frame1.winfo_children():
        widget.destroy()

    Label(frame1, text="Voter Login", font=('Helvetica', 18, 'bold')).grid(row=0, column=2, rowspan=1)
    Label(frame1, text="").grid(row=1, column=0)
    Label(frame1, text="Voter ID:      ", anchor="e", justify=LEFT).grid(row=2, column=0)
    Label(frame1, text="Password:   ", anchor="e", justify=LEFT).grid(row=3, column=0)

    voter_ID = tk.StringVar()
    password = tk.StringVar()

    e1 = Entry(frame1, textvariable=voter_ID)
    e1.grid(row=2, column=2)
    e3 = Entry(frame1, textvariable=password, show='*')
    e3.grid(row=3, column=2)

    sub = Button(frame1, text="Login", width=10, command=lambda: log_server(root, frame1, client_socket, voter_ID.get(), password.get()))
    Label(frame1, text="").grid(row=4, column=0)
    sub.grid(row=5, column=3, columnspan=2)

    frame1.pack()
    root.mainloop()

def log_server(root, frame1, client_socket, voter_ID, password):
    if not (voter_ID and password):
        voter_ID = "0"
        password = "x"

    message = voter_ID + " " + password
    client_socket.send(message.encode())  # Send voter details to server

    message = client_socket.recv(1024)  # Receive authentication response
    message = message.decode()

    if message == "Authenticate":
        votingPg(root, frame1, client_socket)  # Proceed to voting page
    elif message == "VoteCasted":
        failed_return(root, frame1, client_socket, "Vote has Already been Cast")
    elif message == "InvalidVoter":
        failed_return(root, frame1, client_socket, "Invalid Voter")
    else:
        failed_return(root, frame1, client_socket, "Server Error")

def failed_return(root, frame1, client_socket, message):
    for widget in frame1.winfo_children():
        widget.destroy()
    message = message + "... \nTry again..."
    Label(frame1, text=message, font=('Helvetica', 12, 'bold')).grid(row=1, column=1)
    try:
        if client_socket:
            client_socket.close()
    except:
        return

# Example usage
# if __name__ == "__main__":
#     root = Tk()
#     root.geometry('500x500')
#     frame1 = Frame(root)
#     voterLogin(root, frame1)