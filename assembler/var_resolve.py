'''
This is the last pass before the binary file is outputed.
VariableResolver does the following:
    1. create a command class for each cmd
    2. resolve mem variables to real addresses by asking each command if it defines a mem address, and based on each commands length
    3. lets each cmd emit its output to the binary file
       (for complex commands like subroutines, this coud contain recursive code evaluation)

ARGS:
cmds is list of Cmd
out is output file
'''

class VariableResolver:
    def __init__(self, cmds, out):
        self.cmds = cmds
        self.out = out

    
