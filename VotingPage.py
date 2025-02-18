import tkinter as tk
from tkinter import *
from PIL import ImageTk, Image
import threading
import time

# Custom colors and fonts
BG_COLOR = "#f0f0f0"
BUTTON_COLOR = "#4CAF50"
TEXT_COLOR = "#333333"
FONT = ("Helvetica", 12)
HEADER_FONT = ("Helvetica", 18, "bold")

def voteCast(root, frame1, vote, client_socket):
    for widget in frame1.winfo_children():
        widget.destroy()

    # Show loading spinner
    loading_label = Label(frame1, text="Processing your vote...", font=FONT, bg=BG_COLOR)
    loading_label.grid(row=1, column=1, pady=20)
    root.update()

    client_socket.send(vote.encode())  # Send vote to server

    message = client_socket.recv(1024)  # Receive success message
    print(message.decode())
    message = message.decode()

    # Remove loading spinner
    loading_label.destroy()

    if message == "Successful":
        Label(frame1, text="✅ Vote Casted Successfully", font=FONT, bg=BG_COLOR, fg="green").grid(row=1, column=1, pady=20)
    else:
        Label(frame1, text="❌ Vote Cast Failed... Try again", font=FONT, bg=BG_COLOR, fg="red").grid(row=1, column=1, pady=20)

    client_socket.close()
    root.after(3000, root.destroy)  # Close the window after 3 seconds

def countdown_timer(root, frame1, timer_label, duration):
    for remaining in range(duration, -1, -1):
        if not threading.main_thread().is_alive():  # Stop if the main thread is closed
            return
        mins, secs = divmod(remaining, 60)
        timer_label.config(text=f"⏳ Time Left: {mins:02}:{secs:02}")
        time.sleep(1)
    # Timer expired
    Label(frame1, text="⏰ Time's up! Voting session closed.", font=FONT, bg=BG_COLOR, fg="red").grid(row=8, column=1, pady=20)
    root.after(3000, root.destroy)  # Close the window after 3 seconds

def votingPg(root, frame1, client_socket):
    root.title("Cast Your Vote")
    root.configure(bg=BG_COLOR)
    for widget in frame1.winfo_children():
        widget.destroy()

    # Header
    Label(frame1, text="Cast Your Vote", font=HEADER_FONT, bg=BG_COLOR, fg=TEXT_COLOR).grid(row=0, column=1, pady=10)

    # Add countdown timer label
    timer_label = Label(frame1, text="⏳ Time Left: 02:00", font=FONT, bg=BG_COLOR, fg=TEXT_COLOR)
    timer_label.grid(row=1, column=2, pady=10)

    # Start the countdown timer in a separate thread
    countdown_duration = 120  # 2 minutes
    threading.Thread(target=countdown_timer, args=(root, frame1, timer_label, countdown_duration), daemon=True).start()

    vote = StringVar(frame1, "-1")

    # Voting options
    parties = [
        ("JVP", "Anura Dissanayaka", "img/Malimawa.jpg"),
        ("SLPP", "Mahinda Rajapaksha", "img/slpp.png"),
        ("SJB", "Sajith Premadasa", "img/sjb.png"),
        ("UNP", "Ranil Wikkramasingha", "img/unp.png"),
        ("TNA", "R. Sampanthan", "img/tna.png"),
        ("NOTA", "None of the Above", "img/nota.jpg")
    ]

    for i, (party, candidate, image_path) in enumerate(parties):
        try:
            logo = ImageTk.PhotoImage(Image.open(image_path).resize((50, 50), Image.LANCZOS))
            party_logo = Label(frame1, image=logo, bg=BG_COLOR)
            party_logo.image = logo  # Keep a reference to avoid garbage collection
            party_logo.grid(row=i + 2, column=0, padx=10, pady=5)
        except FileNotFoundError:
            print(f"Warning: Image {image_path} not found.")

        Radiobutton(
            frame1,
            text=f"{party}\n{candidate}",
            variable=vote,
            value=party.lower(),
            indicator=0,
            height=3,
            width=20,
            bg=BUTTON_COLOR,
            fg="white",
            selectcolor="#45a049",
            font=FONT,
            command=lambda v=party.lower(): voteCast(root, frame1, v, client_socket)
        ).grid(row=i + 2, column=1, padx=10, pady=5)

    frame1.pack()
    root.mainloop()