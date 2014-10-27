
#include "tas5717_twi.h"
#include "pcuartcmd.h"
#include "main.h"

void ascii2hex(char *hexascii,uint8_t *hex)
{
    uint8_t temp=0;
    uint8_t i=0;
    for(i=0;i<2;i++)
    {
        temp=temp<<4;
        if(hexascii[i]>='0' && hexascii[i]<='9')
            temp += hexascii[i]-'0';
        else if(hexascii[i]>='A' && hexascii[i]<='F')
            temp += 10+hexascii[i]-'A';
        else if(hexascii[i]>='a' && hexascii[i]<='f')
            temp += 10+hexascii[i]-'a';
        else
            temp += 0;
    }

    *hex=temp;
    return;
}

void hex2ascii(uint8_t hex,char *hexascii)
{
    uint8_t i;
    hexascii[0]=hex >> 4;
    hexascii[1]=hex & 0x0F;
    for(i=0;i<2;i++)
    {
        if(hexascii[i]>9)
            hexascii[i] = hexascii[i]-10 + 'A';
        else
            hexascii[i] = hexascii[i] + '0';
    }
}

int pcuartcmd_process(char *cmdstr,uint8_t strlength)
{
    uint8_t register_addr;
    uint8_t valueCount=0;
    uint8_t i;
    #define VALARRAYSIZE 4
    uint8_t valueArray[VALARRAYSIZE]={};
    int result=0;
    switch(cmdstr[0])
    {
            /* cmd: W registeraddr Val1 Val2 ... Val4
             * W2601020304
             */
        case 'W':
            if( strlength <=1 || ((strlength-1)%2) != 0 )
                return -1;
            valueCount=(strlength-3)/2;
            if(valueCount>VALARRAYSIZE)
                return -2;
            ascii2hex(&cmdstr[1],&register_addr);
            for(i=0;i<valueCount;i++)
                ascii2hex(&cmdstr[3+2*i],&valueArray[i]);

            result= TAS5717_write_bytes(register_addr,valueCount,valueArray);
            result= TAS5717_read_bytes(register_addr,valueCount,valueArray);
            uart0_putstr("write result:",13);
            for(i=0;i<valueCount;i++)
            {
                hex2ascii(valueArray[i],&cmdstr[0]);
                uart0_putstr(cmdstr,2);
                uart0_putstr(" ",1);
            }
            uart0_putstr("\r\n",2);

            break;
            /* cmd: R registeraddr readcount(max=4)
             * R0104
             */
        case 'R':
            if( strlength <=1 || ((strlength-1)%2) != 0 )
                return -1;
            ascii2hex(&cmdstr[1],&register_addr);
            ascii2hex(&cmdstr[3],&valueCount);
            if(valueCount>VALARRAYSIZE)
                valueCount=VALARRAYSIZE;

            result= TAS5717_read_bytes(register_addr,valueCount,valueArray);
            uart0_putstr("read result:",12);
            for(i=0;i<valueCount;i++)
            {
                hex2ascii(valueArray[i],&cmdstr[0]);
                uart0_putstr(cmdstr,2);
                uart0_putstr(" ",1);
            }
            uart0_putstr("\r\n",2);
            break;

        default:
            return -2;
    }
    return 0;
}
