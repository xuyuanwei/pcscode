#ifndef _TAS5717_H_
#define _TAS5717_H_

#include <inttypes.h>

uint8_t twst;
int TAS5717_write_bytes(uint8_t subaddr, uint8_t len, uint8_t *buf);
int TAS5717_read_bytes(uint8_t subaddr, uint8_t len, uint8_t *buf);
#endif
