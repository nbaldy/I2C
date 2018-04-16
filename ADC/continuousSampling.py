import smbus #required for communication with device 
bus = smbus.SMBus(1) #or SMBus(0) for raspberry pi 2 and earlier (?)
import time # 1 sps 

# Nicole Baldu
# University of Akron
# Created 04/15/18
# Purpose: To sample voltage levels once per second using the ads1015 Analog-to-Digital Converter

Address = 0x48 #I2C address of ads1015 with ADDR pin connected to gnd

def swap2Bytes(data): 
  #different Endians, so swap the 2 bytes of transmitted "data"
  	data = ((data & 0x00ff) << 8) + ((data|0x0000) >> 8)
	#	     LSB shifted forward 	        MSB shifted back
	return data
  
def configure():
	#Sets config register
	# Bit [15]:	1 - begin conversion
	# Bits [14:12]:	000 - Compare A0 and A1 
	# Bits [11:9]:	001 - range is (+) or (1) 4.096V    
	# Bit [8]:	0 - Continuous Conversion mode
	# Bits [7:5]	100 - 1600 SPS (default)
	# Bit [4]	0 - Traditional Comparator
	# Bit [3]	0 - Comparator Polarity Active Low (default - irrelevant?)
	# Bit [2	0 - Non-latching comparator (default - irrelevant?)
	# Bits [1:0]	00 - Assert after 1 conversion (?)
  
	configData = 0x8280
	bus.write_word_data(Address, 1, swap2Bytes(configData))
  
def read():
	#reads data from serial bus, note NOT SWAPPED, 16 bits, only first 12 relevant
	data = bus.read_word_data(Address, 0)
	return data

def toVolts(data): 
	#convert (NOTE: 12bit, so pre-shifted) data to Voltage  
	#Calculate 2's Complement
	data = (-1)*(data>>11)*(2**11) + (data&0x7FF)
	#	(-1) * msb *2^11       + the positive part 
	
	# 2mV per bit
	return (data*.002) 

configure()
while True: 
	currentData = swap2Bytes(read()) >> 4
	#swap and drop last 4 bits
	print(hex(currentData),toVolts(currentData))
	time.sleep(1) 
	#wait for a second
