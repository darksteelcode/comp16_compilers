def error(err, context):
    print "- Comp16 Assembler - \nError:\n" + str(err) + "\nAt:\n\n" + str(context) + "\n"
    exit()

def nonASMError(err):
    print "- Comp16 Assembler - \nError:\n" + str(err)
    exit()
