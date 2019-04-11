import BlynkLib
import network
import machine
from boot import sta_if
from machine import Pin
import time
from machine import Timer
import dht

#machine.freq(160000000)

BLYNK_AUTH = 'b1803b048a4941ceaa52514139658c0e'

print("Connecting to WiFi...")
wifi = sta_if

print('IP:', wifi.ifconfig()[0])

print("Connecting to Blynk...")
blynk = BlynkLib.Blynk(BLYNK_AUTH, server='192.168.2.194', port=8080)

p2 = Pin(2, Pin.OUT)

@blynk.ON("connected")
def blynk_connected(ping):
    print('Blynk ready. Ping:', ping, 'ms')
    
@blynk.VIRTUAL_WRITE(3)
def v3_write_handler(value):
    print('Current slider value: {}'.format(value[0]))
    print(value)
    global p2
    if value[0] == '1':
      p2.on()
    else:
      p2.off()

A = 1    
#tim = Timer(-1)
#tim.init(period=1000, mode=Timer.PERIODIC, callback=lambda t:print(A))
    
d = dht.DHT11(machine.Pin(0))

def runLoop():
    global A
    while True:
        blynk.run()
        '''A += 1
        print(A)
        d.measure()
        tem = d.temperature()
        hum = d.humidity()
        blynk.virtual_write(5, A)
        blynk.virtual_write(6, hum)'''

# Run blynk in the main thread:
runLoop()
#tim.deinit()



