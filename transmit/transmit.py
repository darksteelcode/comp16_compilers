import serial, sys, time, math
import serial.tools.list_ports
import argparse
ser = serial.Serial()
ser.baudrate = 115200
ser.port = "FALSE"
binFile = ""

parser = argparse.ArgumentParser(usage="\n--------------------\n- Comp16 Prgm Send -\nUsage:\npython transmit.py [options] <bin file>\nOptions:\n-s serial_port  (default: searches for a port with an uart device on it)\n-b baudrate     (default: 115200)\n--------------------")
parser.add_argument("-s", nargs=1)
parser.add_argument("-b", nargs=1)
parser.add_argument("bin_file")
args = parser.parse_args()
print "- Comp16 Prgm Send -"
binFile = args.bin_file
if args.b:
    ser.baudrate = int(args.b)
if args.s:
    ser.port = args.s[0]

def print_usage():
	print "\n--------------------\n- Comp16 Prgm Send -\nUsage:\npython transmit.py [options] <bin file>\nOptions:\n-s serial_port  (default: searches for a port with an uart device on it)\n-b baudrate     (default: 115200)\n--------------------"
	exit()




print "Transmiting " + binFile + " to " + ser.port
num_lines = sum(1 for line in open(binFile, 'r'))
f = open(binFile, 'r')

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

def sendBin(bin_data):
    for d in bin_data:
            ser.write(d)
            time.sleep(0.0001)
    return bin_data

def confirmBin(bin_to_confirm):
    global errors
    confirm_len = len(bin_to_confirm)
    while ser.inWaiting() < confirm_len:
        pass
    data = ser.read(ser.inWaiting())
    good = data == bin_to_confirm
    if not good:
        errors += 1
        print "\n---------------------\nERROR\nBAD CONFIRMATION RECVIVED\n---------------------\n"
    return good

start = time.time()
binData = f.read().replace("\n", "")
chunkLen = 128
chunks = [binData[i:i+chunkLen] for i in range(0, len(binData), chunkLen)]
index = 0
cur = 0
num_chunks = len(chunks)
errors = 0
ser.read(ser.inWaiting())
print "Transmitting"
sys.stdout.write("|")
for i in range(78):
    sys.stdout.write("-")
sys.stdout.write("|\n")
sys.stdout.flush()

for c in chunks:
    conf = sendBin(c)
    confirmBin(conf)
    while int((float(index)/float(num_chunks))*80.0) >= cur:
        cur += 1
        sys.stdout.write("#")
        sys.stdout.flush()
    index+=1

sendBin("ffff")
print
ser.close()

print "Program Sent"
print "Time: " + str(time.time() - start)
print "Errors:"
print errors
