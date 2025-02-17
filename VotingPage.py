import tkinter as tk
import socket
from tkinter import *
from PIL import ImageTk,Image

def voteCast(root,frame1,vote,client_socket):

    for widget in frame1.winfo_children():
        widget.destroy()

    client_socket.send(vote.encode()) #4

    message = client_socket.recv(1024) #Success message
    print(message.decode()) #5
    message = message.decode()
    if(message=="Successful"):
        Label(frame1, text="Vote Casted Successfully", font=('Helvetica', 18, 'bold')).grid(row = 1, column = 1)
    else:
        Label(frame1, text="Vote Cast Failed... \nTry again", font=('Helvetica', 18, 'bold')).grid(row = 1, column = 1)

    client_socket.close()



def votingPg(root,frame1,client_socket):

    root.title("Cast Vote")
    for widget in frame1.winfo_children():
        widget.destroy()

    Label(frame1, text="Cast Vote", font=('Helvetica', 18, 'bold')).grid(row = 0, column = 1, rowspan=1)
    Label(frame1, text="").grid(row = 1,column = 0)

    vote = StringVar(frame1,"-1")

    Radiobutton(frame1, text = "JVP\n\nAnura Kumara Dissanayaka", variable = vote, value = "jvp", indicator = 0, height = 4, width=15, command = lambda: voteCast(root,frame1,"jvp",client_socket)).grid(row = 2,column = 1)
    jvpLogo = ImageTk.PhotoImage((Image.open("img/Malimawa.jpg")).resize((45,45),Image.LANCZOS))
    jvpImg = Label(frame1, image=jvpLogo).grid(row = 2,column = 0)

    Radiobutton(frame1, text = "SLPP\n\nMahinda Rajapaksha", variable = vote, value = "slpp", indicator = 0, height = 4, width=15, command = lambda: voteCast(root,frame1,"slpp",client_socket)).grid(row = 3,column = 1)
    slppLogo = ImageTk.PhotoImage((Image.open("img/slpp.png")).resize((35,48),Image.LANCZOS))
    slppImg = Label(frame1, image=slppLogo).grid(row = 3,column = 0)

    Radiobutton(frame1, text = "SJB\n\nSajith Premadasa", variable = vote, value = "sjb", indicator = 0, height = 4, width=15, command = lambda: voteCast(root,frame1,"sjb",client_socket) ).grid(row = 4,column = 1)
    sjbLogo = ImageTk.PhotoImage((Image.open("img/sjb.png")).resize((55,40),Image.LANCZOS))
    sjbImg = Label(frame1, image=sjbLogo).grid(row = 4,column = 0)

    Radiobutton(frame1, text = "UNP\n\nRanil Wikkramasingha", variable = vote, value = "unp", indicator = 0, height = 4, width=15, command = lambda: voteCast(root,frame1,"unp",client_socket)).grid(row = 5,column = 1)
    unpLogo = ImageTk.PhotoImage((Image.open("img/unp.png")).resize((50,45),Image.LANCZOS))
    unpImg = Label(frame1, image=unpLogo).grid(row = 5,column = 0)

    Radiobutton(frame1, text="TNA\n\nR.Sampanthan", variable=vote, value="tna", indicator=0, height=4, width=15,command=lambda: voteCast(root, frame1, "tna", client_socket)).grid(row=6, column=1)
    tnaLogo = ImageTk.PhotoImage((Image.open("img/tna.png")).resize((50, 45), Image.LANCZOS))
    tnaImg = Label(frame1, image=tnaLogo).grid(row=6, column=0)

    Radiobutton(frame1, text = "\nNOTA    \n  ", variable = vote, value = "nota", indicator = 0, height = 4, width=15, command = lambda: voteCast(root,frame1,"nota",client_socket)).grid(row = 7,column = 1)
    notaLogo = ImageTk.PhotoImage((Image.open("img/nota.jpg")).resize((45,35),Image.LANCZOS))
    notaImg = Label(frame1, image=notaLogo).grid(row = 7,column = 0)

    frame1.pack()
    root.mainloop()


# if __name__ == "__main__":
#         root = Tk()
#         root.geometry('500x500')
#         frame1 = Frame(root)
#         client_socket='Fail'
#         votingPg(root,frame1,client_socket)
