import socket
import time
from machine import Pin
from boot import connector
import select
#import micropython
#micropython.alloc_emergency_exception_buf(100)
# sta_if.ifconfig(('192.168.2.173', '255.255.255.0', '192.168.2.1', '8.8.8.8'))

#p1 = Pin(1, Pin.OUT)

# p0.irq(trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING, handler=callback)

class Run:
  def __init__(self):
    self.s = self.initSocket()
    self.poller = self.initSelect(self.s)
    self.io_out = Pin(2, Pin.OPEN_DRAIN, 1)
    self.io_in = Pin(3, Pin.IN, Pin.PULL_UP)
    self.state = False
    self.counts = 0
    self.value_input = self.io_in.value()
    
  def initSocket(self):
    addr = socket.getaddrinfo('127.0.0.1', 2041)[0][-1]
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(addr)
    s.settimeout(0)
    print('client connected from', addr)
    return s
    
  def initSelect(self, s):
    poller = select.poll()
    poller.register(s, select.POLLIN)
    return poller
    
  def reversePin(self):
    if self.state:
      self.offPin()
    else:
      self.onPin()
    
  def offPin(self):
    self.io_out.off()
    self.state = False
    print('close io')
    
  def onPin(self):
    self.io_out.on()
    self.state = True
    print('open io')
  
  def pinChange(self):
    v = self.io_in.value()
    if v == self.value_input:
      return False
    else:
      self.counts += 1
    if self.counts > 10:
      self.value_input = v
      self.counts = 0
      print('pin changed')
      return True
    else:
      return False

  def loop(self):
    while True:
      res = self.poller.poll(10)
      if res:
        data, addr = self.s.recvfrom(1024)
        print(data)
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
    print('close')

