from enum import Enum
from memory import BRAM
from termuart import UART

class MemoryMap(Enum):
    NOMAP=0
    BRAM=1
    UART=2
    def getperipheral(self,adddress):
        if adddress in range(0x00000000,0x3fffffff):
            return MemoryMap.BRAM
        elif adddress in range(0x40000000,0x4000ffff):
            return MemoryMap.UART
        else:
            return MemoryMap.NOMAP
class Bus:
    def __init__(self):
        self.map=MemoryMap()
        self.uart=UART()
        self.bram=BRAM()
        self.nomap=Nomap()
        self.periphMAP={
                        MemoryMap.BRAM:self.bram,
                        MemoryMap.UART:self.uart,
                        MemoryMap.NOMAP:self.nomap
                       }
    def read(self,address):
        self.periphMAP[MemoryMap.getperipheral(address)].read(address)
    def write(self,address,data,size):
        self.periphMAP[MemoryMap.getperipheral(address)].write(address,data,size)

class Nomap:
    def read(address):
        print("Error : Bus address out of range @ read")
        return 0xdeadbeef
    def write(address,data,size):
        print("Error : Bus address out of range @ write")