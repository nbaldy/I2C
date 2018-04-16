import smbus #allow use of SMbus Library

bus = smbus.SMBus(1) #Raspberry Pi 3 B only enables SMBus line  1

DAC_addr = 0x62 #address of MCP4725
write_DAC_only = 0x40 #command to write to DAC Register only

#get voltage from user
volts = input("Enter a Voltage between 0 and 3.3: ")

#convert voltage to data for DAC
data = int( volts * ((0xFFF) / 3.3)) 

#Reorder bytes
data = ((data % 0x10)* 0x1000) + (data // 0x10)

#actually write the input
bus.write_word_data(DAC_addr, write_DAC_only, data)



