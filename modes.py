from device import Device
from utilities import color_upscale, hsv_fl as hsv, sin100, mix, dimm, loop_d
from random import randint
from joystick import StickState

def rainbow1_l(dev:Device, t, palette):
    key = (-t / 2 / dev.FPS) % 1
    if dev.recall(key):
        return
    
    for i in range(dev.LED_COUNT):
        dev[i] = color_upscale(hsv((key + i / dev.LED_COUNT) % 1, 1, 0.5))
    dev.savestate(key)

def frame_test(dev: Device, t, palette):
    pri = palette[0]
    sec = palette[1]
    for i in range(dev.LED_COUNT):
        if i == (t % dev.LED_COUNT):
            dev[i] = sec
        else: 
            dev[i] = pri


def notification_up(dev:Device, t, palette):
    fg = palette[0]
    
    for r in dev.Z.Rings:
        for x in range(r.COUNT):
            td = (t*15) % 420
            _d = abs(td - abs(loop_d(r.ANGLES[x], 180, 360)) - 120)
            if(_d < 120):
                r[x] = dimm(fg, 1 - abs(_d) / 120)
            else:
                r[x] = [0, 0, 0]

def ring_on(dev:Device, t, palette):
    fg = palette[0]

    for r in dev.Z.Rings:
        for x in range(r.COUNT):
            td = t*12 % 360
            if r.ANGLES[x] < td - 40:
                r[x] = fg
            elif td - 40 <= r.ANGLES[x] < td:
                _p = ((r.ANGLES[x] - td) / 40) % 1
                r[x] = dimm(fg, 1-_p)
            else:
                r[x] = [0,0,0]


shimmer_density = 4
shimmer_table_ = [randint(0, shimmer_density)]
while len(shimmer_table_) < 50:
    n = randint(0, shimmer_density)
    if shimmer_table_[-1] != n:
        shimmer_table_.append(n)

def shimmer_2(dev, t, palette):
    pri = palette[0]
    sec = palette[1]
    
    for i in range(dev.LED_COUNT):
        t_ = ((t/2+7*i) / dev.FPS) % shimmer_density
        if int(t_) == shimmer_table_[i]:
            prog = int(sin100(int(((t_%1)*100))) * 52)
            dev[i] = mix(pri, 52-prog, sec, prog*4)
        else:
            dev[i] = dimm(pri, 52)