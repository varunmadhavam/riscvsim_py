from map import MemoryMap
import logging
class Bus:
    def __init__(self,map):
        self.map=map

    def read(self,address):
        dev=self.map.getperipheral(address)
        logging.debug("Read @ "+str(hex(address))+" from "+str(dev))
        if dev==None:
            logging.critical("Error : Bus address out of range @ read : "+str(hex(address)))
            return 0xdeadbeef
        else:
            return dev.read(address)

    def write(self,address,data,size):
        dev=self.map.getperipheral(address)
        logging.debug("Write @ "+str(hex(address))+" from "+str(dev))
        if dev==None:
            logging.critical("Error : Bus address out of range @ write : "+str(hex(address)))
        else:
            dev.write(address,data,size)