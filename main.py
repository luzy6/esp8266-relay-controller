import socket
import time
import gpio
from boot import connector
import select
import ntptime
#import micropython
#micropython.alloc_emergency_exception_buf(100)
# sta_if.ifconfig(('192.168.2.173', '255.255.255.0', '192.168.2.1', '8.8.8.8'))

#p1 = Pin(1, Pin.OUT)

# p0.irq(trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING, handler=callback)

ON = 'on'
OFF = 'off'
SWITCH = 'switch'

class SysTime:
  def __init__(self):
    ntptime.NTP_DELTA = 3155673600 - 3600*8 # UTC/GMT+08:0
    self._is_init = False

  def isInit(self):
    return self._is_init
    
  def init(self):
    try:
      ntptime.settime()
      now = time.localtime()
      if now[0] > 2000:
        self._is_init = True
    except:
      pass

  def now(self):
    return time.localtime()[:6]

sys_time = SysTime()
sys_time.init()

class NetProcessor:
  def __init__(self):
    self._str_on = b'0'
    self._str_off = b'1'
    self._str_switch = b'2'

    self.s = self._initSocket()
    self.poller = self._initSelect(self.s)
    
  def _initSocket(self):
    addr = socket.getaddrinfo('127.0.0.1', 2041)[0][-1]
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(0)
    s.bind(addr)
    print('{}:  client connected from '.format(sys_time.now()), addr)
    return s
    
  def _initSelect(self, s):
    poller = select.poll()
    poller.register(s, select.POLLIN)
    return poller

  def process(self):
    res = self.poller.poll(10)
    if res:
      data, addr = self.s.recvfrom(1024)
      print('{}:  recv '.format(sys_time.now()), data)
      if data == self._str_on:
        return ON
      elif data == self._str_off:
        return OFF
      elif data == self._str_switch:
        return SWITCH
      else:
        return None
    else:
      return None
    
  def close(self):
    self.s.close()

class KeyProcessor:
  def __init__(self, pin=3):
    self.key = gpio.IOIn(pin)
    self._counts = 0
    self._key_state = self.key.value()
    
  def _pinChange(self):
    v = self.key.value()
    if v == self._key_state:
      self._counts = 0
      return False
    else:
      self._counts += 1
      print('{}:  input pin is triggered {}!'.format(sys_time.now(), self._counts))
    if self._counts > 10:
      self._key_state = v
      self._counts = 0
      print('{}:  input pin is changed!'.format(sys_time.now()))
      return True
    else:
      return False

  def process(self):
    if self._pinChange():
      return SWITCH
    else:
      return None

class Run:
  def __init__(self):
    self.lamp = gpio.IOOut(2)
    self.key_processor = KeyProcessor()
    #self.key_processor = KeyProcessor(0)
    self.net_processor = NetProcessor()
    
  def reverseLamp(self):
    if self.lamp.isOn():
      self.offLamp()
    else:
      self.onLamp()
      
  def onLamp(self):
    self.lamp.on()
    print('{}:  open lamp'.format(sys_time.now()))
      
  def offLamp(self):
    self.lamp.off()
    print('{}:  close lamp'.format(sys_time.now()))
      
  def handle(self, res):
    if res == ON:
      self.onLamp()
    elif res == OFF:
      self.offLamp()
    elif res == SWITCH:
      self.reverseLamp()
    
  def loop(self):
    print('{}:  start loop!!!'.format(sys_time.now()))
    while True:
      res = self.net_processor.process()
      self.handle(res)
      res = self.key_processor.process()
      self.handle(res)
      
  def close(self):
    self.net_processor.close()
        
if __name__ == "__main__":
  run = Run()
  try:
    run.loop()
  finally:
    run.close()
    print('{}:  close!!!'.format(sys_time.now()))

