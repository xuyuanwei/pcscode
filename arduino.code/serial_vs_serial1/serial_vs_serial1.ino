#include "Arduino.h"
void setup();
void loop();
void serialEvent();
void serialEvent1();
void printBaudList();

unsigned long outputBaud[]={57600,9600,115200,4800,38400,19200};
const uint8_t BaudCount=sizeof(outputBaud)/sizeof(unsigned long);
char outputBaudString[BaudCount][10]={"57600","9600","115200","4800","38400","19200"};

const int maxlength=256;
char serial1_buff[maxlength]={};
char serial2_buff[maxlength]={};
char serial_buff[maxlength]={};
uint8_t serial1_index=0;
uint8_t serial2_index=0;
uint8_t serial_index=0;
bool serial_full_flag=0;
bool serial1_full_flag=0;
bool serial2_full_flag=0;

char ascii[2];

void setup()
{
	Serial.begin(115200);  // start serial for output
	Serial1.begin(57600);  
	Serial2.begin(57600);  
	Serial.print("Serial1 and Serial2 to usb Serial\r\n");
}

void loop()
{
    uint8_t i=0;
    if(serial_full_flag==1)
    {
        for(i=0;i<=serial_index;i++) {
            Serial1.print(serial_buff[i]); 
            Serial2.print(serial_buff[i]); 
        }
        serial_index=0;
        serial_full_flag=0;
    }

    if(serial1_full_flag==1)
    {
        Serial.print("serial1:"); 
        for(i=0;i<=serial1_index;i++) {
            Serial.print(serial1_buff[i]); 
        }
        serial1_index=0;
        serial1_full_flag=0;
    }

    if(serial2_full_flag==1)
    {
        Serial.print("serial2:"); 
        for(i=0;i<=serial2_index;i++) {
            Serial.print(serial2_buff[i]); 
        }
        serial2_index=0;
        serial2_full_flag=0;
    }
}

void HexToAscii(uint8_t nHex,char *pAscii)
{
	uint8_t i = 0;

	pAscii[0] = nHex >> 4;
	pAscii[1] = nHex & 0x0F;

	for ( i = 0;i<2;i++ )
	{
		if ( pAscii[i] > 9 )
		{
			pAscii[i] += 'A' - 10;
		}
		else
		{
			pAscii[i] += '0';
		}
	}	
}

uint8_t AsciiToHex(char *pAscii)
{
    uint8_t nHex = 0;
    uint8_t i = 0;
    for ( i=0;i<2;i++ )
    {
        nHex = nHex << 4; 
        if ( ( pAscii[i] >= 'A' ) && ( pAscii[i] <= 'F' ) )
        {
            pAscii[i] = pAscii[i] - 'A' + 10;
        }
        else if ( ( pAscii[i] >= 'a' ) && ( pAscii[i] <= 'f' ) )
        {
            pAscii[i] = pAscii[i] - 'a' + 10;	
        }
        else if ( ( pAscii[i] >= '0' ) && ( pAscii[i] <= '9' ) )
        {
            pAscii[i] -= '0';	
        }
        else
        {
            pAscii[i] = 0;
        }

        nHex += pAscii[i]; 
    }

    return nHex;
}

void serialEvent() {
    while (Serial.available()) {
        if(serial_full_flag==1) //wait the buffer to be send
            break;
        if(serial_index==maxlength)
            serial_index=0;
        serial_buff[serial_index]=char(Serial.read());

        if((serial_index>=1) && (serial_buff[serial_index]=='\n') && (serial_buff[serial_index-1]=='\r'))
            serial_full_flag=1;
    }
}


void serialEvent1() {
    while (Serial1.available()) {
        if(serial1_full_flag==1) //wait the buffer to be send
            break;
        if(serial1_index==maxlength)
            serial1_index=0;
        serial1_buff[serial1_index]=char(Serial1.read());

        if((serial1_index>=1) && (serial1_buff[serial1_index]=='\n') && (serial1_buff[serial1_index-1]=='\r'))
            serial_full_flag=1;
    }
}


void serialEvent2() {
    while (Serial2.available()) {
        if(serial2_full_flag==2) //wait the buffer to be send
            break;
        if(serial2_index==maxlength)
            serial2_index=0;
        serial2_buff[serial2_index]=char(Serial2.read());

        if((serial2_index>=2) && (serial2_buff[serial2_index]=='\n') && (serial2_buff[serial2_index-2]=='\r'))
            serial_full_flag=2;
    }
}
