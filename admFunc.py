import tkinter as tk
from tkinter import *
from PIL import ImageTk, Image
import dframe as df  # Import data frame module


def resetAll(root, frame1):
    df.count_reset()
    df.reset_voter_list()
    df.reset_cand_list()
    Label(frame1, text="").grid(row=10, column=0)
    msg = Message(frame1, text="Reset Complete", width=500)
    msg.grid(row=11, column=0, columnspan=5)


def showVotes(root, frame1):
    def updateVotes():
        result = df.show_result()
        vote_labels["jvp"].config(text=result['jvp'])
        vote_labels["slpp"].config(text=result['slpp'])
        vote_labels["sjb"].config(text=result['sjb'])
        vote_labels["unp"].config(text=result['unp'])
        vote_labels["tna"].config(text=result['tna'])
        vote_labels["nota"].config(text=result['nota'])
        frame1.after(3000, updateVotes)

    root.title("Votes")
    for widget in frame1.winfo_children():
        widget.destroy()

    Label(frame1, text="Vote Count", font=('Helvetica', 18, 'bold')).grid(row=0, column=1)
    Label(frame1, text="").grid(row=1, column=0)

    result = df.show_result()
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
        vote_labels[party] = Label(frame1, text=result[party], font=('Helvetica', 12, 'bold'))
        vote_labels[party].grid(row=i + 2, column=2)

    frame1.pack()
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