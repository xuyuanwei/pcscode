CC=avr-g++
GCC=avr-gcc
AR=avr-ar
OBJCOPY=avr-objcopy
CPPFLAGS=-c -g -Os -Wall -fno-exceptions -ffunction-sections -fdata-sections -mmcu=atmega2560 -DF_CPU=16000000L -MMD -DUSB_VID=null -DUSB_PID=null -DARDUINO=101 
INCULDE=-I/usr/share/arduino/hardware/arduino/cores/arduino
INCULDE +=-I/usr/share/arduino/hardware/arduino/variants/mega 

COMMON_CPP_FLAGS=-c -g -Os -Wall -ffunction-sections -fdata-sections -mmcu=atmega2560 -DF_CPU=16000000L -MMD -DUSB_VID=null -DUSB_PID=null -DARDUINO=101  

COMMON_OBJ_OUTPUT_DIR=/home/cylinc/Code/arduino/project/common
COMMON_SRC_DIR=/usr/share/arduino/hardware/arduino/cores/arduino/

SOURCE_FILE_NAME=serial_vs_serial1.cpp

target = wiring_analog.c.o
target += wiring_digital.c.o
target += WInterrupts.c.o
target += wiring_pulse.c.o
target += wiring.c.o
target += wiring_shift.c.o
target += HID.cpp.o
target += HardwareSerial.cpp.o
target += new.cpp.o
target += IPAddress.cpp.o
target += main.cpp.o
target += USBCore.cpp.o
target += Stream.cpp.o
target += WString.cpp.o
target += Print.cpp.o
target += Tone.cpp.o
target += WMath.cpp.o
target += CDC.cpp.o

default: core.a $(SOURCE_FILE_NAME).o
	$(GCC) -Os -Wl,--gc-sections,--relax -mmcu=atmega2560 -o $(SOURCE_FILE_NAME).elf $(SOURCE_FILE_NAME).o $(COMMON_OBJ_OUTPUT_DIR)/core.a -L$(COMMON_OBJ_OUTPUT_DIR) -lm
	$(OBJCOPY) -O ihex -j .eeprom --set-section-flags=.eeprom=alloc,load --no-change-warnings --change-section-lma .eeprom=0 $(SOURCE_FILE_NAME).elf $(SOURCE_FILE_NAME).eep 
	$(OBJCOPY) -O ihex -R .eeprom $(SOURCE_FILE_NAME).elf $(SOURCE_FILE_NAME).hex 

$(filter %.c.o,%(target)): %.c.o : $(COMMON_SRC_DIR)/%.c
	$(GCC) $(COMMON_CPP_FLAGS) $(INCULDE) $< -o $(COMMON_OBJ_OUTPUT_DIR)/$@

$(filter %.cpp.o,%(target)): %.cpp.o : $(COMMON_SRC_DIR)/%.cpp
	$(GCC) $(COMMON_CPP_FLAGS) $(INCULDE) $< -o $(COMMON_OBJ_OUTPUT_DIR)/$@


$(SOURCE_FILE_NAME).o: $(SOURCE_FILE_NAME)
	$(CC) $(CPPFLAGS) $(INCULDE) $(SOURCE_FILE_NAME) -o $(SOURCE_FILE_NAME).o

core.a: $(addprefix $(COMMON_OBJ_OUTPUT_DIR)/,$(target))
	$(AR) rcs $(COMMON_OBJ_OUTPUT_DIR)/core.a $(addprefix $(COMMON_OBJ_OUTPUT_DIR)/,$(target))


clean:
	rm ./*.o
