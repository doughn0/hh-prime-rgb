
from utilities import mix
from copy import copy

SMOOTH = 0.1

class Palette():
    def __init__(self, bg:list[int], fg:list[int]|None=None) -> None:
        self.bg = bg
        self._bg = bg
        if fg is None:
            self.fg = bg
            self._fg = bg
        else:
            self.fg = fg
            self._fg = fg

    def __eq__(self, p2) -> bool:
        return self.fg == p2.fg and self.bg == p2.bg

    def swap(self):
        return Palette(copy(self.fg), copy(self.bg))

    def paintdrop(self, p2:'Palette'):
        if self != p2:
            self._bg = mix(self._bg, 1-SMOOTH, p2._bg, SMOOTH)
            self._fg = mix(self._fg, 1-SMOOTH, p2._fg, SMOOTH)
            self.bg = [int(round(a)) for a in self._bg]
            self.fg = [int(round(a)) for a in self._fg]
            return False
        return True

GREEN = Palette([0,255,0])
RED = Palette([255,0,0])
BLUE = Palette([0,0,255])

colors = {
    "Cyan" : [0, 200, 200],
    "Aqua" : [50, 140, 220],
    "Magenta" : [255, 0, 180],
    "Green" : [0, 255, 0],
    "Blue" : [0, 50, 255],
    "PBlue" : [0, 0, 255],
    "Mint" : [0, 255, 120],
    "Violet" : [75, 0, 255],
    "Orange" : [255, 60, 0],
    "Yellow" : [255, 200, 0],
    "Gold" : [255, 127, 0],
    "Silver" : [100, 100, 120],
    "Red" : [255, 5, 0],
    "PRed" : [255, 0, 0],
    "Pink" : [255, 50, 100],
    "White" : [255, 255, 255],
    "Black" : [0, 0, 0]
}

def get_palette(S):
    colors_ = S.split("-")
    if(len(colors_) == 1):
        c1 = colors_[0]
        ret = [colors[c1], colors[c1]]
        return ret
    if(len(colors_) == 2):
        c1 = colors_[0]
        c2 = colors_[1]
        ret = [colors[c1], colors[c2]]
        return ret