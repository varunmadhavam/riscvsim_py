class UART:
    def read(address):
        if(address&0x0000000f==0):
            return input()
    def write(address,data,size):
        if(address&0x0000000f==1):
            print(data,end="")