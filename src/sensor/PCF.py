#Read a value from analogue input 2 
#in A/D in the PCF8591P @ address 0x48
from smbus import SMBus
import time

bus = SMBus(1)

print("Read the A/D:")

def read_channel(sensor, channel):
	bus.write_byte(0x48, channel) # set control register to read channel
	reading = bus.read_byte(0x48) # read A/D
   	print "%s sensor | channel %s: %s"%(sensor, channel, reading)

def read_light():
	bus.write_byte(0x48, 1) # set control register to read channel 1
	reading = bus.read_byte(0x48) # read A/D
	return 1080 - float(reading)

while(1): # do forever
	read_channel("resistance", 0);
	read_channel("light", 1);
	read_channel("temprature", 2);
	read_channel("external", 3);
   	print "*"*40
	time.sleep(2)

