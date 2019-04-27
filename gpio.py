from machine import Pin

MODE_OPEN_DRAIN = Pin.OPEN_DRAIN
MODE_OUT = Pin.OUT
MODE_IN = Pin.IN

PULL_UP = Pin.PULL_UP
PULL_NONE = None

class IOOut:
  def __init__(self, pin, mode=MODE_OPEN_DRAIN, value=0):
    if mode not in [MODE_OPEN_DRAIN, MODE_OUT]:
      raise ValueError("Invalid IO out mode!, select in MODE_OPEN_DRAIN or MODE_OUT.")
    if value not in [0, 1]:
      raise ValueError("Invalid IO out value!, select in 0 or 1.")
    self.io = Pin(pin, mode)
    self._value = value
    if self._value == 0:
      self.off()
    else:
      self.on()
  
  @property
  def value(self):
    return self._value
    
  def isOn(self):
    if self._value:
      return True
    else:
      return False
  
  def on(self):
    self.io.on()
    self._value = 1
    
  def off(self):
    self.io.off()
    self._value = 0
    
class IOIn:
  def __init__(self, pin, pull=PULL_UP):
    if pull not in [PULL_UP, PULL_NONE]:
      raise ValueError("Invalid IO out pull!, select in PULL_UP or PULL_NONE.")
    self.io = Pin(pin, Pin.IN, pull)
    
  def value(self):
    return self.io.value()

