#!/usr/bin/python
import serial
import json
import syslog,time,sys

port = '/dev/ttyUSB0'
def main(port):
    ard = serial.Serial(port,9600,timeout=1)
    i = 0
    send =""
    time.sleep(1.5)
    while (i<5):
        send += 'Everything Ok~~'
        ard.flush()
        send = str(send)
        print ("Python value sent: ")
        print (send)
        ard.write(send)

        msg = ard.readline().strip('\n\r') #ard.read(ard.inWaiting()).strip('\n\r') 
        print ("Message from arduino: ")
        
        try:
            key = ['result','data']
            value = msg.split('-',2)
            data = dict(zip(key,value))
        except:
            print 'ERROR!'
        print msg

        print "*"*40
        time.sleep(1)
        i = i + 1
    else:
        print "Exiting"
    exit()

if __name__ == '__main__':
    try:
        main(sys.argv[1] if len(sys.argv) > 1 else port )
    except KeyboardInterrupt:
        ser.close()