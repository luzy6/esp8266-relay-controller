# This file is executed on every boot (including wake-boot from deepsleep)

#import esp
#esp.osdebug(None)

import gc
import sys
import webrepl
import network
webrepl.start()
from wifi_cfg import SSID, PASSWORD

class AP:
  def __init__(self):
    self.ap_if = network.WLAN(network.AP_IF)
    self.is_active = False
  
  def active(self):
    if not self.is_active:
      self.ap_if.active(True)
      self.is_active = True
      
  def inactive(self):
    if self.is_active:
      self.ap_if.active(False)
      self.is_active = False

class Connector:
  def __init__(self):
    self.sta_if = network.WLAN(network.STA_IF)
    self.sta_if.active(True)
    self.ssid = str(SSID)
    self.password = str(PASSWORD)
    
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
      self.sta_if.connect(self.ssid, self.password)
      while not self.sta_if.isconnected():
        pass
    print('network config:', self.sta_if.ifconfig())
    
access_point = AP()
access_point.active()
connector = Connector()
connector.connect()

gc.collect()

