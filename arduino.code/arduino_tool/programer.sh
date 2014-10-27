#!/bin/sh

ArduinoDevice=/dev/ttyACM0
HexFileName=./serialtest.hex

avrdude -C/usr/share/arduino/hardware/tools/avrdude.conf -v -v -v -v -patmega2560 -cstk500v2 -P${ArduinoDevice} -b115200 -D -Uflash:w:${HexFileName}:i
