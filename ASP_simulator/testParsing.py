# from pyparsing import *
# import pyparsing
#
#
# testString = "LT3 1 0 10k 20M 0.1\n" \
#              "G1 2 0 100k 200M 0.5"
#
# type_arg = Or([Literal('G'), Literal('T'), Literal('LT'), Literal('M'),
#                Literal('C'), Literal('Vb'), Literal('Sb')])
# name_arg = Word(alphanums)
# tempName_arg = Word(alphanums)
# net1_arg = Word(alphanums)
# net2_arg = Word(alphanums)
# voltage_arg = Word(alphanums)
#
# type_decl = type_arg('type') + name_arg('auxName')
#
#
# # called when current line declares a component
# component_decl = type_decl('name') + net1_arg('net1') + net2_arg('net2')
# # called when current line declares the base parameters
# #base_decl =
# #
# #
# # #a = type_decl.parseString(testString)
# # a = component_decl.parseString(testString)
# # a.name = a.type + a.auxName
# #
# # print a.name
# #
# # class parser:
# #     def __init__(self):
# #         pass
# #
# #     def parse(self, str):
# #         pass
# #
# # def InterfaceDict(expr, param):
# #     def createDict(tokens):
# #         d = ParseResults()
# #         i = 0
# #         for token in tokens:
# #             ikey = pyparsing._ustr(token[param])
# #
# #             dictvalue = token.copy()  # ParseResults(i)
# #             if len(dictvalue) != 1 or (isinstance(dictvalue, ParseResults) and dictvalue.haskeys()):
# #                 d[ikey] = pyparsing._ParseResultsWithOffset(dictvalue, i)
# #             else:
# #                 d[ikey] = pyparsing._ParseResultsWithOffset(dictvalue[0], i)
# #
# #             d.append(d[ikey])
# #
# #             i = i + 1
# #         return [d]
# #     return expr.setParseAction(lambda toks: createDict(toks))
#
#
# from pyparsing import *
# import pyparsing
#
#
#
#
# def templateParse(line):
#     lineSplit = line.split(" ")
#     templParser = Word(alphanums)(lineSplit[0])
#     del lineSplit[0]
#     for a in lineSplit:
#         templParser += Word(alphanums)(a)
#     return templParser
#
# def parse(line, parseTemplate):
#     type = typeParse(line) # get line type
#
#
#
# class test:
#     pass
#
# t1 = test()
#
# t1.name = "rthyeutty"
# t1.age = 350
#
# t2 = test()
# for attr, value in t1.__dict__.iteritems():
#     setattr(t2,attr,value)
# print t2.name, t2.age
#
# testString = "name net1 net2 V S X"
#
# parse_args = templateParse(testString)
# n = parse_args.parseString("G1 2 0 100k 200M 0.5")
#
# for key, value in n.iteritems():
#     print key, value
#



var = '0.1'

var = float(var)
print var






