#Read a value from analogue input 2 
#in A/D in the PCF8591P @ address 0x48
from smbus import SMBus
bus = SMBus(1)

def read_light():
	bus.write_byte(0x48, 1) # set control register to read channel 1
	reading = bus.read_byte(0x48) # read A/D
	return float(reading)

print read_light()