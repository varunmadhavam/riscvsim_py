#include"ttyuart.h"
#include<stdio.h>
#include<string.h>
int main() {
   __tty_uart_send_string("\r\n***Hello! World from RISC-V SIM***\n\n");
    while (1){
    }
    return 0;
}
