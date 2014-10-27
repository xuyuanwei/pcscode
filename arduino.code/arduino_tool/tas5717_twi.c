#include <util/twi.h>
#include <avr/io.h>
#include <avr/iom2560.h>
#include "tas5717_twi.h"

#define TAS5717ADDR 0x56
#define MAX_ITER	200

/* return the bytes write */
/* TODO: warning, there is no precaution in function
 * 0x00 ~ 0x1F: surport single byte or mutiple bytes read/write
 * 0x20 ~ 0xFF: surport only mutiple bytes read/write
 */
int TAS5717_write_bytes(uint8_t subaddr, uint8_t len, uint8_t *buf)
{
    uint8_t sla, n = 0;
    int rv = 0;

    sla = TAS5717ADDR << 1;

restart:
    if (n++ >= MAX_ITER)
        return -2;
begin:
    TWCR = _BV(TWINT) | _BV(TWSTA) | _BV(TWEN); /* send start condition */
    while ((TWCR & _BV(TWINT)) == 0) ; /* wait for transmission */
    switch ((twst = TW_STATUS))
    {
        case TW_REP_START:		/* OK, but should not happen */
        case TW_START:
            break;

        case TW_MT_ARB_LOST:
            goto begin;

        default:
            return -3;		/* error: not in start condition */
            /* NB: do /not/ send stop condition */
    }

    /* send SLA+W */
    TWDR = sla | TW_WRITE;
    TWCR = _BV(TWINT) | _BV(TWEN); /* clear interrupt to start transmission */
    while ((TWCR & _BV(TWINT)) == 0) ; /* wait for transmission */
    switch ((twst = TW_STATUS))
    {
        case TW_MT_SLA_ACK:
            break;

        case TW_MT_SLA_NACK:	/* nack during select: device busy writing */
            goto restart;

        case TW_MT_ARB_LOST:	/* re-arbitrate */
            goto begin;

        default:
            goto error;		/* must send stop condition */
    }

    TWDR = subaddr;		/* low 8 bits of addr */
    TWCR = _BV(TWINT) | _BV(TWEN); /* clear interrupt to start transmission */
    while ((TWCR & _BV(TWINT)) == 0) ; /* wait for transmission */
    switch ((twst = TW_STATUS))
    {
        case TW_MT_DATA_ACK:
            break;

        case TW_MT_DATA_NACK:
            goto quit;

        case TW_MT_ARB_LOST:
            goto begin;

        default:
            goto error;		/* must send stop condition */
    }

    for (; len > 0; len--)
    {
        TWDR = *buf++;
        TWCR = _BV(TWINT) | _BV(TWEN); /* start transmission */
        while ((TWCR & _BV(TWINT)) == 0) ; /* wait for transmission */
        switch ((twst = TW_STATUS))
        {
            case TW_MT_DATA_NACK:
                goto error;		/* device write protected -- Note [16] */

            case TW_MT_DATA_ACK:
                rv++;
                break;

            default:
                goto error;
        }
    }
quit:
    TWCR = _BV(TWINT) | _BV(TWSTO) | _BV(TWEN); /* send stop condition */

    return rv;

error:
    rv = -4;
    goto quit;
}

int TAS5717_read_bytes(uint8_t subaddr, uint8_t len, uint8_t *buf)
{
    uint8_t sla, twcr, n = 0;
    int rv = 0;

    sla = TAS5717ADDR << 1;

    /*
     * Note [8]
     * First cycle: master transmitter mode
     */
restart:
    if (n++ >= MAX_ITER)
        return -1;
begin:

    TWCR = _BV(TWINT) | _BV(TWSTA) | _BV(TWEN); /* send start condition */
    while ((TWCR & _BV(TWINT)) == 0) ; /* wait for transmission */
    switch ((twst = TW_STATUS))
    {
        case TW_REP_START:		/* OK, but should not happen */
        case TW_START:
            break;

        case TW_MT_ARB_LOST:	/* Note [9] */
            goto begin;

        default:
            return -1;		/* error: not in start condition */
            /* NB: do /not/ send stop condition */
    }

    /* Note [10] */
    /* send SLA+W */
    TWDR = sla | TW_WRITE;
    TWCR = _BV(TWINT) | _BV(TWEN); /* clear interrupt to start transmission */
    while ((TWCR & _BV(TWINT)) == 0) ; /* wait for transmission */
    switch ((twst = TW_STATUS))
    {
        case TW_MT_SLA_ACK:
            break;

        case TW_MT_SLA_NACK:	/* nack during select: device busy writing */
            /* Note [11] */
            goto restart;

        case TW_MT_ARB_LOST:	/* re-arbitrate */
            goto begin;

        default:
            goto error;		/* must send stop condition */
    }

    TWDR = subaddr;		/* low 8 bits of addr */
    TWCR = _BV(TWINT) | _BV(TWEN); /* clear interrupt to start transmission */
    while ((TWCR & _BV(TWINT)) == 0) ; /* wait for transmission */
    switch ((twst = TW_STATUS))
    {
        case TW_MT_DATA_ACK:
            break;

        case TW_MT_DATA_NACK:
            goto quit;

        case TW_MT_ARB_LOST:
            goto begin;

        default:
            goto error;		/* must send stop condition */
    }

    /*
     * Note [12]
     * Next cycle(s): master receiver mode
     */
    TWCR = _BV(TWINT) | _BV(TWSTA) | _BV(TWEN); /* send (rep.) start condition */
    while ((TWCR & _BV(TWINT)) == 0) ; /* wait for transmission */
    switch ((twst = TW_STATUS))
    {
        case TW_START:		/* OK, but should not happen */
        case TW_REP_START:
            break;

        case TW_MT_ARB_LOST:
            goto begin;

        default:
            goto error;
    }

    /* send SLA+R */
    TWDR = sla | TW_READ;
    TWCR = _BV(TWINT) | _BV(TWEN); /* clear interrupt to start transmission */
    while ((TWCR & _BV(TWINT)) == 0) ; /* wait for transmission */
    switch ((twst = TW_STATUS))
    {
        case TW_MR_SLA_ACK:
            break;

        case TW_MR_SLA_NACK:
            goto quit;

        case TW_MR_ARB_LOST:
            goto begin;

        default:
            goto error;
    }

    for (twcr = _BV(TWINT) | _BV(TWEN) | _BV(TWEA) /* Note [13] */;
            len > 0;
            len--)
    {
        if (len == 1)
            twcr = _BV(TWINT) | _BV(TWEN); /* send NAK this time */
        TWCR = twcr;		/* clear int to start transmission */
        while ((TWCR & _BV(TWINT)) == 0) ; /* wait for transmission */
        switch ((twst = TW_STATUS))
        {
            case TW_MR_DATA_NACK:
                len = 0;		/* force end of loop */
                /* FALLTHROUGH */
            case TW_MR_DATA_ACK:
                *buf++ = TWDR;
                rv++;
                if(twst == TW_MR_DATA_NACK) goto quit;
                break;

            default:
                goto error;
        }
    }
quit:
    /* Note [14] */
    TWCR = _BV(TWINT) | _BV(TWSTO) | _BV(TWEN); /* send stop condition */

    return rv;

error:
    rv = -1;
    goto quit;
}
