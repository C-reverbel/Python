from pyparsing import *
import pyparsing










testString = "LT3 1 0 10k 20M 0.1\n" \
             "G1 2 0 100k 200M 0.5"

type_arg = Or([Literal('G'), Literal('T'), Literal('LT'), Literal('M'),
               Literal('C'), Literal('Vb'), Literal('Sb')])
tempName_arg = Word(alphanums)
net1_arg = Word(alphanums)
net2_arg = Word(alphanums)
voltage_arg = Word(alphanums)

# called to check e=what kind of line we are initializing (component, comment, base, etc...)
type_decl = type_arg('type') + Optional(alphanums)
# called when current line declares a component
component_decl = name_arg('name') + net1_arg('net1') + net2_arg('net2')
# called when current line declares the base parameters
#base_decl =




a = type_decl.parseString(testString)
a.name =
a = component_decl.parseString(testString)
a.name = a.type + a.name

print a

def

class parser:
    def __init__(self):
        pass

    def parse(self, str):
        pass
