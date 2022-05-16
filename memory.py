from ctypes import *
class BRAM:
    def __init(self,mem_size=4096):
        self.RAM=[0]*mem_size
        self.mem_size=mem_size

    def read(self,address):
        addr=address>>2
        if(addr<self.mem_size):
            return self.RAM[addr]
        else:
            print("Error : memory address out of range @ read")

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
        if(addr<self.mem_size):
            orig=self.RAM[addr]
            if(size&1):
                orig|=size&0x000000ff
            if(size&2):
                orig|=size&0x0000ff00
            if(size&4):
                orig|=size&0x00ff0000
            if(size&8):
                orig|=size&0xff000000
            self.RAM[addr]=orig
        else:
            print("Error : memory address out of range @ write")