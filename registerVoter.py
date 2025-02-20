import tkinter as tk
import dframe as df
from tkinter import ttk
from tkinter import *
from dframe import *

BG_COLOR = "#2A3457"  
ACCENT_COLOR = "#3E4A6B"  
TEXT_COLOR = "white"
FONT_TITLE = ('Helvetica', 24, 'bold')
FONT_LABEL = ('Helvetica', 12)
FONT_INPUT = ('Helvetica', 11)
ENTRY_BG = "#F0F0F0"
BTN_BG = "#4CAF50"  
BTN_ACTIVE = "#45a049"


def reg_server(root, frame1, name, sex, zone, city, passw):

    for widget in frame1.winfo_children():
        if isinstance(widget, tk.Message) or isinstance(widget, tk.Label):
            widget.destroy()

    if not all([name, sex, zone, city, passw]):
        error_msg = Label(frame1, text="⚠️ All fields are required!", 
                         fg="#E74C3C", bg=BG_COLOR, font=FONT_LABEL)
        error_msg.pack(pady=10)
        return -1
        
    if ' ' in passw or len(passw) < 6:
        error_msg = Label(frame1, text="⚠️ Password must be at least 6 characters\nand contain no spaces!", 
                         fg="#E74C3C", bg=BG_COLOR, font=FONT_LABEL)
        error_msg.pack(pady=10)
        return -1

    vid = df.taking_data_voter(name, sex, zone, city, passw)
    for widget in frame1.winfo_children():
        widget.destroy()
        
    success_frame = Frame(frame1, bg=BG_COLOR)
    success_frame.pack(expand=True, fill=BOTH)
    
    Label(success_frame, text="✓ Registration Successful", 
         fg=BTN_BG, bg=BG_COLOR, font=FONT_TITLE).pack(pady=10)
    Label(success_frame, text=f"Voter ID: {vid}", 
         fg=TEXT_COLOR, bg=BG_COLOR, font=('Helvetica', 16)).pack(pady=5)

def Register(root, frame1):
    root.title("Voter Registration")
    root.configure(bg=BG_COLOR)
    
    for widget in frame1.winfo_children():
        widget.destroy()

    main_frame = Frame(frame1, bg=BG_COLOR)
    main_frame.pack(expand=True, fill=BOTH)
    
    Label(main_frame, text="Voter Registration", 
         font=FONT_TITLE, bg=BG_COLOR, fg=TEXT_COLOR).pack(pady=20)

    form_frame = Frame(main_frame, bg=ACCENT_COLOR, padx=20, pady=20)
    form_frame.pack()

    fields = [
        ("Full Name", "name"),
        ("Zone", "zone"),
        ("City", "city"),
        ("Password", "password")
    ]

    entries = {}
    for idx, (label, field) in enumerate(fields):
        Label(form_frame, text=label+":", font=FONT_LABEL,
             bg=ACCENT_COLOR, fg=TEXT_COLOR).grid(row=idx, column=0, padx=10, pady=10, sticky="e")
        
        entry = Entry(form_frame, font=FONT_INPUT, bg=ENTRY_BG, 
                     width=25, relief=tk.FLAT)
        entry.grid(row=idx, column=1, padx=10, pady=10)
        entries[field] = entry
        
        if field == "password":
            entry.config(show="•")

    Label(form_frame, text="Gender:", font=FONT_LABEL,
         bg=ACCENT_COLOR, fg=TEXT_COLOR).grid(row=4, column=0, padx=10, pady=10, sticky="e")
    
    gender = ttk.Combobox(form_frame, font=FONT_INPUT, width=23, 
                         state="readonly")
    gender['values'] = ("Male", "Female", "Other")
    gender.current(0)
    gender.grid(row=4, column=1, padx=10, pady=10)

    reg_btn = Button(main_frame, text="Complete Registration", 
                    font=('Helvetica', 14, 'bold'), 
                    bg=BTN_BG, fg=TEXT_COLOR, activebackground=BTN_ACTIVE,
                    padx=20, pady=10,
                    command=lambda: reg_server(
                        root, main_frame,
                        entries["name"].get(),
                        gender.get(),
                        entries["zone"].get(),
                        entries["city"].get(),
                        entries["password"].get()
                    ))
    reg_btn.pack(pady=30)

    style = ttk.Style()
    style.theme_use('clam')
    style.configure('TCombobox', fieldbackground=ENTRY_BG, background=ENTRY_BG)
    
    frame1.pack(expand=True, fill=BOTH)
    root.mainloop()