#include"ttyuart.h"
#include<string.h>
#include<stdlib.h>
#include<stdio.h>

int main() {
    char tmp[100];
    int a;
    int b;
    int res;
   __tty_uart_send_string("\r\n***Hello! World from RISC-V Calculator**\n\n");
    while (1){
        __tty_uart_send_string("\r\nEnter the first number: ");
        __tty_uart_receive_string(tmp);
        a=atoi(tmp);
        __tty_uart_send_string("\r\nEnter the second number: ");
        __tty_uart_receive_string(tmp);
        b=atoi(tmp);
        res=a+b;
        __tty_uart_send_string("\r\na + b = ");
        sprintf(tmp,"%d",res);
        __tty_uart_send_string(tmp);
    }
    return 0;
}
