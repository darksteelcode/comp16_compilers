#!/usr/bin/python

import serial, sys, time
import serial.tools.list_ports
import argparse
ser = serial.Serial()
ser.baudrate = 115200
ser.port = "FALSE"

def print_usage():
    print "\n--------------------\n- Comp16 Prgm Send -\nUsage:\npython transmit.py [options] <bin file>\nOptions:\n-s serial_port  (default: searches for a port with an uart device on it)\n-c number of bytes per chunk  (default:128)\n--------------------"
    exit()


if ser.port == "FALSE":
	print "No Port Specified, Looking for Port with a UART on It"
for p in serial.tools.list_ports.comports():
    if "uart" in p[1].lower() and ser.port == "FALSE":
        print "Found port " + str(p) + ".\nOpening to transmit"
        ser.port = p[0]

if ser.port == "FALSE":
    print "No Port Specified, and no UART Port Found. Terminating"
    exit()
ser.open()
if ser.isOpen():
    ser.read(ser.inWaiting())
    print "Opened"
else:
    print "Port Failed to open"
    exit()

if len(sys.argv) != 2:
    print_usage()
path = sys.argv[1]
print "Transmiting " + path + " to " + ser.port

sys.stdout.write("|")
for i in range(78):
    sys.stdout.write("-")
sys.stdout.write("|\n")
sys.stdout.flush()

f = open(path, 'r')
data = f.read()
f.close()

def send(word):
	ser.write(word[0])
	time.sleep(0.0002)
	ser.write(word[1])
	time.sleep(0.0002)
	while ser.inWaiting() < 2:
		pass
	ser.read(2)

cur = 0
for i in range(len(data)):
    if i % 2 == 1:
        send(data[i-1] + data[i])
    while int((float(i)/float(len(data)))*80.0) >= cur:
        cur += 1
        sys.stdout.write("#")
        sys.stdout.flush()

send(chr(255)+chr(255))
sys.stdout.write("\n")
sys.stdout.flush()
print "Sent"
