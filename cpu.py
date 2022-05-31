from multiprocessing.connection import wait
import sys
from time import sleep
from bus import Bus
from ctypes import *
from isa import Isa,Instructions
import logging
import array

class Cpu:
    def __init__(self,reset,sysbus:Bus):
        #cpu gp registers
        self.cpuregs=array.array('i',(0 for i in range(0,32)))
        self.XLEN=32
        #break point list
        self.bp_list={}
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
        self.res=c_int(0)
        self.currentInstruction=Instructions.noimp

        self.isa = Isa()
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
            Instructions.lb:self.exeLB,
            Instructions.lh:self.exeLH,
            Instructions.lw:self.exeLW,
            Instructions.lbu:self.exeLBU,
            Instructions.lhu:self.exeLHU,
            Instructions.sb:self.exeSB,
            Instructions.sh:self.exeSH,
            Instructions.sw:self.exeSW,
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
            Instructions.sltu:self.exeSLTU,
            Instructions.xor:self.exeXOR,
            Instructions.srl:self.exeSRL,
            Instructions.sra:self.exeSRA,
            Instructions.zor:self.exeOR,
            Instructions.zand:self.exeAND,
            Instructions.ecall:self.exeEBRK,
            Instructions.ebreak:self.exeEBRK
        }

    def add_bp(self,bp):
        self.bp_list[bp]=0

    def rm_bp(self,bp):
        self.bp_list.pop(bp)

    def dump_regs(self):
        for i in range(0,32):
            print("X{}={}".format(i,hex(self.cpuregs[i]&(2**32-1))))

    def cpu_cyc(self,delay):
        if self.pc.value in self.bp_list:
            if self.bp_list[self.pc.value]==0:
                self.bp_list[self.pc.value]=1
                return 2
            else:
                self.bp_list[self.pc.value]=0
        self.fetch()
        self.decode()
        self.execute()
        self.memaccess()
        self.writeback()
        sleep(delay)
        if logging.root.level == logging.DEBUG :
            self.dump_regs()
            print("")
            
    def fetch(self):
        self.mar.value=self.pc.value
        self.mdr.value=self.bus.read(self.mar.value)
        self.ir.value=self.mdr.value
        logging.debug("pc : "+hex(self.pc.value))
        logging.debug("fetched : "+hex(self.ir.value))

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
        logging.debug("opcode={} | rd={} | rs1={} | rs2={} | func3={} | func7={} | shmat={} | imm={} | Inst={}".format(hex(self.opcode.value),self.rd.value,self.rs1.value,self.rs2.value,hex(self.func3.value),hex(self.func7.value),self.shamt.value,self.imm.value,self.currentInstruction))
        
    def execute(self):
        logging.debug("executng : "+str(self.opcodeExeMAP[self.currentInstruction]))
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
                self.mdr.value=self.mdr.value<<8
            elif(loc==2):
                size=0x4
                self.mdr.value=self.mdr.value<<16
            else:
                size=0x8
                self.mdr.value=self.mdr.value<<24
            self.bus.write(self.mar.value,self.mdr.value,size)
            return 0

        elif(self.currentInstruction==Instructions.sh):
            loc=self.mar.value&0x3
            if(loc==0):
                size=0x3
            elif(loc==2):
                size=0xC
                self.mdr.value=self.mdr.value<<16
            else:
                logging.critical("MEMACCESS : Unaligned half word write")
                return 1
            logging.debug("Write to => "+str(hex(self.mar.value))+" "+str(hex(self.mdr.value))+" "+str(hex(size)))
            self.bus.write(self.mar.value,self.mdr.value,size)
            return 0
        
        elif(self.currentInstruction==Instructions.sw):
            loc=self.mar.value&0x3
            if(loc==0):
                size=0xF
            else:
                logging.critical("MEMACCESS : Unaligned word write")
                return 1
            self.bus.write(self.mar.value,self.mdr.value,size)
            return 0

        else:
            pass

    def writeback(self):
        if(self.currentInstruction in (Instructions.lb,Instructions.lbu,Instructions.lh,Instructions.lhu,Instructions.lw)):
            tmp=c_int(0)
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
                    logging.critical("MEMACCESS Unaligned half word read")
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
                    logging.critical("MEMACCESS Unaligned half word read")
                    return 1
            elif(self.currentInstruction==Instructions.lw):
                size=self.mar.value&0x3
                if(size==0):
                    tmp.value=self.mdr.value
                else:
                    logging.critical("MEMACCESS Unaligned word read")
                    return 1
            self.cpuregs[self.rd.value]=tmp.value
            return 0
        elif(self.currentInstruction not in(Instructions.beq,Instructions.bge,Instructions.bgeu,\
            Instructions.blt,Instructions.bltu,Instructions.bne,Instructions.sb,Instructions.sh,Instructions.sw)):
            if(self.rd.value==0):
                logging.info("Write to reg X0")
                return 0
            else:
                self.cpuregs[self.rd.value]=self.res.value
                return 0
        else:
            return 0

    ##execution functions for each instruction
    def exeEBRK(self):
        logging.info("Ebreak/ecall executed")
        sys.exit(0)

    def exeADD(self):
        self.res.value=self.cpuregs[self.rs1.value]+self.cpuregs[self.rs2.value]
        self.pc.value+=4

    def exeADDI(self):
        self.res.value=self.cpuregs[self.rs1.value]+self.imm.value
        self.pc.value+=4

    def exeAND(self):
        self.res.value=self.cpuregs[self.rs1.value]&self.cpuregs[self.rs2.value]
        self.pc.value+=4

    def exeANDI(self):
        self.res.value=self.cpuregs[self.rs1.value]&self.imm.value
        self.pc.value+=4

    def exeAUIPC(self):
        self.res.value=self.pc.value+self.imm.value
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
        self.res.value=self.pc.value+4
        self.pc.value+=self.imm.value

    def exeJALR(self):
        self.res.value=self.pc.value+4
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
        self.res.value=self.imm.value
        self.pc.value+=4

    def exeLW(self):
        self.mar.value=self.imm.value+self.cpuregs[self.rs1.value]
        self.pc.value+=4
    
    def exeOR(self):
        self.res.value=self.cpuregs[self.rs1.value]|self.cpuregs[self.rs2.value]
        self.pc.value+=4

    def exeORI(self):
        self.res.value=self.cpuregs[self.rs1.value]|self.imm.value
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
        self.res.value=self.cpuregs[self.rs1.value]<<(self.cpuregs[self.rs2.value]%self.XLEN)
        self.pc.value+=4

    def exeSLLI(self):
        self.res.value=self.cpuregs[self.rs1.value]<<self.shamt.value
        self.pc.value+=4

    def exeSLT(self):
        if(self.cpuregs[self.rs1.value]<self.cpuregs[self.rs2.value]):
            self.res.value=1
        else:
            self.res.value=0
        self.pc.value+=4

    def exeSLTI(self):
        if(self.cpuregs[self.rs1.value]<self.imm.value):
            self.res.value=1
        else:
            self.res.value=0
        self.pc.value+=4
    
    def exeSLTIU(self):
        tmp1=c_uint(self.cpuregs[self.rs1.value])
        tmp2=c_uint(self.imm.value)
        if(tmp1.value<tmp2.value):
            self.res.value=1
        else:
            self.res.value=0
        self.pc.value+=4
    
    def exeSLTU(self):
        tmp1=c_uint(self.cpuregs[self.rs1.value])
        tmp2=c_uint(self.imm.value)
        if(tmp1.value<tmp2.value):
            self.res.value=1
        else:
            self.res.value=0
        self.pc.value+=4
    
    def exeSRL(self):
        tmp=c_uint(self.cpuregs[self.rs1.value])
        self.res.value=(tmp.value)>>(self.cpuregs[self.rs2.value]%self.XLEN)
        self.pc.value+=4

    def exeSRLI(self):
        tmp=c_uint(self.cpuregs[self.rs1.value])
        self.res.value=(tmp.value)>>self.shamt.value
        self.pc.value+=4
    
    def exeSRA(self):
        self.res.value=self.cpuregs[self.rs1.value]>>(self.cpuregs[self.rs2.value]%self.XLEN)
        self.pc.value+=4

    def exeSRAI(self):
        self.res.value=self.cpuregs[self.rs1.value]>>self.shamt.value
        self.pc.value+=4
    
    def exeSUB(self):
        self.res.value=self.cpuregs[self.rs1.value]-self.cpuregs[self.rs2.value]
        self.pc.value+=4
    
    def exeXOR(self):
        self.res.value=self.cpuregs[self.rs1.value]^self.cpuregs[self.rs2.value]
        self.pc.value+=4

    def exeXORI(self):
        self.res.value=self.cpuregs[self.rs1.value]^self.imm.value
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
    cpu = Cpu(0,None)
    cpu.ir.value=0x060000ef
    cpu.decode()
    tmp=c_int(cpu.imm.value)
    print(hex(cpu.imm.value),tmp.value)
    print(cpu.currentInstruction)
    cpu.execute()

if __name__ == "__main__":
    test_cpu()