import json
from colors import Palette
from device import Device
from effects.noti_up import Effect

_INSTANCE:'RGBState|None' = None

class RGBState:
    def __init__(self) -> None:
        self.DEV = Device()
        self.BR = 255
        self.PAL = [Palette([0,0,0], [0,0,0]), Palette([0,0,0], [0,0,0])]
        self._target_palette = [Palette([0,0,0], [0,0,0]), Palette([0,0,0], [0,0,0])]
        self._target_br = 255

        self.FPS = 30
        self.FRTM = int(1000 / self.FPS)

        self.modes = [Effect(self.DEV, 0)]
        self.events = []
    
    @staticmethod
    def get() -> 'RGBState':
        global _INSTANCE
        if _INSTANCE is None:
            _INSTANCE = RGBState()
        return _INSTANCE

    def render(self, TICK):
        
        mode = self.modes[-1]

        conf_done = self.smooth_conf()
        mode.prepare()

        framekey = mode.framekey(TICK)
        if not self.DEV.recall(framekey):
            mode.apply(TICK, self.PAL)
            if conf_done:
                self.DEV.savestate(framekey)

    def write(self):
        self.DEV.write()
    
    def load_config(self):
        config = json.load(open('config.json'))

        print(config)
        self.DEV.nuke_savestates()

        raw_palette = config['palette']
        self._target_palette = [Palette(*raw_palette), Palette(*raw_palette)]
        if config['palette_swap']:
            self._target_palette = [p.swap() for p in self._target_palette]
        if config['palette_swap_secondary']:
            self._target_palette[1] = self._target_palette[1].swap()
    
    def smooth_conf(self):

        done = True

        for i in range(2):
            done = self.PAL[i].paintdrop(self._target_palette[i]) and done
        
        return done