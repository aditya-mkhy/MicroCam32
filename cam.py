import socket
import camera
from time import sleep
import gc
from util import WiFi, log, DB, update_time

class Server:
    def __init__(self):
        self.db = DB()
        self.wifi = WiFi()
        ssid = self.db.get("ssid")
        log(f"Connecting to wi-fi -> {ssid}")
        status = self.wifi.connect_to(ssid=ssid, passwd=self.db.get("passwd"), timeout=120)

        if not status:
            log(f"Error in connecting with ssid : {ssid}. So can't proceed further.")
            exit()
        
        log(f"Connected to {ssid}")
        if not self.wifi.is_online():
            log(f"Not conneted to the in INTERNET. But can proceed further..")

        log("Connected to INTERNET. Let's start..")

        # Create server..
        gc.collect()
        self.network = socket.socket()
        self.network.bind(('0.0.0.0', 80))
        self.network.listen(5)
        self.network.settimeout(3)
        log("Server network initialized....")

        # update time...
        update_time()

    def init_camera(self):
        gc.collect()

        camera.framesize(10) # frame size 800X600 (1.33 espect ratio)
        camera.contrast(100) # increase contrast
        camera.speffect(100)

        for i in range(5):
            cam = camera.init()
            if cam:
                break
            else:
                sleep(2)

        log("is camera ready? : ", cam)


    def handle_client(self, conn: socket.socket):
        gc.collect()
        conn.send(camera.capture())
        conn.close()

    def run(self):
        self.init_camera()

        while True:
            try:
                conn, addr = self.network.accept()
                log(f"Connected....{addr}")
                self.handle_client(conn)

            except Exception as e:
                if "ETIMEDOUT" in str(e):
                    log("Timeout")
                else:
                    log(f"Erorr[001] : {e}")
            
            except KeyboardInterrupt:
                try:
                    conn.close()
                except:
                    pass

                try:
                    self.network.shutdown(socket.SHUT_RDWR)
                except:
                    pass

                self.network.close()
                break


if __name__ == "__main__":
    server = Server()
    server.run()
