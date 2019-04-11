import socket
import time
from machine import Pin
from boot import sta_if
sta_if.ifconfig(('192.168.2.173', '255.255.255.0', '192.168.2.1', '8.8.8.8'))
addr = socket.getaddrinfo('192.168.2.173', 2040)[0][-1]
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(addr)
print('client connected from', addr)

p2 = Pin(2, Pin.OUT)
p0 = Pin(0, pin.IN)

def run():
  p2.off()
  state = False
  while True:
    data, addr = s.recvfrom(1024)
    t2 = time.time()
    print(data)
    if data == b'0':
      p2.on()
      state = True
    elif data == b'1':
      p2.off()
      state = False
    elif data == b'2':
      if state:
        p2.off()
        state = False
      else:
        p2.on()
        state = True
        
run()
s.close()
print('close')


