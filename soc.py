from memory import BRAM
from cpu import Cpu
from bus import Bus
from termuart import UART

class soc():
    def __init__(self):
        self.ram=BRAM(4096,"../sw/firmware/firmware.bin")
        self.bus=Bus()