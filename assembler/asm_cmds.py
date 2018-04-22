#Macro commands are effectivley macros programmed in python

class MacroCmdBase:
    def __init__(tokens, args):
        self.tokens = tokens
        self.args = args
