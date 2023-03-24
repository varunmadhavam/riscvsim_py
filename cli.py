from soc import Soc
import sys
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
import string
from memory import Memory

def check_address_valid(addr):
    if(len(addr)!=8):
        return False
    return set(addr).issubset(string.hexdigits)
def print_help():
    print("")
    print("q|x|exit|quit : Exit the Simulator")
    print("r|run : Run till a break point is hit")
    print("s|step : Single step")
    print("dumpreg : Dump all registers")
    print("dumpreg regno : Dump register regno where 0<=regno<32")
    print("dumpmem addr : Dump word in memory pointed by addr where addr in hex without 0x prefix. eg 00000008")
    print("dumpmem addr len: Dump len/2 words before and after the address pointed by addr from memory where addr in hex without 0x prefix. eg 00000008 and len is a decimal")
    print("set addr : Sets a breakpoint @ address addr where addr in hex without 0x prefix. eg 00000008")
    print("remove addr : Removes a breakpoint @ address addr where addr in hex without 0x prefix. eg 00000008")
    print("reset : Resets the CPU model")
    print("debug : Toggle debug mode")
    print("dumpbp : List all the current set break points")
    print("h|help : Prints this message")
    print("")
debug=False
n=len(sys.argv)
if n==1:
    bootfile="./sw/app/bootloader/firmware.bin"
    binfile="./sw/app/main_app/firmware/firmware.bin"
elif n==2:
    bootfile="./sw/test/firmware/firmware.bin"
    binfile=None
else:
    print("Usage : python3 soc.py [test] ")
soc=Soc(bootfile,binfile)
while 1:
    try:
        completer = WordCompleter(['exit', 'dumpreg', 'dumpmem', 'run', 'step', 'set', 'remove', 'reset', 'debug','dumpbp', 'help','quit'])
        user_input = prompt('> ',completer=completer,complete_while_typing=True)
        if (user_input=='x' or user_input=='q' or user_input=='exit' or user_input=='quit'):
            exit(0)
        elif(user_input=="h" or user_input=="help"):
            print_help()
        elif(user_input=="r" or user_input=="run"):
            soc.run(debug=debug,mode="r")
        elif(user_input=="s" or user_input=="step"):
            soc.run(debug=debug,mode="s")
        else:
            res=user_input.split()
            if(len(res)==1):
                if(res[0]=="dumpreg"):
                    soc.cpu.dump_regs()
                elif(res[0]=="reset"):
                    soc.cpu.reset()
                elif(res[0]=="dumpbp"):
                    soc.cpu.dump_bp()
                elif(res[0]=="debug"):
                    if(debug):
                        debug=False
                        print("debug disabled")
                    else:
                        debug=True
                        print("debug enabled")
            elif(len(res)==2):
                if(res[0]=="dumpreg"):
                    if(res[1].isnumeric() and (int(res[1])<32)):
                        print("X{}={}".format(int(res[1]),hex(soc.cpu.cpuregs[int(res[1])]&(2**32-1))))
                elif(res[0]=="dumpmem"):
                    if(check_address_valid(res[1])):
                        perip=soc.map.getperipheral(int(res[1],16))
                        if(type(perip)==Memory):
                            perip.dumpmem(int(res[1],16),0)
                elif(res[0]=="set"):
                    if(check_address_valid(res[1])):
                            soc.cpu.add_bp(int(res[1],16))
                elif(res[0]=="remove"):
                    if(check_address_valid(res[1])):
                            soc.cpu.rm_bp(int(res[1],16))
            elif(len(res)==3):
                if(res[0]=="dumpmem"):
                    if(check_address_valid(res[1])):
                        perip=soc.map.getperipheral(int(res[1],16))
                        if(type(perip)==Memory):
                            perip.dumpmem(int(res[1],16),int(res[2],10))

    except KeyboardInterrupt:
        print("")
        continue
    except EOFError:
        exit(0)



    
        