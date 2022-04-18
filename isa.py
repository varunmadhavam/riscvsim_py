from enum import Enum
from ctypes import *
class Instructions(Enum):
    lui=0
    auipc=1
    jal=2
    jalr=3
    beq=4
    bne=5
    blt=6
    bge=7
    bltu=8
    bgeu=9
    lb=10
    lh=11
    lw=12
    lbu=13
    lhu=14
    sb=15
    sh=16
    sw=17
    addi=18
    slti=19
    sltiu=20
    xori=21
    ori=22
    andi=23
    slli=24
    srli=25
    srai=26
    add=27
    sub=28
    sll=29
    slt=30
    sltu=31
    xor=33
    srl=34
    sra=35
    zor=36
    zand=37
    ecall=38
    ebreak=39
    csrrw=40
    csrrs=41
    csrrc=42
    csrwi=43
    csrrsi=44
    csrrci=45
    noimp=99

class Isa():
    def __init__(self):
        self.func7MAPecall={ #ecall not implemented..Will be treated as ebreaks
            0b00000000:Instructions.ebreak
        }
        self.func7MAPshfti={
            0b00000000:Instructions.srli,
            0b00100000:Instructions.srai
        }
        self.func7MAPshft={
            0b00000000:Instructions.srl,
            0b00100000:Instructions.sra
        }
        self.func7MAPaddsub={
            0b00000000:Instructions.add,
            0b00100000:Instructions.sub
        }
        self.func3MAPB={
            0b00000000:Instructions.beq,
            0b00000001:Instructions.bne,
            0b00000100:Instructions.blt,
            0b00000101:Instructions.bge,
            0b00000110:Instructions.bltu,
            0b00000111:Instructions.bgeu
        }
        self.func3MAPS={
            0b00000000:Instructions.sb,
            0b00000001:Instructions.sh,
            0b00000010:Instructions.sw
        }
        self.func3MAPI1={
            0b00000000:Instructions.lb,
            0b00000001:Instructions.lh,
            0b00000010:Instructions.lw,
            0b00000100:Instructions.lbu,
            0b00000101:Instructions.lhu
        }
        self.func3MAPI2={
            0b00000000:Instructions.addi,
            0b00000001:Instructions.slli,
            0b00000010:Instructions.slti,
            0b00000011:Instructions.sltiu,
            0b00000100:Instructions.xori,
            0b00000101:self.func7MAPshfti,
            0b00000110:Instructions.ori,
            0b00000111:Instructions.andi
        }
        self.func3MAPR={
            0b00000000:self.func7MAPaddsub,
            0b00000001:Instructions.sll,
            0b00000010:Instructions.slt,
            0b00000011:Instructions.sltu,
            0b00000100:Instructions.xor,
            0b00000101:self.func7MAPshft,
            0b00000110:Instructions.zor,
            0b00000111:Instructions.zand
        }
        self.func3MAPSYS={
            0b00000000:self.func7MAPecall,
            0b00000001:Instructions.csrrw,
            0b00000010:Instructions.csrrs,
            0b00000011:Instructions.csrrc,
            0b00000101:Instructions.csrwi,
            0b00000110:Instructions.csrrsi,
            0b00000111:Instructions.csrrci
        }
        self.opcodeMAP={
            0b00110111:Instructions.lui,
            0b00010111:Instructions.auipc,
            0b01101111:Instructions.jal,
            0b01100111:Instructions.jalr,
            0b01100011:self.func3MAPB,
            0b00100011:self.func3MAPS,
            0b00000011:self.func3MAPI1,
            0b00010011:self.func3MAPI2,
            0b00110011:self.func3MAPR,
            0b01110011:self.func3MAPSYS
        }

    def getInstructions(self,opcode:c_ubyte,func3:c_ubyte,func7:c_ubyte):
        inst=self.opcodeMAP[opcode.value]
        if type(inst) is Instructions:
            return inst
        elif type(inst) is dict:
            inst=inst[func3.value]
            if type(inst) is Instructions:
                return inst
            elif type(inst) is dict:
                inst=inst[func7.value]
                if type(inst) is Instructions:
                    return inst
                else:
                    print("Error: Unimplemented Instructions encountered3\n")
                    return Instructions.noimp
            else:
                print("Error: Unimplemented Instructions encountered2\n")
                return Instructions.noimp
        else:
            print("Error: Unimplemented Instructions encountered1\n")
            return Instructions.noimp


