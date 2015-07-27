import dhtreader

def read_temp_and_hum():
    dhtreader.init()
    temp_and_hum = dhtreader.read(11, 4)
    if temp_and_hum:
    	return temp_and_hum
    else:
    	print "[Error:] Failed to read from sensor, maybe try again?"