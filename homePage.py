import subprocess as sb_p
import threading
import tkinter as tk
from tkinter import *
from Admin import AdmLogin
from voter import voterLogin

BG_COLOR = "#2A3457"
BUTTON_BG = "#4CAF50"
BUTTON_ACTIVE = "#45a049"
TEXT_COLOR = "white"
FONT_TITLE = ('Helvetica', 28, 'bold')
FONT_BUTTON = ('Helvetica', 14, 'bold')
BTN_PADX = 20
BTN_PADY = 10

def open_new_tab():
    sb_p.Popen(["python", "homePage.py"], shell=True)  # Non-blocking execution

def Home(root, frame1, frame2):
    for widget in frame1.winfo_children():
        widget.destroy()
    
    frame2.configure(bg=BG_COLOR)
    frame2.pack(side=TOP, fill=X)
    
    home_btn = Button(frame2, text="🏠 Home", font=('Helvetica', 12), 
                      bg="#3E4A6B", fg=TEXT_COLOR, activebackground="#4E5A7B",
                      command=lambda: Home(root, frame1, frame2))
    home_btn.pack(side=LEFT, padx=10, pady=5)

    Frame(frame2, bg=BG_COLOR, height=10).pack(side=BOTTOM, fill=X)

    root.title("Secure Voting System")
    root.configure(bg=BG_COLOR)

    frame1.configure(bg=BG_COLOR)
    Label(frame1, text="Online Voting System", font=FONT_TITLE, 
          bg=BG_COLOR, fg=TEXT_COLOR).pack(pady=30)
    
    button_frame = Frame(frame1, bg=BG_COLOR)
    button_frame.pack(expand=True)

    admin = Button(button_frame, text="Admin Login", font=FONT_BUTTON,
                   bg="#E74C3C", fg=TEXT_COLOR, activebackground="#C0392B",
                   padx=BTN_PADX, pady=BTN_PADY, width=15,
                   command=lambda: AdmLogin(root, frame1))
    admin.pack(pady=15)

    voter = Button(button_frame, text="Voter Login", font=FONT_BUTTON,
                   bg=BUTTON_BG, fg=TEXT_COLOR, activebackground=BUTTON_ACTIVE,
                   padx=BTN_PADX, pady=BTN_PADY, width=15,
                   command=lambda: voterLogin(root, frame1))
    voter.pack(pady=15)

    newTab = Button(button_frame, text="New Window", font=FONT_BUTTON,
                    bg="#3498DB", fg=TEXT_COLOR, activebackground="#2980B9",
                    padx=BTN_PADX, pady=BTN_PADY, width=15,
                    command=open_new_tab)
    newTab.pack(pady=15)
    Label(frame1, text="🔒 Secure Digital Voting Platform", bg=BG_COLOR,
          fg="#95A5A6", font=('Helvetica', 12)).pack(side=BOTTOM, pady=20)

    frame1.pack(expand=True, fill=BOTH)
    root.mainloop()

def new_home():
    root = Tk()
    root.geometry('800x700')
    root.resizable(False, False)
    frame1 = Frame(root)
    frame2 = Frame(root)
    Home(root, frame1, frame2)

if __name__ == "__main__":
    new_home()
