
import os

SERIAL_PORT = '/dev/ttyS5'

def calculate_checksum(data:list[int]) -> int:
    return sum(data) & 0xFF
    
class RGBDriver:

    header = [1, 255] # mode 1, which is the mode where you can do raw rendering and max brightness (we will do that manually one layer above...)

    def __init__(self, extra) -> None:
        
        ## set up the serial port
        self.rgb_serial = os.open(SERIAL_PORT, os.O_RDWR | os.O_NOCTTY | os.O_NONBLOCK) # type: ignore

    # expects a list of rgb values [[255,0,0], ... ]
    def render(self, rgb_data:list[int]) -> bytes:
        all_data = self.header + rgb_data
        checksum = calculate_checksum(all_data)

        return bytes(all_data+[checksum])
    
    def write(self, bytes:bytes):
        os.write(self.rgb_serial, bytes)
    
    def close(self) -> None:        
        os.close(self.rgb_serial)

    

