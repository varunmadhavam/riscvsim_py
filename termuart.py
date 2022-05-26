class UART:
    def read(self,address):
        if(address&0x0000000f==0):
            return str(input())
    def write(self,address,data,size):
        if(address&0x0000000f==0):
            print(chr(data),end="")

def test_uart():
    uart=UART()
    uart.write(0x40000000,uart.read(0x40000000),0)

if __name__ == "__main__":
    test_uart()