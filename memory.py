from ctypes import *
import logging
import sys
class BRAM:
    def __init__(self,memsize=4096,binfile=""):
        self.RAM=[0]*memsize
        self.mem_size=memsize
        self.init_mem(binfile)

    def read(self,address):
        addr=address>>2
        if(addr<self.mem_size*4):
            return self.RAM[addr]
        else:
            logging.critical("BRAM : Bus address out of range @ read : "+str(hex(address)) +" "+ str(self.mem_size*4))
            sys.exit(1)

    def init_mem(self,binfile):
        file=open(binfile,"rb")
        addr=0
        while word:=file.read(4): 
            val=0
            val|=word[0]
            val|=word[1]<<8
            val|=word[2]<<16
            val|=word[3]<<24
            self.RAM[addr]=val
            addr+=1

    def write(self,address,data,size):
        addr=address>>2
        if(addr<self.mem_size*4):
            orig=self.RAM[addr]
            if(size&1):
                orig&=~(0x000000ff)
                orig|=data&0x000000ff
            if(size&2):
                orig&=~(0x0000ff00)
                orig|=data&0x0000ff00
            if(size&4):
                orig&=~(0x00ff0000)
                orig|=data&0x00ff0000
            if(size&8):
                orig&=~(0xff000000)
                orig|=data&0xff000000
            self.RAM[addr]=orig
        else:
            logging.critical("BRAM : Bus address out of range @ write : "+str(hex(address))+" "+ str(self.mem_size*4))
            sys.exit(1)

#to run unit tests do pytest ./memory.py
def test_bram():
    import random
    bram=BRAM(binfile="test.bin")
    assert bram.RAM[0x00>>2] == 0x0040006f
    assert bram.RAM[0xe8>>2] == 0x00000537
    assert bram.RAM[0xc0>>2] == 0xfedff06f
    
    #word read / writes
    for i in range(0,100):
        addr=random.randrange(0,4096)
        val=random.randrange(0,0xffffffff)
        bram.write(addr,val,15)
        assert bram.read(addr) == val
        val=0xaaaaaaaa
        bram.write(addr,val,15)
        assert bram.read(addr) == val
        val=0x55555555
        bram.write(addr,val,15)
        assert bram.read(addr) == val

    #byte read writes
    for i in range(0,100):
        addr=random.randrange(0,4096)
        val=0xffffffff
        bram.write(addr,val,15)
        assert bram.read(addr) == val
        size=random.choice([1,2,4,8])
        val=0xaaaaaaaa
        bram.write(addr,val,size)
        val=bram.read(addr)
        if(size==1):
            assert val==0xffffffaa
        elif(size==2):
            assert val==0xffffaaff
        elif(size==4):
            assert val==0xffaaffff
        else:
            assert val==0xaaffffff

    #half word read writes
    for i in range(0,100):
        addr=random.randrange(0,4096)
        val=0xffffffff
        bram.write(addr,val,15)
        assert bram.read(addr) == val
        size=random.choice([3,12])
        val=0xaaaaaaaa
        bram.write(addr,val,size)
        val=bram.read(addr)
        if(size==3):
            assert val==0xffffaaaa
        else:
            assert val==0xaaaaffff

if __name__ == "__main__":
    test_bram()