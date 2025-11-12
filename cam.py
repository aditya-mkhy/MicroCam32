import socket
import camera
from time import sleep
import gc
from util import WiFi, log

class Conn:
    def __init__(self):
        pass
        


class Cam:
    pass
def handle_client(conn):
    gc.collect()
    data = conn.recv(1024).decode()
    print("Data==>", data)
    if data == "--send--img" or data:
        gc.collect()
        img = camera.capture()
        f = f"len=={len(img)}"
        conn.send(f.encode())
        conf = conn.recv(100).decode()
        if conf == "ok":
            
            conn.send(img)
            conf = conn.recv(100).decode()
            gc.collect()
            if conf == "ok":
                print("Image send sucess")
            else:
                print("Error in conferming")
    conn.close()
    
def handle_web_client(conn):
    gc.collect()
    conn.send(camera.capture())
    conn.close()

for i in range(5):
    cam = camera.init()
    print("Camera ready?: ", cam)
    if cam:
        break
    else:
        sleep(2)
    
    
wlan = WiFi()
ssid = "kumud 4g"
passwd = "you wifi passwd"

wlan.connect_to(ssid=ssid, passwd=passwd)

gc.collect()
camera.framesize(10)     # frame size 800X600 (1.33 espect ratio)
camera.contrast(100)       # increase contrast
camera.speffect(100)

net = socket.socket()
net.bind(('0.0.0.0', 80))
net.listen(5)
net.settimeout(3)
print("Done initializing....")
gc.collect()
while True:
    try:
        conn, addr = net.accept()
        print(f"Connected....{addr}")
        handle_web_client(conn)

    except Exception as e:
        e = str(e)
        if "ETIMEDOUT" in str(e):
            print("TimeOut")
        else:
            print(f"Erorr[00190] : {e}")
    

    except KeyboardInterrupt:
        try:
            conn.close()
        except:
            pass
        try:
            net.close()
        except:
            pass
        break

print("Done......")

