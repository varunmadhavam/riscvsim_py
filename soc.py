from select import select
from memory import BRAM
from cpu import Cpu
from bus import Bus
from termuart import UART
from map import MemoryMap
import logging
import sys
import signal
import sys

class Soc():
    def __init__(self,bootfile="./sw/firmware/firmware.bin",binfile=None):
        self.bootrom=BRAM(32768,bootfile)
        self.ram=BRAM(32768,binfile)
        self.uart=UART()
        self.map=MemoryMap()
        self.map.addperipheral(0x00000000,0x0fffffff,self.bootrom)
        self.map.addperipheral(0x10000000,0x1fffffff,self.ram)
        self.map.addperipheral(0x40000000,0x400000ff,self.uart)
        self.bus=Bus(self.map)
        self.cpu=Cpu(0x00000000,self.bus)
    
    def run(self,debug=True):
        if debug:
            logging.basicConfig(level="DEBUG")
            self.cpu.cpu_cyc(0)
        else:
            logging.basicConfig(level="CRITICAL")
            self.cpu.cpu_cyc(0)

def run():
    n=len(sys.argv)
    if   n==1:
        bootfile="./sw/app/bootloader/firmware.bin"
        binfile="./sw/app/main_app/firmware/firmware.bin"
    elif n==2:
        bootfile="./sw/test/firmware/firmware.bin"
        binfile=None
    else:
        print("Usage : python3 soc.py [test] ")
    soc=Soc(bootfile,binfile)
    soc.run(debug=False)

def signal_handler(signum, frame):
    signal.signal(signum, signal.SIG_IGN)
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

run()

