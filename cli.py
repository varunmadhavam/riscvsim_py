from soc import Soc
import sys
import signal
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter

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
try:
    while 1:
        completer = WordCompleter(['exit', 'dumpreg', 'dumpmem', 'run', 'step', 'set', 'remove'])
        user_input = prompt('> ',completer=completer)
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
            elif(len(res)==2):
                if(res[0]=="dumpreg"):
                    if(res[1].isnumeric() and (int(res[1])<32)):
                        print("X{}={}".format(int(res[1]),soc.cpu.cpuregs[int(res[1])]))
                elif(res[0]=="dumpmem"):
                    soc.ram.dumpmem(res[1],0)
            elif(len(res)==3):
                if(res[0]=="dumpmem"):
                    soc.ram.dumpmem(res[1],res[2])
except KeyboardInterrupt:
    soc.setkeep(False)



    
        