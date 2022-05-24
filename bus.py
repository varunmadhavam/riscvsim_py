from map import MemoryMap
class Bus:
    def __init__(self,map):
        self.map=map

    def read(self,address):
        dev=self.map.getperipheral(address)
        if dev==None:
            print("Error : Bus address out of range @ read")
            return 0xdeadbeef
        else:
            return dev.read(address)

    def write(self,address,data,size):
        dev=self.map.getperipheral(address)
        if dev==None:
            print("Error : Bus address out of range @ write")
        else:
            dev.write(address,data,size)