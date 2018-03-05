import sys
if len(sys.argv) < 3:
    print "Arguments: binfile.bin hexfile.txt"
    exit()

binFile = open(sys.argv[1])
hexFile = open(sys.argv[2], 'w')

data = binFile.read()
if len(data) % 2 != 0:
    print "Error: Bin file length not divisible by two"
    exit()

i = 0
for d in data:
    if i % 2 == 1:
        hexFile.write(hex(ord(d) + (ord(data[i-1])<<8))[2:].zfill(4))
        hexFile.write("\n")
    i+=1
hexFile.close()
