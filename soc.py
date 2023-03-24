from select import select
from memory import Memory
from cpu import Cpu
from bus import Bus
from termuart import UART
from map import MemoryMap
import logging

class Soc():
    def __init__(self,bootfile="./sw/firmware/firmware.bin",binfile=None):
        self.bootrom=Memory(32768,bootfile)
        self.ram=Memory(32768,binfile)
        self.uart=UART()
        self.map=MemoryMap()
        self.map.addperipheral(0x00000000,0x0fffffff,self.bootrom)
        self.map.addperipheral(0x10000000,0x1fffffff,self.ram)
        self.map.addperipheral(0x40000000,0x400000ff,self.uart)
        self.bus=Bus(self.map)
        self.cpu=Cpu(0x00000000,self.bus)

    def run(self,debug=True,mode="r"):
        delay=2
        if debug:
            logging.basicConfig(level="DEBUG")
            if(mode=="s"):
                self.cpu.cpu_cyc(delay)
            elif(mode=="r"):
                while self.cpu.cpu_cyc(delay)!=2:
                    pass

        else:
            logging.basicConfig(level="CRITICAL")
            if(mode=="s"):
                self.cpu.cpu_cyc(0)
            elif(mode=="r"):
                while self.cpu.cpu_cyc(0)!=2:
                    pass
                


