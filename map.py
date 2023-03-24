class MemoryMap():
    def __init__(self):
        self.adr_range_to_periph_map={}

    def addperipheral(self,addr_ranage_low,addr_range_high,peripheral):
        key=(addr_ranage_low,addr_range_high)
        self.adr_range_to_periph_map[key]=peripheral
        
    def getperipheral(self,adddress):
        for key in self.adr_range_to_periph_map:
            if adddress in range(key[0],key[1]):
                return self.adr_range_to_periph_map[key]
        return None

def test_map():
    map=MemoryMap()
    map.addperipheral(0x00000000,0x10000000,10)
    map.addperipheral(0x20000000,0x2FFFFFFF,100)
    assert map.getperipheral(0x00001111)==10
    assert map.getperipheral(0x21345678)==100
    assert map.getperipheral(0x30001111)==None