from select import select
from memory import BRAM
from cpu import Cpu
from bus import Bus
from termuart import UART
from map import MemoryMap

class Soc():
    def __init__(self):
        self.ram=BRAM(4096,"./sw/firmware/firmware.bin")
        self.uart=UART()
        self.map=MemoryMap()
        self.map.addperipheral(0x00000000,0x0000ffff,self.ram)
        self.map.addperipheral(0x40000000,0x400000ff,self.uart)
        self.bus=Bus(self.map)
        self.cpu=Cpu(0x00000000,self.bus,1)
    
    def run(self):
        self.cpu.cpu_cyc(0)
    
soc=Soc()
soc.run()