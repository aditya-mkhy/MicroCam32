import socket
from tkinter import *
import time
import os, sys
import ctypes
from PIL import ImageTk, Image
import io
import threading

ctypes.windll.shcore.SetProcessDpiAwareness(True)

'''
use this as a client on windows to view
'''
def get_image():
    s = socket.socket()
    s.connect(("192.168.14.1", 80))
    data = b""
    while True:
        try:
            d = s.recv(1024)
            if not d:
                break
            data += d
        except Exception as e:
            print(e)
            break
    try:
        s.close()
    except:
        pass

    return data
    
def handle_image():
    global lab, root, image_store
    image_store.append(ImageTk.PhotoImage(Image.open(io.BytesIO(get_image()))))
    lab.config(image=image_store[len(image_store)-1])
    root.update()
    if len(image_store) > 5:
        image_store.pop(0)
    showimage()


def showimage():
    threading.Thread(target=handle_image, daemon=True).start()


image_store = []
root = Tk()
root.geometry("800x600+200+100")
root.config(bg="white")
lab = Label(root, bg="white", bd=0, relief="flat")
lab.place(x=0, y=0)
lab.after(100, showimage)
root.mainloop()
