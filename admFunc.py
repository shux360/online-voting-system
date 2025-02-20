import tkinter as tk
from tkinter import *
from PIL import ImageTk, Image
import threading
import dframe as df
import time

# Colors and Fonts
BG_COLOR = "#2A3457"  
CARD_COLOR = "#3E4A6B"  
TEXT_COLOR = "white"
FONT_TITLE = ('Helvetica', 24, 'bold')
FONT_LABEL = ('Helvetica', 14)
FONT_VOTES = ('Helvetica', 16, 'bold')
BTN_BG = "#4CAF50"  
BTN_ACTIVE = "#45a049"
DANGER_BG = "#E74C3C"  

def resetAll(root, frame1):
    """ Resets all election data """
    df.count_reset()
    df.reset_voter_list()
    df.reset_cand_list()
    
    for widget in frame1.winfo_children():
        if isinstance(widget, tk.Message):
            widget.destroy()
    
    success_frame = Frame(frame1, bg=BG_COLOR)
    success_frame.place(relx=0.5, rely=0.9, anchor=CENTER)
    Label(success_frame, text="✅ System Reset Complete", 
          fg=BTN_BG, bg=BG_COLOR, font=FONT_LABEL).pack()

def fetchVotes(vote_labels, root):
    """ Fetches vote counts in a separate thread and updates the UI safely """
    while True:
        result = df.show_result()
        root.after(0, lambda: updateUI(result, vote_labels))  # Safe UI update
        time.sleep(1)  # Fetch every second

def updateUI(result, vote_labels):
    """ Safely updates vote labels on the UI thread """
    for party, votes in result.items():
        vote_labels[party].config(text=str(votes))

def showVotes(root, frame1):
    """ Displays live election results using threading """
    root.title("Live Vote Results")
    for widget in frame1.winfo_children():
        widget.destroy()

    main_frame = Frame(frame1, bg=BG_COLOR)
    main_frame.pack(expand=True, fill=BOTH, padx=20, pady=20)

    Label(main_frame, text="Live Election Results", 
          font=FONT_TITLE, bg=BG_COLOR, fg=TEXT_COLOR).pack(pady=20)

    results_frame = Frame(main_frame, bg=BG_COLOR)
    results_frame.pack()

    parties = ["jvp", "slpp", "sjb", "unp", "tna", "nota"]
    images = ["img/Malimawa.jpg", "img/slpp.png", "img/sjb.png", 
              "img/unp.png", "img/tna.png", "img/nota.jpg"]
    
    vote_labels = {}
    frame1.image_refs = []  

    for idx, (party, img_path) in enumerate(zip(parties, images)):
        card = Frame(results_frame, bg=CARD_COLOR, padx=20, pady=10)
        card.grid(row=idx//2, column=idx%2, padx=10, pady=10)

        try:
            img = ImageTk.PhotoImage(Image.open(img_path).resize((80, 70), Image.LANCZOS))
        except Exception as e:
            print(f"Error loading {img_path}: {e}")
            img = ImageTk.PhotoImage(Image.new("RGB", (80, 70), "gray"))  # Placeholder image
        
        frame1.image_refs.append(img)
        Label(card, image=img, bg=CARD_COLOR).grid(row=0, column=0, rowspan=2)

        Label(card, text=party.upper(), font=FONT_LABEL, bg=CARD_COLOR, fg=TEXT_COLOR).grid(row=0, column=1, sticky="w")
        vote_labels[party] = Label(card, text="0", font=FONT_VOTES, bg=CARD_COLOR, fg="#4CAF50")
        vote_labels[party].grid(row=1, column=1, sticky="w")

    # Start thread for fetching vote updates
    threading.Thread(target=fetchVotes, args=(vote_labels, root), daemon=True).start()

def adminHome():
    """ Creates the Admin Dashboard window """
    root = tk.Tk()
    root.geometry('800x600')
    root.configure(bg=BG_COLOR)
    root.title("Admin Dashboard")

    main_frame = Frame(root, bg=BG_COLOR)
    main_frame.pack(expand=True, fill=BOTH, padx=40, pady=40)

    Label(main_frame, text="Administration Panel", font=FONT_TITLE, bg=BG_COLOR, fg=TEXT_COLOR).pack(pady=20)

    btn_frame = Frame(main_frame, bg=BG_COLOR)
    btn_frame.pack(pady=30)

    buttons = [
        ("📊 Show Votes", showVotes, BTN_BG),
        ("🔄 Reset System", lambda: resetAll(root, main_frame), DANGER_BG),
        ("🚪 Exit", root.destroy, "#95A5A6")
    ]

    for text, cmd, color in buttons:
        btn = Button(btn_frame, text=text, font=FONT_LABEL, bg=color, fg=TEXT_COLOR,
                     activebackground=color, padx=20, pady=10, width=20)

        if text == "🚪 Exit":
            btn.config(command=root.destroy)
        else:
            btn.config(command=lambda c=cmd: c(root, main_frame))
        
        btn.pack(pady=15, fill=X)

    root.mainloop()

if __name__ == "__main__":
    adminHome()
