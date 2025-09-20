import os
import re

CONFIG = {
  "fps": 30,
  "mode": "stick_chase",
  "brightness": 14,
  "palette": [
    [
      255,
      0,
      255
    ],
    [
      0,
      255,
      255
    ]
  ],
  "palette_swap": False,
  "palette_swap_secondary": False,
  "speed": 0
}

KEY_LED_MODE="led.mode"
KEY_LED_BRIGHTNESS="led.brightness"
KEY_LED_BRIGHTNESS_ADAPTIVE="led.brightness.adaptive"
KEY_LED_SPEED="led.speed"
KEY_LED_COLOUR="led.colour"
KEY_LED_COLOUR_RIGHT="led.colour.right"
KEY_LED_BATTERY_LOW_THRESHOLD="led.battery.low"
KEY_LED_BATTERY_CHARGING_ENABLED="led.battery.charging"

mode_map = {
    '0' : 'null',
    '1' : 'static',
    '3' : 'stick_chase',
    '5' : 'rainbow'
}

def identify_device():
    board = ""

    try:
        with open('/boot/boot/batocera.board', 'r') as f:
            board = f.read().strip()
    except (IOError, FileNotFoundError):
        pass

    return board

def get_param(key):
    return os.popen('batocera-settings-get '+key).read().strip()

def refresh(key:str|None=None):
    if key is None or key == KEY_LED_MODE:
        val = get_param(KEY_LED_MODE)
        CONFIG['mode'] = mode_map[val]
    
    if key is None or key == KEY_LED_BRIGHTNESS:
        val = get_param(KEY_LED_BRIGHTNESS)
        CONFIG['brightness'] = (int(val) // 7)
