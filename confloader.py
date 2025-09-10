import os
import re

CONFIG = {
  "device": "trimui_smart_pro",
  "fps": 30,
  "mode": "stick_chase",
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

def identify_device():
    board = ""
    
    try:
        with open('/boot/boot/batocera.board', 'r') as f:
            board = f.read().strip()
    except (IOError, FileNotFoundError):
        pass

    return board

def refresh(key:str|None=None):
    pass