#include"ttyuart.h"
int main(void){
    __tty_uart_send_string("\rHello!World\n");
    while(1){
    }
	return 0;
}

