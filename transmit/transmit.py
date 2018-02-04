import serial, sys, time, math
import serial.tools.list_ports
ser = serial.Serial()
ser.baudrate = 115200
hexFile = ""
if len(sys.argv) < 2:
    hexFile = raw_input("Hexedecimal Text file to open: ")
else:
    hexFile = sys.argv[1]
print "Hexedecimal Text File To Transmit: " + hexFile
num_lines = sum(1 for line in open(hexFile, 'r'))
f = open(hexFile, 'r')

print "Looking for FTDI Port"
foundOne = False
for p in serial.tools.list_ports.comports():
    if "ft232r" in p[1].lower():
        foundOne = True
        print "Found port " + str(p) + ".\nOpening to transmit"
        ser.port = p[0]
        ser.open()
        if ser.isOpen():
            print "Waiting For Device Signature"
            sigStart = time.time()
            sigCheck = True
            while ser.inWaiting() < 1:
                if time.time() - sigStart > 1.0:
                    print "No Signature Recived, Starting Anyway"
                    sigCheck = False
                    break
            if sigCheck:
                if ser.read(1) != '*':
                    print "Signature Recived - Bad Device Signature Found"
                    if raw_input("Send Anyway (y/n):") == 'n':
                        exit()
                else:
                    print "Signature Recived - Signature Good"
            ser.read(ser.inWaiting())
            print "Opened"
        else:
            print "Port Failed to open"
            exit()
if not foundOne:
    print "No Port Found"
    exit()
def sendHex(hex):
    confirm = ""
    for d in range(len(hex)):
        if d % 2 == 1:
            data = bytearray.fromhex(hex[d-1:d+1])
            ser.write(data)
            confirm += hex[d-1:d+1]
            time.sleep(0.0001)
    return confirm

def confirmHex(hex_to_confirm):
    global errors
    confirm_len = len(hex_to_confirm)/2
    while ser.inWaiting() < confirm_len:
        pass
    data = ser.read(ser.inWaiting()).encode('hex')
    good = data == hex_to_confirm
    if not good:
        errors += 1
        print "\n---------------------\nERROR\nBAD CONFIRMATION RECVIVED\n---------------------\n"
    return good
start = time.time()
hexData = f.read().replace("\n", "")
chunkLen = 128
chunkLen = chunkLen * 2
chunks = [hexData[i:i+chunkLen] for i in range(0, len(hexData), chunkLen)]
index = 0
cur = 0
num_chunks = len(chunks)
errors = 0
ser.read(ser.inWaiting())
print "Transmitting"
sys.stdout.write("|")
for i in range(78):
    sys.stdout.write("-")
sys.stdout.write("|")
sys.stdout.flush()

for c in chunks:
    conf = sendHex(c)
    confirmHex(conf)
    if int((float(index)/float(num_chunks))*80.0) >= cur:
        cur += 1
        sys.stdout.write("#")
        sys.stdout.flush()
    index+=1

sendHex("ffff")
ser.close()

print "Program Sent"
print "Time: " + str(time.time() - start)
print "Errors:"
print errors
