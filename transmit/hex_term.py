import serial
ser = serial.Serial('/dev/ttyUSB0', baudrate=115200)
def sendHex(hex):
    for d in range(len(hex)):
        if d % 2 == 1:
            if ser.inWaiting() > 0:
                print ":" + ser.read(ser.inWaiting()).encode('hex')
            data = bytearray.fromhex(hex[d-1:d+1])
            ser.write(data)
	    if ser.inWaiting() > 0:
                print ":" + ser.read(ser.inWaiting()).encode('hex')

while True:
	a = raw_input(">")
	sendHex(a)	
