import readchar
import sys
class UART:
    def read(self,address):
        if(address&0x0000000f==0):
            try:
                c = readchar.readkey()
                print(c,end="",flush=True)
            except KeyboardInterrupt:
                sys.exit(0)
            else:
                return ord(c)
    def write(self,address,data,size):
        if(address&0x0000000f==0):
            print(chr(data),end="",flush=True)

def test_uart():
    uart=UART()
    while True:
        uart.write(0x40000000,uart.read(0x40000000),0)

if __name__ == "__main__":
    test_uart()