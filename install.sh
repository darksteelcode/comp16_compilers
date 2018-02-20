#!/bin/bash
python assembler/c16asm.py
chmod +x assembler/c16asm.py
sudo ln -sf `pwd`/assembler/c16asm.py /usr/local/bin/c16asm
python transmit/c16send.py
chmod +x transmit/c16send.py
sudo ln -sf `pwd`/transmit/c16send.py /usr/local/bin/c16send
