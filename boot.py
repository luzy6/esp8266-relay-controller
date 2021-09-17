# This file is executed on every boot (including wake-boot from deepsleep)

import esp
esp.osdebug(None)

import gc
gc.enable()
import sys
import webrepl
import network
import machine
import ntptime
import time

from config import Config

def setAP(ssid, pwd):
  print('set AP')
  ap_if = network.WLAN(network.AP_IF)
  if sta_if.isconnected():
    sta_if.active(False)
  ap_if = network.WLAN(network.AP_IF)
  ap_if.active(True)
  try:
    ap_if.config(essid=ssid, password=pwd, authmode=network.AUTH_WPA_WPA2_PSK)
  except Exception as e:
    print(e)
    return False
  return true

def setWifi(ssid, pwd, timeout_s=40):
  print('set WIFI')
  ap_if = network.WLAN(network.AP_IF)
  if ap_if.active():
    ap_if.active(False)
  del ap_if
  
  sta_if = network.WLAN(network.STA_IF)
  sta_if.active(True)
  if not sta_if.isconnected():
    self.sta_if.connect(ssid, pwd)
    while not sta_if.isconnected() and timeout_s > 0:
      print('Waiting for connection...')
      timeout -= 1
      sleep(1)
  return sta_if.isconnected()

def setNTP_RTC():
  if network.WLAN(network.STA_IF).isconnected():
    try:
      # Sync with NTP server
      ntptime.settime()
      # Get localtime + GMT
      (year, month, mday, hour, minute, second, weekday, yearday) =\
        time.localtime(time.time() + 8*3600) # UTC/GMT+08:0
      # Create RealTimeClock + Set RTC with time (+timezone)
      machine.RTC().datetime((year, month, mday, 0, hour, minute, second, 0))
      # Print time
      print("NTP setup DONE: {}".format(time.localtime()))
      return True
    except Exception as e:
      print("NTP setup errer: {}".format(e))
  return False

Config.readFile()
sta_ssid = Config.get('sta_ssid')
sta_pwd = Config.get('sta_pwd')
state = False
if sta_ssid is not None and sta_pwd is not None:
  state = setWifi(sta_ssid, sta_pwd)
  if state:
    setNTP_RTC()
if not state:
  ap_ssid = Config.get('ap_ssid')
  ap_pwd = Config.get('ap_pwd')
  setAP(ap_ssid, ap_pwd)
if Config.get('recovery_mode'):
  webrepl_pwd = Config.get('webrepl_pwd', '123456')
  webrepl.start(password=webrepl_pwd)
gc.collect()

