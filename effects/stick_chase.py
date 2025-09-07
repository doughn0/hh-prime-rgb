from effects._base_effect import BaseEffect
from device import Device
from joystick import StickState
from utilities import loop_d, mix, dimm

_metadata = {
    'name': 'Stick Chase',
    'reqs': []
}

class Effect(BaseEffect):
    def __init__(self, dev: Device, initial_tick: int) -> None:
        super().__init__(dev, initial_tick)
        self.bg_scale = 0.3
        self.ST = StickState(dev.CONFIG['zones'])
    
    def prepare(self):
        self.ST.update(False)
    
    def apply(self, t, palettes):
        self.ST.update(False)
        for r in self.dev.Z.Rings:
            p = palettes[r.PAL_ID]
            s = self.ST[r.ID]
            for x in range(r.COUNT):
                if s['value'] > 0.3:
                    _p = (90 - abs(loop_d(r.ANGLES[x], s['angle'], 360))) / 90
                    if _p > 0:
                        __p = (_p*((s['value']-0.3)/0.7))
                        r[x] = mix(p.fg, __p, p.bg, self.bg_scale*(1-__p))
                    else:
                        r[x] = dimm(p.bg, self.bg_scale)
                else:
                    r[x] = dimm(p.bg, self.bg_scale)
    
    def framekey(self, t):
        key = 1
        for r in self.dev.Z.Rings:
            s = self.ST[r.ID]
            key *= 1000
            key += s['angle']
            key *= 100
            key += int(s['value']*99)
        return key