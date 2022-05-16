from memory import BRAM

bram=BRAM()
bram.init_mem("./sw/firmware/firmware.bin")
print(hex(bram.RAM[0x0>>2]))
print(hex(bram.RAM[0]))
print(hex(bram.RAM[0x4>>2]))
print(hex(bram.RAM[1]))
print(hex(bram.RAM[0x9C>>2]))
print(hex(bram.RAM[1]))