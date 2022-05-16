#include"ttyuart.h"

char __tty_uart_receive_char(){
    return (char) TTYUART->DATA;
}

void __tty_uart_send_char(char c){
    TTYUART->DATA=c;
}

void __tty_uart_send_string(char *s){
    while (*s!=0){
        __tty_uart_send_char(*s);
        s++;
    }
}

void __tty_uart_receive_string(char *s){
    char c=0; 
    while(c!='\n'){
        c=__tty_uart_receive_char();
        *s=c;
        s++;
    }
    s--;
    *s=0;
}
