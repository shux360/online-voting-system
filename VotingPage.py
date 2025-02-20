import threading
import time
import tkinter as tk
from tkinter import *
from PIL import ImageTk, Image

# ================== STYLING CONSTANTS ==================
BG_COLOR = "#2A3457"  # Dark blue background
BUTTON_BG = "#4CAF50"  # Green buttons
TEXT_COLOR = "white"
FONT_TITLE = ('Helvetica', 24, 'bold')
FONT_BUTTON = ('Helvetica', 12, 'bold')
PARTY_COLOR = "#3E4A6B"  # Party button background
ACTIVE_COLOR = "#4E5A7B"  # Active button color
# ========================================================

def voteCast(root, frame1, vote, client_socket):
    for widget in frame1.winfo_children():
        widget.destroy()

    client_socket.send(vote.encode())
    message = client_socket.recv(1024).decode()

    result_frame = Frame(frame1, bg=BG_COLOR)
    result_frame.place(relx=0.5, rely=0.5, anchor=CENTER)

    if message == "Successful":
        Label(result_frame, text="✅ Vote Cast Successfully", font=FONT_TITLE,
              bg=BG_COLOR, fg=BUTTON_BG).pack(pady=20)
        root.after(2000, root.destroy)  # Close the window after 2 seconds
    else:
        Label(result_frame, text="❌ Vote Failed - Try Again", font=FONT_TITLE,
              bg=BG_COLOR, fg="#E74C3C").pack(pady=20)

def closeApplication(root, client_socket):
    try:
        client_socket.close()
    except:
        pass
    root.destroy()

def countdown_timer(root, frame1, timer_label, duration):
    def update_timer(remaining):
        if remaining >= 0:
            mins, secs = divmod(remaining, 60)
            timer_label.config(text=f"⏳ Time Left: {mins:02}:{secs:02}")
            root.after(1000, update_timer, remaining - 1)
        else:
            timer_label.config(text="⏰ Time's up! Voting session closed.", fg="red")
            root.after(3000, lambda: closeApplication(root, None))

    update_timer(duration)


def votingPg(root, frame1, client_socket):
    root.title("Cast Your Vote")
    root.configure(bg=BG_COLOR)
    for widget in frame1.winfo_children():
        widget.destroy()

    # Store image references
    image_refs = []

    # Main container
    main_frame = Frame(frame1, bg=BG_COLOR)
    main_frame.pack(expand=True, fill=BOTH)

    # Header
    Label(main_frame, text="Select Your Preferred Party", font=FONT_TITLE,
         bg=BG_COLOR, fg=TEXT_COLOR).pack(pady=20)

    # Timer label
    timer_label = Label(main_frame, text="⏳ Time Left: 01:00", font=FONT_BUTTON, bg=BG_COLOR, fg=TEXT_COLOR)
    timer_label.pack(pady=5)

    # Start the countdown timer in a separate thread
    threading.Thread(target=countdown_timer, args=(root, main_frame, timer_label, 60), daemon=True).start()

    # Voting container
    vote_frame = Frame(main_frame, bg=BG_COLOR)
    vote_frame.pack(pady=20)

    # Candidate list with improved styling
    candidates = [
        ("JVP", "Anura Kumara Dissanayaka", "img/Malimawa.jpg", "jvp"),
        ("SLPP", "Mahinda Rajapaksha", "img/slpp.png", "slpp"),
        ("SJB", "Sajith Premadasa", "img/sjb.png", "sjb"),
        ("UNP", "Ranil Wikkramasingha", "img/unp.png", "unp"),
        ("TNA", "R.Sampanthan", "img/tna.png", "tna"),
        ("NOTA", "None of the Above", "img/nota.jpg", "nota")
    ]

    vote = StringVar(frame1, "-1")

    for idx, (party, leader, img_path, value) in enumerate(candidates):
        row_frame = Frame(vote_frame, bg=BG_COLOR)
        row_frame.grid(row=idx, column=0, pady=10, sticky="w")

        # Party logo
        try:
            img = ImageTk.PhotoImage(Image.open(img_path).resize((60,60), Image.LANCZOS))
            image_refs.append(img)
            Label(row_frame, image=img, bg=BG_COLOR).pack(side=LEFT, padx=10)
        except:
            Label(row_frame, text="[LOGO]", bg=PARTY_COLOR, fg=TEXT_COLOR).pack(side=LEFT, padx=10)

        # Radio button
        Radiobutton(row_frame, 
            text=f"{party}\n{leader}",
            font=('Helvetica', 11),
            variable=vote,
            value=value,
            bg=PARTY_COLOR,
            activebackground=ACTIVE_COLOR,
            fg=TEXT_COLOR,
            selectcolor=PARTY_COLOR,
            indicatoron=0,
            width=25,
            height=3,
            command=lambda v=value: voteCast(root, frame1, v, client_socket)
        ).pack(side=LEFT, padx=10)

    # Footer note
    Label(main_frame, text="Your vote is confidential and secure", 
         font=('Helvetica', 10), bg=BG_COLOR, fg="#95A5A6").pack(side=BOTTOM, pady=20)

    frame1.pack(expand=True, fill=BOTH)
    root.mainloop()