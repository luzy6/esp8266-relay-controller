import socket
import time
from boot import sta_if
sta_if.ifconfig(('192.168.2.173', '255.255.255.0', '192.168.2.1', '8.8.8.8'))
addr = socket.getaddrinfo('192.168.2.173', 2040)[0][-1]
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(addr)
#s.setblocking(True)
print('listening on', addr)

# cl, addr = s.accept()
print('client connected from', addr)

def test1():
  t2 = time.time()
  while True:
    t1 = time.time()
    if t1 - t2 > 1:
      data, addr = s.recvfrom(1024)
      t2 = time.time()
      print(data)
      if data:
        print(data) 
      if data == b'9':
        print('break')
        break
      
def test2():
  while True:
    s.recv(1024)
    s.send('1')

test1()
s.close()
print('close')


