/*
 * Simple demo program that to test the basic serial function using the avr-libc
 *
 */

#include <inttypes.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include <avr/interrupt.h>
#include <avr/io.h>
#include <avr/iom2560.h>
#include "tas5717_twi.h"
#include "pcuartcmd.h"




/*
 * System clock in Hz.
 */
#define F_CPU 16000000UL	/* Note [2] */
#define BAUD 57600UL
#define F_TWISCL 100000UL
#include <util/setbaud.h>


#define RX_BUFFER_SIZE 10
#define RX_BUFFER_LENGTH 20
char uart0_rx_buffer[RX_BUFFER_SIZE][RX_BUFFER_LENGTH];
uint8_t uart0_rx_buffer_index_x=0;
uint8_t uart0_rx_buffer_index_y=0;
uint8_t uart0_rx_buffer_index_x_pre=0;
uint8_t udr0_data=0;

/*
 * Do all the startup-time peripheral initializations: UART (for our
 * debug/test output), and TWI clock.
 */
void ioinit(void)
{
    uint16_t ubrr;
    /* usart0 initial */
    ubrr = (F_CPU / (16 * BAUD)) - 1; /* Bd */
    UBRR0H = (unsigned char)(ubrr>>8);
    UBRR0L = (unsigned char)ubrr;
    UCSR0B = (1<<RXEN0)|(1<<TXEN0);
    UCSR0C = (1<<USBS0)|(3<<UCSZ00); 
    UCSR0B |=(1<<RXCIE0);

    /* twi initial */
    /* initialize TWI clock: 100 kHz clock, TWPS = 0 => prescaler = 1 */
#if defined(TWPS0)
    /* has prescaler (mega128 & newer) */
    TWSR = 0;
#endif

#if F_CPU < 3600000UL
    TWBR = 10;			/* smallest TWBR value, see note [5] */
#else
    TWBR = (F_CPU / F_TWISCL - 16) / 2;
#endif

}

/*
 * Note [6]
 * Send character c down the UART Tx, wait until tx holding register
 * is empty.
 */
int uart0_putchar(char c, FILE *unused)
{
    if (c == '\n')
        uart0_putchar('\r', 0);
    loop_until_bit_is_set(UCSR0A, UDRE0);
    UDR0 = c;
    return 0;
}


FILE mystdout = FDEV_SETUP_STREAM(uart0_putchar, NULL, _FDEV_SETUP_WRITE);

int uart0_putch(char c)
{
    loop_until_bit_is_set(UCSR0A, UDRE0);
    UDR0 = c;
    return 0;
}

int uart0_putstr(char *c,uint8_t strlength)
{
    uint8_t i;
    for(i=0;i<strlength;i++)
        uart0_putch(c[i]);
    return 0;
}


/**
 * \brief Data RX interrupt handler
 *
 * This is the handler for UART receive data
 */
ISR(USART0_RX_vect)
{
    if(UDR0 == '\n')
    {
        uart0_rx_buffer[uart0_rx_buffer_index_x][uart0_rx_buffer_index_y]='\0';
        if(uart0_rx_buffer[uart0_rx_buffer_index_x][uart0_rx_buffer_index_y-1]
                =='\r')
            uart0_rx_buffer[uart0_rx_buffer_index_x][uart0_rx_buffer_index_y-1]
                ='\0';
        uart0_rx_buffer_index_x++;
    }
    uart0_rx_buffer_index_y++;
    if(uart0_rx_buffer_index_y == RX_BUFFER_LENGTH)
        uart0_rx_buffer_index_y = 0;
    if(uart0_rx_buffer_index_x == RX_BUFFER_SIZE)
        uart0_rx_buffer_index_x = 0;
}


int main(void)
{
    uint8_t i;

    ioinit();
    sei();

    //printf("started\n");
    uart0_putstr("started\n",8);

    udr0_data=1;

    while(1)
    {
        if(uart0_rx_buffer_index_x_pre!=uart0_rx_buffer_index_x)
        {
            pcuartcmd_process(uart0_rx_buffer[uart0_rx_buffer_index_x_pre],
                    strlen(uart0_rx_buffer[uart0_rx_buffer_index_x_pre]));
            uart0_rx_buffer_index_x_pre++;
            if(uart0_rx_buffer_index_x_pre == RX_BUFFER_SIZE)
                uart0_rx_buffer_index_x_pre = 0;
        }
    }

    return 0;

}
