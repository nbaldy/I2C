import smbus #allow use of SMbus Library import time #allows pauses to make more managable 
bus = smbus.SMBus(1) #Raspberry Pi 3 B only enables SMBus 1
import time 
DAC_addr = 0x62 #address of MCP4725
write_DAC_only = 0x40 #command to write to DAC Register only


def writeVolts(volts): #sends data to DAC to output given voltage
	#convert voltage to data for DAC
	data = int( volts * ((0xFFF) / 3.3))

	#Reorder bytes
	firstByte = (0x00F & data) << 12
	secondByte = (data >> 4)
	data = firstByte+secondByte

	#actually write the input
	bus.write_word_data(DAC_addr, write_DAC_only, data)


def approxCos(theta): #approximates the cosine value using the taylor series for cos(x)
	return (1 - (1/2*theta**2) + (1/24*theta**4) - (1/720*theta**6));

period = 1.0/input("Frequency (Hz): ")
incrementTime = period / 628 #number of increments
A = input("Max voltage: ")/2
while(True):
	x = -3.14
	while(x < 3.14):
		writeVolts(A*approxCos(x) - 1/2*A)
		time.sleep(incrementTime)
		x+=.01;
