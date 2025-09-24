from bottle import run, route, get, request
from colors import BLUE, GREEN, RED, Palette
from state import RGBState, Event, EventType
from utilities import hex_to_rgb
from copy import deepcopy

STATE = RGBState.get()

presets = {
    'battery_charging': [
        Event(EventType.RunEffect, 'noti_up', 3, GREEN),
    ],
    'battery_full': [
        Event(EventType.RunEffect, 'noti_up', 1, GREEN),
        Event(EventType.RunEffect, 'noti_round', 1, GREEN),
        Event(EventType.RunEffect, 'noti_blink_off', 1, GREEN),
    ],
    'battery_low': [
        Event(EventType.RunEffect, 'noti_blink', 3, RED),
    ],
    'cheevo': [
        Event(EventType.RunEffect, 'noti_cheevo', 1),
    ]
}

def run_preset_effect(preset):
    STATE.events.append(Event(EventType.FadeOut))
    for e in preset:
        STATE.events.append(deepcopy(e))
    STATE.events.append(Event(EventType.FadeIn))

@get("/reload-config")
def json():
    STATE.events.append(Event(EventType.LoadConfig))
    return ""

@route("/animation", method='POST')
def animation():
    req = request.body.read().decode() # pyright: ignore[reportAttributeAccessIssue]
    if req == 'charging':
        run_preset_effect(presets['battery_charging'])
    elif req == 'cheevo':
        run_preset_effect(presets['cheevo'])
    elif req == 'battery_low':
        run_preset_effect(presets['battery_low'])
    elif req == 'battery_full':
        run_preset_effect(presets['battery_full'])
    else:
        req_ = req.split()
        try:
            if len(req_):
                STATE.events.append(Event(EventType.FadeOut))
                STATE.events.append(Event(EventType.RunEffect, req_[0], int(req_[1]), Palette(hex_to_rgb(req_[2]))))
        except Exception as e:
            return "Error while processing Command:\n[name] [count] [hex_color]\n"
    return ""


batt_last = ''
@route("/update-battery-state", method='POST')
def battery():
    global batt_last
    req = request.body.read().decode().split() # pyright: ignore[reportAttributeAccessIssue]
    if req[1] != batt_last and req[1] == 'Charging':
        run_preset_effect(presets['battery_charging'])
    if req[1] != batt_last and req[1] == 'Full':
        run_preset_effect(presets['battery_full'])
    batt_last = req[1]
    pass

@route("/update-screen-state", method='POST')
def screen():
    pass

@get("/kill")
def kill():
    STATE.events.append(Event(EventType.FadeOut))
    STATE.events.append(Event(EventType.Die))


def run_api():
    run(host='localhost', port=1235)

if __name__ == '__main__':
    run_api()