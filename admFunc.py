import tkinter as tk
from tkinter import *
from PIL import ImageTk, Image
import dframe as df  # Import data frame module
import threading

def resetAll(root, frame1):
    df.count_reset()
    df.reset_voter_list()
    df.reset_cand_list()
    Label(frame1, text="").grid(row=10, column=0)
    msg = Message(frame1, text="Reset Complete", width=500)
    msg.grid(row=11, column=0, columnspan=5)


def showVotes(root, frame1):
    def updateVotes():
        """Fetch and update vote counts in a separate thread"""

        def fetch_votes():
            result = df.show_result()
            root.after(0, lambda: displayVotes(result))  # Update UI safely

        threading.Thread(target=fetch_votes, daemon=True).start()  # Run in a background thread
        root.after(3000, updateVotes)  # Schedule next update

    def displayVotes(result):
        """Display updated votes"""
        vote_labels = {}
        parties = ["jvp", "slpp", "sjb", "unp", "tna", "nota"]
        image_files = ["img/Malimawa.jpg", "img/slpp.png", "img/sjb.png", "img/unp.png", "img/tna.png", "img/nota.jpg"]

        frame1.image_refs = []  # Store image references to avoid garbage collection

        for i, party in enumerate(parties):
            try:
                logo = ImageTk.PhotoImage(Image.open(image_files[i]).resize((40, 35), Image.LANCZOS))
                frame1.image_refs.append(logo)
                Label(frame1, image=logo).grid(row=i + 2, column=0)
            except FileNotFoundError:
                print(f"Warning: Image {image_files[i]} not found.")

            Label(frame1, text=f"{party.upper()}:", font=('Helvetica', 12, 'bold')).grid(row=i + 2, column=1)
            vote_labels[party] = Label(frame1, text=result.get(party, "0"), font=('Helvetica', 12, 'bold'))
            vote_labels[party].grid(row=i + 2, column=2)

    root.title("Votes")
    for widget in frame1.winfo_children():
        widget.grid_forget()  # Clear previous widgets

    Label(frame1, text="Vote Count", font=('Helvetica', 18, 'bold')).grid(row=0, column=1)
    Label(frame1, text="").grid(row=1, column=0)

    updateVotes()


def adminHome():
    root = Tk()
    root.geometry('500x500')
    frame1 = Frame(root)
    frame1.pack()

    Button(frame1, text="Show Votes", command=lambda: showVotes(root, frame1)).grid(row=0, column=0)
    Button(frame1, text="Reset All", command=lambda: resetAll(root, frame1)).grid(row=0, column=1)
    Button(frame1, text="Exit", command=root.destroy).grid(row=0, column=2)

    root.mainloop()


if __name__ == "__main__":
    adminHome()