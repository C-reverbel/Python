import os
from ASP_Classes import *


def line2class(character):
    switcher = {
        '*': 0,
        'G': 1,
        'T': 2,
        'LT': 3,
        'Vb': 4,
        'Sb': 5,
    }
    return switcher.get(character,0)

def initCircuit(lineSplit):
    global circ1

    if lineSplit[0][0] == 'G':  # init new generator
        tempGen = Generator(lineSplit)
        circ1.generators.append(tempGen)
    elif lineSplit[0][0] == 'T':
        tempTrans = Transformer(lineSplit)
        circ1.transformers.append(tempTrans)
    elif lineSplit[0][0] == 'L':
        if lineSplit[0][1] == 'T':
            tempLine = TransmissionLine(lineSplit)
            circ1.transmissionLines.append(tempLine)
    elif lineSplit[0][0] == 'C':
        pass

def main():
    global circ1

    with open("Circ1.txt") as f:
        lines = f.readlines()
    for line in lines:
        lineSplit = line.split(" ")
        initCircuit(lineSplit)


if __name__ == "__main__":
    circ1 = Circuit("Circ1.txt")
    main()


