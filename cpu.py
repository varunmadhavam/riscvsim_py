from bus import Bus
from ctypes import *
from isa import Isa,Instructions

class Cpu:
    def __init__(self,reset,sysbus:Bus):
        #cpu gp registers
        self.cpuregs=[0]*32
        self.XLEN=32

        #cpu other registers
        self.pc=c_int(reset)
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
        self.res=c_uint(0)
        self.currentInstruction=Instructions.noimp

        self.isa=Isa()
        self.bus = sysbus
        
        self.opcodeExeMAP={
            Instructions.lui:self.exeLUI,
            Instructions.auipc:self.exeAUIPC,
            Instructions.jal:self.exeJAL,
            Instructions.jalr:self.exeJALR,
            Instructions.beq:self.exeBEQ,
            Instructions.bne:self.exeBNE,
            Instructions.blt:self.exeBLT,
            Instructions.bge:self.exeBGE,
            Instructions.bltu:self.exeBLTU,
            Instructions.bgeu:self.exeBGEU,
            Instructions.lb:self.exeSKIP,
            Instructions.lh:self.exeSKIP,
            Instructions.lw:self.exeSKIP,
            Instructions.lbu:self.exeSKIP,
            Instructions.lhu:self.exeSKIP,
            Instructions.sb:self.exeSKIP,
            Instructions.sh:self.exeSKIP,
            Instructions.sw:self.exeSKIP,
            Instructions.addi:self.exeADDI,
            Instructions.slti:self.exeSLTI,
            Instructions.sltiu:self.exeSLTIU,
            Instructions.xori:self.exeXORI,
            Instructions.ori:self.exeORI,
            Instructions.andi:self.exeANDI,
            Instructions.slli:self.exeSLLI,
            Instructions.srli:self.exeSRLI,
            Instructions.srai:self.exeSRAI,
            Instructions.add:self.exeADD,
            Instructions.sub:self.exeSUB,
            Instructions.sll:self.exeSLL,
            Instructions.slt:self.exeSLT,
            Instructions.slti:self.exeSLTU,
            Instructions.xor:self.exeXOR,
            Instructions.srl:self.exeSRL,
            Instructions.sra:self.exeSRA,
            Instructions.zor:self.exeOR,
            Instructions.zand:self.exeAND,
            Instructions.ecall:self.exeEBRK,
            Instructions.ebreak:self.exeEBRK
        }

    def cpu_cyc(self):
        while True:
            self.fetch()
            self.decode()
            self.execute()
            self.memaccess()
            self.writeback()
            
    def fetch(self):
        self.mar.value=self.pc.value
        self.mdr.value=self.bus.read(self.mar.value)
        self.ir.value=self.mdr.value

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
        self.opcodeExeMAP[self.currentInstruction]()

    def memaccess(self):
        if(self.currentInstruction in (Instructions.lb,Instructions.lbu,Instructions.lh,Instructions.lhu,Instructions.lw)):
            self.mdr.value=self.bus.read(self.mar.value)
            return 0

        elif(self.currentInstruction==Instructions.sb):
            loc=self.mar.value&0x3
            if(loc==0):
                size=0x1
            elif(loc==1):
                size=0x2
            elif(loc==2):
                size=0x4
            else:
                size=0x8
            self.bus.write(self.mar.value,self.mdr.value,size)
            return 0

        elif(self.currentInstruction==Instructions.sh):
            loc=self.mar.value&0x3
            if(loc==0):
                size=0x3
            elif(loc==2):
                size=0xC
            else:
                print("Error : Unaligned half word write")
                return 1
            self.bus.write(self.mar.value,self.mdr.value,size)
            return 0
        
        elif(self.currentInstruction==Instructions.sw):
            loc=self.mar.value&0x3
            if(loc==0):
                size=0xF
            else:
                print("Error : Unaligned word write")
                return 1
            self.bus.write(self.mar.value,self.mdr.value,size)
            return 0

        else:
            pass

    def writeback(self):
        if(self.rd.value==0):
            print("Error :  Write to reg X0")
            return 1
        elif(self.currentInstruction in (Instructions.lb,Instructions.lbu,Instructions.lh,Instructions.lhu,Instructions.lw)):
            tmp=c_uint(0)
            if(self.currentInstruction==Instructions.lb):
                size=self.mar.value&0x3
                if(size==0):
                    tmp.value=self.mdr.value&0xff
                elif(size==1):
                    tmp.value=(self.mdr.value&0xff00)>>8
                elif(size==2):
                    tmp.value=(self.mdr.value&0xff0000)>>16
                else:
                    tmp.value=(self.mdr.value&0xff000000)>>24
                if(tmp.value&0x80):
                    tmp.value|=0xffffff00
            elif(self.currentInstruction==Instructions.lbu):
                size=self.mar.value&0x3
                if(size==0):
                    tmp.value=self.mdr.value&0xff
                elif(size==1):
                    tmp.value=(self.mdr.value&0xff00)>>8
                elif(size==2):
                    tmp.value=(self.mdr.value&0xff0000)>>16
                else:
                    tmp.value=(self.mdr.value&0xff000000)>>24
            elif(self.currentInstruction==Instructions.lh):
                size=self.mar.value&0x3
                if(size==0):
                    tmp.value=self.mdr.value&0xffff
                elif(size==2):
                    tmp.value=(self.mdr.value&0xffff0000)>>16
                else:
                    print("Error: Unaligned half word read")
                    return 1
                if(tmp.value&0x8000):
                    tmp.value|=0xffff0000
            elif(self.currentInstruction==Instructions.lhu):
                size=self.mar.value&0x3
                if(size==0):
                    tmp.value=self.mdr.value&0xffff
                elif(size==2):
                    tmp.value=(self.mdr.value&0xffff0000)>>16
                else:
                    print("Error: Unaligned half word read")
                    return 1
            elif(self.currentInstruction==Instructions.lw):
                size=self.mar.value&0x3
                if(size==0):
                    tmp.value=self.mdr.value
                else:
                    print("Error: Unaligned word read")
                    return 1
            self.cpuregs[self.rd.value]=tmp.value
            return 0
        elif(self.currentInstruction not in(Instructions.beq,Instructions.bge,Instructions.bgeu,\
            Instructions.blt,Instructions.bltu,Instructions.bne,Instructions.sb,Instructions.sh,Instructions.sw)):
            self.cpuregs[self.rd.value]=self.res.value
            return 0
        else:
            return 0

    ##execution functions for each instruction
    def exeEBRK(self):
        print("Ebreak/ecall executed")
        pass

    def exeADD(self):
        self.res=self.cpuregs[self.rs1.value]+self.cpuregs[self.rs2.value]
        self.pc.value+=4

    def exeADDI(self):
        self.res=self.cpuregs[self.rs1.value]+self.imm.value
        self.pc.value+=4

    def exeAND(self):
        self.res=self.cpuregs[self.rs1.value]&self.cpuregs[self.rs2.value]
        self.pc.value+=4

    def exeANDI(self):
        self.res=self.cpuregs[self.rs1.value]&self.imm.value
        self.pc.value+=4

    def exeAUIPC(self):
        self.res=self.pc.value+self.imm.value
        self.pc.value+=4

    def exeBEQ(self):
        if(self.cpuregs[self.rs1.value]==self.cpuregs[self.rs2.value]):
            self.pc.value+=self.imm.value
        else:
            self.pc.value+=4

    def exeBGE(self):
        if(self.cpuregs[self.rs1.value]>=self.cpuregs[self.rs2.value]):
            self.pc.value+=self.imm.value
        else:
            self.pc.value+=4

    def exeBGEU(self):
        tmp1=c_uint(self.cpuregs[self.rs1.value])
        tmp2=c_uint(self.cpuregs[self.rs2.value])
        if(tmp1.value>=tmp2.value):
            self.pc.value+=self.imm.value
        else:
            self.pc.value+=4

    def exeBLT(self):
        if(self.cpuregs[self.rs1.value]<self.cpuregs[self.rs2.value]):
            self.pc.value+=self.imm.value
        else:
            self.pc.value+=4

    def exeBLTU(self):
        tmp1=c_uint(self.cpuregs[self.rs1.value])
        tmp2=c_uint(self.cpuregs[self.rs2.value])
        if(tmp1.value<tmp2.value):
            self.pc.value+=self.imm.value
        else:
            self.pc.value+=4

    def exeBNE(self):
        if(self.cpuregs[self.rs1.value]!=self.cpuregs[self.rs2.value]):
            self.pc.value+=self.imm.value
        else:
            self.pc.value+=4

    def exeJAL(self):
        self.res=self.pc.value+4
        self.pc.value+=self.imm.value

    def exeJALR(self):
        self.res=self.pc.value+4
        self.pc.value=(self.imm.value+self.cpuregs[self.rs1.value])&0xfffffffe

    def exeLB(self):
        self.mar.value=self.imm.value+self.cpuregs[self.rs1.value]
        self.pc.value+=4

    def exeLBU(self):
        self.mar.value=self.imm.value+self.cpuregs[self.rs1.value]
        self.pc.value+=4

    def exeLH(self):
        self.mar.value=self.imm.value+self.cpuregs[self.rs1.value]
        self.pc.value+=4

    def exeLHU(self):
        self.mar.value=self.imm.value+self.cpuregs[self.rs1.value]
        self.pc.value+=4

    def exeLUI(self):
        self.res=self.imm.value
        self.pc.value+=4

    def exeLW(self):
        self.mar.value=self.imm.value+self.cpuregs[self.rs1.value]
        self.pc.value+=4
    
    def exeOR(self):
        self.res=self.cpuregs[self.rs1.value]|self.cpuregs[self.rs2.value]
        self.pc.value+=4

    def exeORI(self):
        self.res=self.cpuregs[self.rs1.value]|self.imm.value
        self.pc.value+=4
    
    def exeSB(self):
        self.mar.value=self.imm.value+self.cpuregs[self.rs1.value]
        self.mdr.value=self.cpuregs[self.rs2.value]
        self.pc.value+=4
    
    def exeSH(self):
        self.mar.value=self.imm.value+self.cpuregs[self.rs1.value]
        self.mdr.value=self.cpuregs[self.rs2.value]
        self.pc.value+=4
    
    def exeSW(self):
        self.mar.value=self.imm.value+self.cpuregs[self.rs1.value]
        self.mdr.value=self.cpuregs[self.rs2.value]
        self.pc.value+=4

    def exeSLL(self):
        self.res=self.cpuregs[self.rs1.value]<<(self.cpuregs[self.rs2.value]%self.XLEN)
        self.pc.value+=4

    def exeSLLI(self):
        self.res=self.cpuregs[self.rs1.value]<<self.shamt
        self.pc.value+=4

    def exeSLT(self):
        if(self.cpuregs[self.rs1.value]<self.cpuregs[self.rs2.value]):
            self.res=1
        else:
            self.res=0
        self.pc.value+=4

    def exeSLTI(self):
        if(self.cpuregs[self.rs1.value]<self.imm.value):
            self.res=1
        else:
            self.res=0
        self.pc.value+=4
    
    def exeSLTIU(self):
        tmp1=c_uint(self.cpuregs[self.rs1.value])
        tmp2=c_uint(self.cpuregs[self.rs2.value])
        if(tmp1.value<tmp2.value):
            self.res=1
        else:
            self.res=0
        self.pc.value+=4
    
    def exeSLTU(self):
        tmp1=c_uint(self.cpuregs[self.rs1.value])
        tmp2=c_uint(self.imm.value)
        if(tmp1.value<tmp2.value):
            self.res=1
        else:
            self.res=0
        self.pc.value+=4
    
    def exeSRL(self):
        tmp=c_uint(self.cpuregs[self.rs1.value])
        self.res=(tmp.value)>>(self.cpuregs[self.rs2.value]%self.XLEN)
        self.pc.value+=4

    def exeSRLI(self):
        tmp=c_uint(self.cpuregs[self.rs1.value])
        self.res=(tmp.value)>>self.shamt
        self.pc.value+=4
    
    def exeSRA(self):
        self.res=self.cpuregs[self.rs1.value]>>(self.cpuregs[self.rs2.value]%self.XLEN)
        self.pc.value+=4

    def exeSRAI(self):
        self.res=self.cpuregs[self.rs1.value]>>self.shamt
        self.pc.value+=4
    
    def exeSUB(self):
        self.res=self.cpuregs[self.rs1.value]-self.cpuregs[self.rs2.value]
        self.pc.value+=4
    
    def exeXOR(self):
        self.res=self.cpuregs[self.rs1.value]^self.cpuregs[self.rs2.value]
        self.pc.value+=4

    def exeXORI(self):
        self.res=self.cpuregs[self.rs1.value]^self.imm.value
        self.pc.value+=4

    def exeSKIP(self):
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
        
def test_cpu():
    bus=Bus()
    cpu = Cpu(0,bus)
    cpu.ir.value=0x00177713
    cpu.decode()
    tmp=c_int(cpu.imm.value)
    print(hex(cpu.imm.value),tmp.value)
    print(cpu.currentInstruction)
    cpu.execute()

if __name__ == "__main__":
    test_cpu()