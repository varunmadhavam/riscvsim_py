#ifndef TTYUART_IO
#define TTYUART_IO
    #include<stdint.h>

    #define TTYUART_BASE    0x40000000
    typedef struct {
        volatile uint32_t DATA;
    } ttyuart_type;
    #define TTYUART  ((ttyuart_type*)TTYUART_BASE)
    char __tty_uart_receive_char();
    void __tty_uart_send_char(char c);
    void __tty_uart_send_string(char *s);
    void __tty_uart_receive_string(char *s);
#endif
