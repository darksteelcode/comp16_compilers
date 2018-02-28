#!/bin/bash
chmod +x assembler/c16asm.py
ln -sf `pwd`/assembler/c16asm.py /usr/bin/c16asm
chmod +x transmit/c16send.py
ln -sf `pwd`/transmit/c16send.py /usr/bin/c16send
