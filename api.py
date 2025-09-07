from bottle import run, route, get, post
from state import RGBState

STATE = RGBState.get()

@get("/reload-config")
def json():
    STATE.load_config()
    return ""

@post("/animation")
def animation():
    
    return ""

def run_api():
    run(host='localhost', port=1235)

if __name__ == '__main__':
    run_api()