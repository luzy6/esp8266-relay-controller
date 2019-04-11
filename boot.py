
# This file is executed on every boot (including wake-boot from deepsleep)

#import esp
#esp.osdebug(None)

import gc
# import webrepl
import network


class Connector:
  def __init__(self):
    ap_if = network.WLAN(network.AP_IF)
    ap_if.active(False)
    self.sta_if = network.WLAN(network.STA_IF)
    self.sta_if.active(True)
    self.ssid = '@PHICOMM_40'
    self.password = '20405lzy'
    
  def connect(self):
    if not self.sta_if.isconnected():
        print('connecting to network...')
        self.sta_if.connect(self.ssid, self.password)
    
  def isConnect(self):
    return self.sta_if.isconnected()
    
  def getInfo(self):
    return self.sta_if.ifconfig()
  
  def doConnect(self):
    if not self.sta_if.isconnected():
        print('connecting to network...')
        self.sta_if.connect('@PHICOMM_40', '20405lzy')
        while not self.sta_if.isconnected():
            pass
    print('network config:', self.sta_if.ifconfig())
    
connector = Connector()
connector.connect()

# webrepl.start()

gc.collect()

