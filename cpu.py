import opcode
from bus import Bus
from ctypes import *
from isa import Isa,Instructions

class Cpu:
    def __init__(self,reset,sysbus:Bus):
        self.pc=c_uint(reset)
        self.ir=c_uint(0)
        self.mar=c_uint(0)
        self.mdr=c_uint(0)
        self.rs1=c_ubyte(0)
        self.rs2=c_ubyte(0)
        self.rd=c_ubyte(0)
        self.imm=c_int(0)
        self.size=c_ubyte(0)
        self.opcode=c_ubyte(0)
        self.func3=c_ubyte(0)
        self.func7=c_ubyte(0)
        self.shamt=c_ubyte(0)
        self.bus = sysbus
        self.res=c_uint(0)
        self.currentInstruction=Instructions.noimp
        self.isa=Isa()
        self.cpuregs=[0]*32

        self.opcodeExeMAP={
            Instructions.add:self.exeADD,
            Instructions.addi:self.exeADDI,
            Instructions.zand:self.exeAND,
            Instructions.andi:self.exeANDI,
            Instructions.lui:self.exeLUI
        }

    def fetch(self):
        self.mar=self.pc
        self.mdr=self.bus.read(self.mar)
        self.ir.value=self.mdr

    def decode(self):
        self.opcode.value=self.ir.value&0x0000007f
        self.rd.value=(self.ir.value&0x00000f80)>>7
        self.rs1.value=(self.ir.value&0x000f8000)>>15
        self.rs2.value=(self.ir.value&0x01f00000)>>20
        self.func7.value=(self.ir.value&0xfe000000)>>25
        self.func3.value=(self.ir.value&0x00007000)>>12
        self.shamt.value=self.rs2.value
        self.currentInstruction=self.isa.getInstruction(self.opcode,self.func3,self.func7)
        self.genimmediate()
        

    def execute(self):
        self.opcodeExeMAP[currentInstruction]()
        pass

    def memaccess(self):
        pass

    def writeback(self):
        pass

    #generate the immediate value based on the instruction
    def genimmediate(self):
        if(self.opcode.value==0b00110111 or self.opcode.value==0b00010111): #U type
            self.imm.value=self.ir.value&0xfffff000
        elif(self.opcode.value==0b01101111): # J type
            if(self.ir.value&0x80000000):
                tmp=0xfff00000
            else:
                tmp=0x0
            self.imm.value=((self.ir.value&0x7fe00000)>>20)|((self.ir.value&0x00100000)>>9)\
                |((self.ir.value&0x000ff000))|((self.ir.value&0x80000000)>>11)|tmp
        elif(self.opcode.value==0b01100111 or self.opcode.value==0b00000011 or self.opcode.value==0b00010011): #I types
                tmp=c_int(self.ir.value)
                self.imm.value=(tmp.value>>20)
        elif(self.opcode.value==0b01100011): #B type
            if(self.ir.value&0x80000000):
                tmp=0xfffff000
            else:
                tmp=0x0
            self.imm.value=((self.ir.value&0x00000f00)>>7) | ((self.ir.value&0x00000080)<<4) | ((self.ir.value&0x7e000000)>>20)\
                | ((self.ir.value&0x80000000)>>19) | tmp
        elif(self.opcode.value==0b00100011): # S type
            tmp=c_int(self.ir.value)
            self.imm.value=((tmp.value>>20)&0xffffffe0)|((self.ir.value>>7)&0x0000001f)
        else:
            pass

    ##execution functions for each instruction
    def exeLUI(self):
        self.cpuregs[self.rd.value]=self.imm
        self.pc+=4
    def exeADD(self):
        self.cpuregs[self.rd]=self.cpuregs[self.rs1]+self.cpuregs[self.rs2]
        self.pc+=4
    def exeADDI(self):
        self.cpuregs[self.rd]=self.cpuregs[self.rs1]+self.imm
        self.pc+=4
    def exeAND(self):
        self.cpuregs[self.rd]=self.cpuregs[self.rs1]&self.cpuregs[self.rs2]
        self.pc+=4

        
def Tests():
    bus=Bus()
    cpu = Cpu(0,bus)
    cpu.ir.value=0x00000073
    cpu.decode()
    tmp=c_int(cpu.imm.value)
    print(hex(cpu.imm.value),tmp.value)
    print(cpu.currentInstruction)

if __name__ == "__main__":
    Tests()