from enum import Enum
import json
from colors import Palette
from device import Device
from effect_store import STORE
from effects._base_effect import BaseEffect
from utilities import generate_brightness_list

BRIGHTNESS = generate_brightness_list(15, 255)
MAX_BR = len(BRIGHTNESS)-1

print(BRIGHTNESS)

class RGBState:
    def __init__(self) -> None:
        self.DEV = Device()
        self._br = MAX_BR
        self._tr = MAX_BR
        self._palette = [Palette([0,0,0], [0,0,0]), Palette([0,0,0], [0,0,0])]
        self._target_palette = [Palette([0,0,0], [0,0,0]), Palette([0,0,0], [0,0,0])]
        self._target_br = MAX_BR
        self._target_tr = MAX_BR

        self._tick = 0

        self.FPS = 30
        self.FRTM = int(1000 / self.FPS)

        self._mode = 'null'
        self.modes:list[BaseEffect] = [STORE['null']['class'](self.DEV, self._tick)]
        self.events:list[Event] = [
            Event(EventType.RunEffect, 'noti_round', 1, Palette(bg=[255,255,255], fg=[255,255,255])),
            Event(EventType.RunEffect, 'noti_blink_off', 1, Palette(bg=[255,255,255], fg=[255,255,255]))
        ]
    
    @staticmethod
    def get() -> 'RGBState':
        global _INSTANCE
        if _INSTANCE is None:
            _INSTANCE = RGBState()
        return _INSTANCE

    def manage_events(self):
        if len(self.events) > 0:
            event = self.events[0]
            if event.type == EventType.FadeIn:
                self.DEV.nuke_savestates()
                self._target_tr = MAX_BR
                self.events.pop(0)
            if event.type == EventType.FadeOut:
                if not event.running:
                    self.DEV.nuke_savestates()
                    self._target_tr = 0
                    event.running = True
                if(int(self._tr) == 0):
                    self.events.pop(0)
            if event.type == EventType.ChangeMode:
                self.modes[0] = STORE[event.payload]['class'](self.DEV, self._tick)
                self._tr = 0
                self.events.pop(0)
                self.DEV.nuke_savestates()
                self.events.append(Event(EventType.FadeIn))
            if event.type == EventType.RunEffect:
                if not event.running:
                    self.DEV.nuke_savestates()
                    self._tr = MAX_BR
                    self._target_tr = MAX_BR
                    event.running = True
                    self.modes.append(STORE[event.payload]['class'](self.DEV, self._tick))
                    event.timer = event.repeat * STORE[event.payload]['metadata']['duration']
                else:
                    event.timer -= 1
                    if event.timer == 0:
                        self.events.pop(0)
                        self.modes.pop()
                        self._tr = 0
                        self.DEV.nuke_savestates()
                        self.events.append(Event(EventType.FadeIn))
                        return True

    def get_palette(self):
        if len(self.events) > 0:
            if self.events[0].palette is not None:
                return [self.events[0].palette, self.events[0].palette]
        return self._palette

    def render(self, TICK):
        self._tick = TICK
        while self.manage_events(): pass
        mode = self.modes[-1]
        conf_done = self.smooth_conf()
        mode.prepare()

        framekey = mode.framekey(TICK)
        if not self.DEV.recall(framekey):
            mode.apply(TICK, self.get_palette())
            if conf_done:
                self.DEV.savestate(framekey)

    def write(self):
        self.DEV.write()
    
    def load_config(self):
        config = json.load(open('config.json'))

        print(config)
        self.DEV.nuke_savestates()

        if config['mode'] != self._mode:
            self.events.append(Event(EventType.FadeOut))
            self.events.append(Event(EventType.ChangeMode, config['mode']))
            self._mode = config['mode']

        raw_palette = config['palette']
        self._target_palette = [Palette(*raw_palette), Palette(*raw_palette)]
        if config['palette_swap']:
            self._target_palette = [p.swap() for p in self._target_palette]
        if config['palette_swap_secondary']:
            self._target_palette[1] = self._target_palette[1].swap()
    
    def smooth_conf(self):

        done = True

        for i in range(2):
            done = self._palette[i].paintdrop(self._target_palette[i]) and done
        
        if self._br != self._target_br:
            self._br += -1 if self._target_br < self._br else 1
            done = False

        if self._tr != self._target_tr:
            self._tr += -1 if self._target_tr < self._tr else 1
            done = False
        
        self.DEV.BR = BRIGHTNESS[int(self._tr*self._br) // len(BRIGHTNESS)]
        
        return done

_INSTANCE:RGBState|None = None

class EventType(Enum):
    ChangeMode = 0
    RunEffect = 1
    FadeOut = 10
    FadeIn = 11

class Event:
    def __init__(self, type:EventType, payload:str='', repeat:int=1, palette:Palette|None=None) -> None:
        self.type = type
        self.payload = payload
        self.repeat = repeat
        self.palette = palette
        self.timer = 0
        self.running = False
    
    def __str__(self) -> str:
        return f'Event: {self.type}/{self.payload}'