import network 
from time import time, sleep, localtime as loct
from json import loads
import usocket as usk


def log(*args, **kwargs):
    print(f" INFO [{loct()[2]}/{loct()[1]}/{loct()[0]} {loct()[3]}:{loct()[4]}:{loct()[5]}] ", args, kwargs)
  
class WiFi:
    def __init__(self):
        self.default_passwd = "wifi@246"
        network.WLAN(network.AP_IF).active(0) 
        self.station = network.WLAN(network.STA_IF)
        sleep(1)
        self.station.active(True)
        sleep(1)
        self.online = 0
        self.ssid=None

    def is_online(self):
        try:
            ai=usk.getaddrinfo('darkstartech.pythonanywhere.com',443,0,usk.SOCK_STREAM)[0]
            s=usk.socket(ai[0],usk.SOCK_STREAM,ai[2])
            s.connect(ai[-1])
            s.close()
            self.online = True
        except:
            self.online = False

        return self.online
    
    
    def connect_to(self, ssid, passwd, timeout=30):
        try:
            self.station.disconnect()
            self.station.connect(ssid, passwd)
            count = 0
            start_time = time()
            while self.station.status()==network.STAT_CONNECTING:
                count+=1
                log(f"{count}){ssid}&st={self.station.status()}")
                if (time()-start_time)> timeout:
                    log("TimeOut")
                    break

                sleep(1)

            status = self.station.status()
            self.ssid = ssid

            log(f"Status==> {status}")
            if status==network.STAT_WRONG_PASSWORD:
                log("Wrong Passwd...")

        except Exception as e:
            log(f'Error[1] : {e}')
        return self.station.isconnected()

    def scan(self): 
        wifi_list = []
        if self.station.isconnected():
            self.station.disconnect()
        try:
            scan_wifi = self.station.scan()
            for wifi_info in scan_wifi:
                name = wifi_info[0].decode()
                
                if wifi_info[4] != 0:
                    wifi_list.append(name)

            return wifi_list
        except:
            return wifi_list