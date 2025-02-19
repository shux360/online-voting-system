import subprocess as sb_p
import tkinter as tk
import registerVoter as regV
import admFunc as adFunc
from tkinter import *
from registerVoter import *
from admFunc import *


BG_COLOR = "#2A3457"  
BUTTON_BG = "#4CAF50"  
BUTTON_ACTIVE = "#45a049"  
TEXT_COLOR = "white"
FONT_TITLE = ('Helvetica', 25, 'bold')
FONT_BUTTON = ('Helvetica', 14, 'bold')
BTN_PADX = 20
BTN_PADY = 10


def AdminHome(root, frame1, frame3):
    root.title("Admin Panel")
    root.configure(bg=BG_COLOR)
    for widget in frame1.winfo_children():
        widget.destroy()

    
    frame3.configure(bg="#3E4A6B")
    Button(frame3, text="Admin", font=('Helvetica', 12), 
          bg="#3E4A6B", fg=TEXT_COLOR, activebackground="#4E5A7B",
          command=lambda: AdminHome(root, frame1, frame3)).pack(side=LEFT, padx=10, pady=5)
    frame3.pack(side=TOP, fill=X)

    
    frame1.configure(bg=BG_COLOR)
    Label(frame1, text="Admin Dashboard", font=FONT_TITLE, 
         bg=BG_COLOR, fg=TEXT_COLOR).grid(row=0, column=0, pady=30, columnspan=3)

    
    button_frame = Frame(frame1, bg=BG_COLOR)
    button_frame.grid(row=1, column=0, columnspan=3, pady=20)

    
    buttons = [
        ("Run Server", "#E74C3C", "#C0392B", lambda: sb_p.call('start python Server.py', shell=True)),
        ("Register Voter", BUTTON_BG, BUTTON_ACTIVE, lambda: regV.Register(root, frame1)),
        ("Show Votes", "#3498DB", "#2980B9", lambda: adFunc.showVotes(root, frame1)),
        ("Reset All", "#95A5A6", "#7F8C8D", lambda: adFunc.resetAll(root, frame1))
    ]

    for idx, (text, bg, active_bg, cmd) in enumerate(buttons):
        btn = Button(button_frame, text=text, font=FONT_BUTTON,
                    bg=bg, fg=TEXT_COLOR, activebackground=active_bg,
                    padx=BTN_PADX, pady=BTN_PADY, width=20,
                    command=cmd)
        btn.grid(row=idx, column=0, pady=10, sticky="ew")

    
    frame1.grid_columnconfigure(0, weight=1)
    frame1.pack(expand=True, fill=BOTH)
    root.mainloop()

def log_admin(root, frame1, admin_ID, password):
    if admin_ID == "Admin" and password == "admin":
        frame3 = root.winfo_children()[1]
        AdminHome(root, frame1, frame3)
    else:
        msg = Message(frame1, text="Either ID or Password is Incorrect", 
                     width=500, bg=BG_COLOR, fg="#E74C3C")
        msg.grid(row=6, column=0, columnspan=5)

def AdmLogin(root, frame1):
    root.title("Admin Login")
    root.configure(bg=BG_COLOR)
    for widget in frame1.winfo_children():
        widget.destroy()

    frame1.configure(bg=BG_COLOR)
    
    
    Label(frame1, text="Admin Login", font=FONT_TITLE, 
         bg=BG_COLOR, fg=TEXT_COLOR).grid(row=0, column=0, columnspan=2, pady=40)

    form_frame = Frame(frame1, bg=BG_COLOR)
    form_frame.grid(row=1, column=0, pady=20)

    
    Label(form_frame, text="Admin ID:", font=FONT_BUTTON, 
         bg=BG_COLOR, fg=TEXT_COLOR).grid(row=0, column=0, padx=10, pady=10, sticky="e")
    Label(form_frame, text="Password:", font=FONT_BUTTON, 
         bg=BG_COLOR, fg=TEXT_COLOR).grid(row=1, column=0, padx=10, pady=10, sticky="e")

    admin_ID = tk.StringVar()
    password = tk.StringVar()

    e1 = Entry(form_frame, font=('Helvetica', 12), width=25)
    e1.grid(row=0, column=1, padx=10, pady=10)
    e2 = Entry(form_frame, show='*', font=('Helvetica', 12), width=25)
    e2.grid(row=1, column=1, padx=10, pady=10)

    
    Button(form_frame, text="Login", font=FONT_BUTTON,
          bg="#3498DB", fg=TEXT_COLOR, activebackground="#2980B9",
          padx=20, pady=5, width=15,
          command=lambda: log_admin(root, frame1, e1.get(), e2.get())
          ).grid(row=2, column=0, columnspan=2, pady=30)

   
    frame1.grid_columnconfigure(0, weight=1)
    frame1.pack(expand=True, fill=BOTH)
    root.mainloop()