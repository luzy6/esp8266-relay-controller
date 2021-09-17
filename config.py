import json

Default_Config = {"ap_ssid": "Node", 
                  "ap_pwd": "admin8266",
                  "sta_ssid": None,
                  "sta_pwd": None,
                  "webrepl_pwd": "123456",
                  "recovery_mode": False}

class Config:
  PATH = "./config.json"
  CONFIG = {}
  CONFIG.update(Default_Config)
  
  @classmethod
  def readFile(cls):
    try:
      with open(cls.Path, 'r') as f:
        cfg = json.load(f)
      cls.CONFIG.update(cfg)
    except Exception as e:
      print('read config error: {}'.format(e))
      
  @classmethod
  def writeFile(cls):
    try:
      with open(cls.Path, 'w') as f:
        cfg = json.dump(cls.CONFIG, f)
    except Exception as e:
      print('write config error: {}'.format(e))

  @classmethod
  def get(cls, key):
    return cls.CONFIG.get(key, None)
  
  @classmethod
  def set(cls, key, value):
    cls.CONFIG[key] = value

