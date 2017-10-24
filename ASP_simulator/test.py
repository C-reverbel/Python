from Learning import *

circ1 = Circuit("Circ1.txt")

# for x in range(len(circ1.compList)):
#     print circ1.compList[x]

print circ1.getPathToNet('8')
