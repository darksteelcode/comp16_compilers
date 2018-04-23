#Macro commands are effectivley macros programmed in python
import assemble

class MacroCmdBase:
    #Args are a list of args the macro is called with, and types are the arg types
    def __init__(args, types):
        self.args = args
        self.types = types

    def checkArgs():
        #If an error occurs, print a message here
        return True

    #Return tokens to add in to the code
    def getResult():
        return []
        
