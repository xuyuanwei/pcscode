#ifndef _PCUARTCMD_H_
#define _PCUARTCMD_H_

#include <inttypes.h>

void ascii2hex(char *hexascii,uint8_t *hex);
void hex2ascii(uint8_t hex,char *hexascii);
int pcuartcmd_process(char *cmdstr,uint8_t strlen);

#endif
