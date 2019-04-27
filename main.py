import socket
import time
from machine import Pin
from boot import connector
import select
import ntptime
#import micropython
#micropython.alloc_emergency_exception_buf(100)
# sta_if.ifconfig(('192.168.2.173', '255.255.255.0', '192.168.2.1', '8.8.8.8'))

#p1 = Pin(1, Pin.OUT)

# p0.irq(trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING, handler=callback)

class Run:
  def __init__(self):
    ntptime.NTP_DELTA = 3155673600 - 3600*8 # UTC/GMT+08:0
    self.s = self.initSocket()
    self.poller = self.initSelect(self.s)
    self.io_out = Pin(2, Pin.OPEN_DRAIN)
    self.io_in = Pin(3, Pin.IN, Pin.PULL_UP)
    #self.io_in = Pin(0, Pin.IN, Pin.PULL_UP)
    self.state = False
    self.real_time_is_set = False
    self.counts = 0
    self.value_input = self.io_in.value()
    self.offPin()
    
  def initSocket(self):
    addr = socket.getaddrinfo('127.0.0.1', 2041)[0][-1]
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(addr)
    s.settimeout(0)
    print('{}:  client connected from '.format(self.time()), addr)
    return s
    
  def initSelect(self, s):
    poller = select.poll()
    poller.register(s, select.POLLIN)
    return poller
    
  def setRealTime(self):
    try:
      ntptime.settime()
      now = time.localtime()
      if now[0] > 2000:
        self.real_time_is_set = True
    except:
      pass
  
  def time(self):
    return time.localtime()[:6]
  
  def reversePin(self):
    if self.state:
      self.offPin()
    else:
      self.onPin()
    
  def offPin(self):
    self.io_out.off()
    self.state = False
    print('{}:  close output io'.format(self.time()))
    
  def onPin(self):
    self.io_out.on()
    self.state = True
    print('{}:  open output io'.format(self.time()))
  
  def pinChange(self):
    v = self.io_in.value()
    if v == self.value_input:
      self.counts = 0
      return False
    else:
      self.counts += 1
      print('{}:  input pin is triggered {}!'.format(self.time(), self.counts))
    if self.counts > 10:
      self.value_input = v
      self.counts = 0
      print('{}:  input pin is changed!'.format(self.time()))
      return True
    else:
      return False

  def loop(self):
    while True:
      if not self.real_time_is_set:
        self.setRealTime()
      res = self.poller.poll(10)
      if res:
        data, addr = self.s.recvfrom(1024)
        print('{}:  recv '.format(self.time()), data)
        if data == b'0':
          self.onPin()
        elif data == b'1':
          self.offPin()
        elif data == b'2':
          self.reversePin()
      if self.pinChange():
        self.reversePin()
        
  def close(self):
    self.s.close()
        
if __name__ == "__main__":
  run = Run()
  try:
    run.loop()
  finally:
    run.close()
    print('{}:  close!!!'.format(run.time()))

