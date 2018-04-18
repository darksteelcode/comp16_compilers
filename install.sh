#!/bin/bash
chmod +x assembler/c16asm.py
ln -sf `pwd`/assembler/c16asm.py /usr/local/bin/c16asm
chmod +x transmit/c16send.py
ln -sf `pwd`/transmit/c16send.py /usr/local/bin/c16send
chmod +x binToMif/c16binToMif.py
ln -sf `pwd`/binToMif/c16binToMif.py /usr/local/bin/c16binToMif
mkdir -p /usr/c16-include
