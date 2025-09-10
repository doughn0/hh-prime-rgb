from bottle import run, route, get, request
from colors import BLUE, GREEN, RED, Palette
from state import RGBState, Event, EventType
from utilities import hex_to_rgb

STATE = RGBState.get()

@get("/reload-config")
def json():
    STATE.load_config()
    return ""

@route("/animation", method='POST')
def animation():
    req = request.body.read().decode() # pyright: ignore[reportAttributeAccessIssue]
    if req == 'charging':
        STATE.events.append(Event(EventType.FadeOut))
        STATE.events.append(Event(EventType.RunEffect, 'noti_up', 3, GREEN))
    elif req == 'cheevo':
        STATE.events.append(Event(EventType.FadeOut))
        STATE.events.append(Event(EventType.RunEffect, 'noti_cheevo', 1))
    elif req == 'battery_low':
        STATE.events.append(Event(EventType.FadeOut))
        STATE.events.append(Event(EventType.RunEffect, 'noti_blink', 3, RED))
    else:
        req_ = req.split()
        try:
            if len(req_):
                STATE.events.append(Event(EventType.FadeOut))
                STATE.events.append(Event(EventType.RunEffect, req_[0], int(req_[1]), Palette(hex_to_rgb(req_[2]))))
        except Exception as e:
            return "Error while processing Command:\n[name] [count] [hex_color]\n"
    return ""

def run_api():
    run(host='localhost', port=1235)

if __name__ == '__main__':
    run_api()