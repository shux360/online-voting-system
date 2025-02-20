import tkinter as tk
from tkinter import *
from VotingPage import votingPg
import socket
BG_COLOR = "#2A3457"  
ACCENT_COLOR = "#3E4A6B" 
TEXT_COLOR = "white"
FONT_TITLE = ('Helvetica', 25, 'bold')
FONT_BUTTON = ('Helvetica', 14, 'bold')
FONT_INPUT = ('Helvetica', 12)
BTN_PADX = 20
BTN_PADY = 10
ENTRY_BG = "#F0F0F0"

def establish_connection(server_ip):
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.settimeout(10)  # Set a timeout for the connection
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
      
def failed_return(root, frame1, client_socket, message):
    for widget in frame1.winfo_children():
        widget.destroy()
    
    error_frame = Frame(frame1, bg=BG_COLOR)
    error_frame.place(relx=0.5, rely=0.5, anchor=CENTER)
    
    Label(error_frame, text="⚠️ Connection Error ⚠️", 
         font=FONT_TITLE, bg=BG_COLOR, fg="#E74C3C").pack(pady=20)
    Label(error_frame, text=message + "\nPlease try again later...", 
         font=FONT_INPUT, bg=BG_COLOR, fg=TEXT_COLOR).pack(pady=10)
    
    try:
        client_socket.close()
    except:
        pass
   
def log_server(root, frame1, client_socket, voter_ID, password):
    if not (voter_ID and password):
        voter_ID, password = "0", "x"
    
    client_socket.send(f"{voter_ID} {password}".encode())
    response = client_socket.recv(1024).decode()

    if response == "Authenticate":
        votingPg(root, frame1, client_socket)
    else:
        messages = {
            "VoteCasted": "Vote has already been cast",
            "InvalidVoter": "Invalid voter credentials",
            "default": "Server connection error"
        }
        failed_return(root, frame1, client_socket, messages.get(response, messages["default"]))


def voterLogin(root, frame1):
    server_ip = "192.168.244.229"
    client_socket = establish_connection(server_ip)
    if client_socket == 'Failed':
        failed_return(root, frame1, None, "Connection to server failed")
        return

    root.title("Voter Login")
    root.configure(bg=BG_COLOR)
    for widget in frame1.winfo_children():
        widget.destroy()

    main_frame = Frame(frame1, bg=BG_COLOR)
    main_frame.pack(expand=True, fill=BOTH)

    Label(main_frame, text="Voter Login", font=FONT_TITLE,
          bg=BG_COLOR, fg=TEXT_COLOR).pack(pady=40)

    form_frame = Frame(main_frame, bg=BG_COLOR)
    form_frame.pack(pady=20)

    labels = ["Voter ID:", "Password:"]
    entries = []

    for idx, label_text in enumerate(labels):
        Label(form_frame, text=label_text, font=FONT_BUTTON,
              bg=BG_COLOR, fg=TEXT_COLOR).grid(row=idx, column=0, padx=10, pady=10, sticky="e")

        entry = Entry(form_frame, font=FONT_INPUT, bg=ENTRY_BG,
                      width=25, relief=tk.FLAT)
        entry.grid(row=idx, column=1, padx=10, pady=10)
        entries.append(entry)

        if idx == 1:
            entry.config(show='*')

    login_btn = Button(form_frame, text="Secure Login", font=FONT_BUTTON,
                       bg="#4CAF50", fg=TEXT_COLOR, activebackground="#45a049",
                       padx=BTN_PADX, pady=BTN_PADY, width=20,
                       command=lambda: log_server(root, frame1, client_socket,
                                                  entries[0].get(), entries[1].get()))
    login_btn.grid(row=len(labels), column=0, columnspan=2, pady=30)

    form_frame.grid_columnconfigure(0, weight=1)
    form_frame.grid_columnconfigure(1, weight=1)

    Label(main_frame, text="🔒 Secured Voting System • 2023",
          bg=BG_COLOR, fg="#95A5A6", font=('Helvetica', 10)).pack(side=BOTTOM, pady=20)

    frame1.pack(expand=True, fill=BOTH)
    root.mainloop()

if __name__ == '__main__':
    root = tk.Tk()  # Initialize Tkinter root window
    frame1 = Frame(root, bg=BG_COLOR)  # Create a frame
    frame1.pack(expand=True, fill=BOTH)  # Pack the frame

    voterLogin(root, frame1)  # Call voterLogin function