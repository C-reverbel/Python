from pyparsing import *

COLON = Literal(":").suppress()
COMMA = Literal(",").suppress()
EQUALS = Literal("=").suppress()
LPAREN = Literal("(").suppress()
RPAREN = Literal(")").suppress()
DECL = Literal("decl")
MSG = Literal("msg")

cmd_last_arg = restOfLine
cmd_arg = ZeroOrMore(Regex(r"[^,]+"))

parm_label = Regex(r"[^,()=]")
parm_value = Regex(r"[^,()=]")

parm_arg = parm_label + EQUALS + parm_value
parm_args = delimitedList(parm_arg, delim=',')
parms = LPAREN + parm_args + RPAREN

decl_cmd = Group(DECL + Optional(parms) + COLON + cmd_last_arg)
msg_cmd = Group(MSG + COLON + cmd_arg + COMMA + cmd_arg + COMMA + cmd_last_arg)
cmd = (decl_cmd | msg_cmd | pythonStyleComment)

content = raw_input("enter: ")
try:
    a = cmd.parseString(content)
except ParseException, pe:
    print pe
else:
    cmd_text = a[0][0]
    if cmd_text == "msg":
        src = a[0][1]
        dst = a[0][2]
        txt = a[0][3]
        print "message from ", src, " to ", dst, " with text = ", txt















# from Learning import *
#
# circ1 = Circuit("Circ1_P1_XXXX.txt")
#
# # for x in range(len(circ1.compList)):
# #     print circ1.compList[x]
#
# circ1.printPu()
#print circ1.getPathToNet('5'
