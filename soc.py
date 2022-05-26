from select import select
from memory import BRAM
from cpu import Cpu
from bus import Bus
from termuart import UART
from map import MemoryMap
import logging
import sys

class Soc():
    def __init__(self,binfile="./sw/firmware/firmware.bin"):
        self.ram=BRAM(32768,binfile)
        self.uart=UART()
        self.map=MemoryMap()
        self.map.addperipheral(0x00000000,0x30000000,self.ram)
        self.map.addperipheral(0x40000000,0x400000ff,self.uart)
        self.bus=Bus(self.map)
        self.cpu=Cpu(0x00000000,self.bus)
    
    def run(self,debug=True):
        if debug:
            logging.basicConfig(level="DEBUG")
            self.cpu.cpu_cyc(1)
        else:
            logging.basicConfig(level="CRITICAL")
            self.cpu.cpu_cyc(0)

n=len(sys.argv)
if   n==1:
    binfile="./sw/firmware/firmware.bin"
elif n==2:
    binfile="./sw/test/firmware/firmware.bin"
else:
    print("Usage : python3 soc.py [test] ")
soc=Soc(binfile)
soc.run(debug=False)
