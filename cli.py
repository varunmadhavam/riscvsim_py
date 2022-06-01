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
        completer = WordCompleter(['exit', 'dumpreg', 'dumpmem', 'run', 'step', 'set', 'remove', 'reset', 'debug'])
        user_input = prompt('> ',completer=completer,complete_while_typing=True)
        if (user_input=='x' or user_input=='exit'):
            exit(0)
        if(user_input=="r" or user_input=="run"):
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



    
        