from pyparsing import *
import pyparsing
import math

class Component:
    name = ""
    type = ""
    net1 = ""
    net2 = ""
    Vmul = 1
    X_pu = 0
    V_pu = 0
    lineTemplate = ""

    def __init__(self, line):
        lineParsed = self.parseComponent(line, self.lineTemplate)
        for attr, value in lineParsed.iteritems():
            setattr(self, attr, value)
        # change required attributes to float
        self.conv2float()
    def __str__(self):
        return str(self.__dict__)
    # convert custom string to float
    def str2float(self, number):
        nb = number.lower()
        if nb.find('k') >= 0:
            return 1e3 * float(nb.replace('k', '.'))
        elif nb.find('m') >= 0:
            return 1e6 * float(nb.replace('m', '.'))
        else:
            return float(nb)
    # init pu variables
    def initPu(self, Vb, Sb):
        #print 'clacPU: ' + self.name + ' Vb = ' + str(Vb) + ' Sb = ' + str(Sb)
        if hasattr(self, 'X'):
            if hasattr(self, 'V'):
                self.X_pu = self.X * ((self.V**2)/self.S) / ((Vb**2)/Sb)
            elif hasattr(self, 'VPri'):
                self.X_pu = self.X * ((self.VPri ** 2) / self.S) / ((Vb ** 2) / Sb)
        else:
            # completar isso =========================================
            self.X_pu = self.L / ((Vb**2)/Sb)
        if hasattr(self, 'V'):
            self.V_pu = self.V / Vb
    # returns an object with all parameters initialized
    def parseComponent(self, line, parseTemplate):
        # parse definitions
        point = Literal('.')
        e = CaselessLiteral('E')
        plusorminus = Literal('+') | Literal('-')
        number = Word(nums)
        integer = Combine(Optional(plusorminus) + number)
        floatnumber = Combine(integer +
                              Optional(point + Optional(number)) +
                              Optional(alphanums)
                              )
        token = Or([Word(alphanums),floatnumber])
        # parse definitions

        lineSplit = parseTemplate.split(" ")
        templParser = token(lineSplit[0])
        del lineSplit[0]
        for a in lineSplit:
            templParser += token(a)
        n = templParser.parseString(line)
        return n
    # change required attributes to float
    def conv2float(self):
        for attr, val in self.__dict__.iteritems():
            if attr in self.floatElements:
                setattr(self,attr,self.str2float(val))

class Generator(Component):
    lineTemplate = "name net1 net2 V S X"
    floatElements = ['V', 'S', 'X']
    def __init__(self, line):
        self.type = 'G'
        Component.__init__(self, line)
    def initPu(self, Vb, Sb):
        self.X_pu = self.X * ((self.V ** 2) / self.S) / ((Vb ** 2) / Sb)
        self.V_pu = self.V / Vb
class Transformer(Component):
    lineTemplate = "name net1 net2 VPri VSec S X"
    floatElements = ['VPri', 'VSec', 'S', 'X']
    def __init__(self, line):
        self.type = 'T'
        Component.__init__(self, line)
        self.Vmul = self.VSec / self.VPri
    def initPu(self, Vb, Sb):
        self.X_pu = self.X * ((self.VPri ** 2) / self.S) / ((Vb ** 2) / Sb)
class TransmissionLine(Component):
    lineTemplate = "name net1 net2 R L"
    floatElements = ['R', 'L']
    def __init__(self, line):
        self.type = 'LT'
        Component.__init__(self, line)
    def initPu(self, Vb, Sb):
        Zb = (Vb ** 2) / Sb
        self.R_pu = self.R / Zb
        self.X_pu = self.L / Zb
class Motor(Component):
    lineTemplate = "name net1 net2 V S X"
    floatElements = ['V', 'S', 'X']
    def __init__(self, line):
        self.type = 'M'
        Component.__init__(self, line)
    def initPu(self, Vb, Sb):
        self.X_pu = self.X * ((self.V ** 2) / self.S) / ((Vb ** 2) / Sb)
        self.V_pu = self.V / Vb
class Load(Component):
    lineTemplate = "name net1 net2 V P Q"
    floatElements = ['V', 'P', 'Q']
    def __init__(self, line):
        self.type = 'C'
        Component.__init__(self, line)
    def initPu(self, Vb, Sb):
        Zb = (Vb ** 2) / Sb
        S = math.sqrt(self.P ** 2 + self.Q ** 2)
        self.R_pu = self.P * (self.V ** 2) / (S * S * Zb)
        self.X_pu = self.Q * (self.V ** 2) / (S * S * Zb)

class Circuit:

    # list of methods to initialize new components
    def addGenerator(self, paramList):
        tempGen = Generator(paramList)
        self.compList.append(tempGen)
    def addTransformer(self, paramList):
        tempTrafo = Transformer(paramList)
        self.compList.append(tempTrafo)
    def addTransmissionLine(self, paramList):
        tempTL = TransmissionLine(paramList)
        self.compList.append(tempTL)
    def addMotor(self, paramList):
        tempMotor = Motor(paramList)
        self.compList.append(tempMotor)
    def addLoad(self, paramList):
        tempLoad = Load(paramList)
        self.compList.append(tempLoad)
    def addVbase(self, paramList):
        parameters = paramList.split(" ")
        self.base['V'] = self.str2float(parameters[1])
        self.base['net'] = parameters[2]
    def addSbase(self, paramList):
        parameters = paramList.split(" ")
        self.base['S'] = self.str2float(parameters[1])
    componentsInitDict = {
        'G': addGenerator,
        'T': addTransformer,
        'LT': addTransmissionLine,
        'M': addMotor,
        'C': addLoad,
        'L': addLoad,
        'Vb': addVbase,
        'Sb': addSbase,
    }

    compTypeDict = ['G', 'T','LT','M','C', 'Vb', 'Sb', 'L']
    base = {
        'V' : None,
        'S' : None,
        'net' : ''
    }
    circFile = ""
    compList = []

    def __init__(self, fileName):
        self.circFile = fileName
        lines = self.getDataFromFile(fileName)
        for line in lines:
            self.addComponent(line)

    # ===== metodos privados =====
    # retorna apenas as linhas com informacoes uteis
    def getDataFromFile(self, fileName):
        lines = []
        with open(fileName) as f:
            for lin in f.readlines():
                lineSplit = lin.split(" ")
                if self.isUsefulData(lineSplit[0]):
                    lines.append(lin.rstrip('\n'))
        return lines
    # detect if current line is not a comment
    def isUsefulData(self, parameter):
        for x in range(len(self.compTypeDict)):
            if self.compTypeDict[x] in parameter[:len(self.compTypeDict[x])]:
                return True
    # add new component to the list based
    def addComponent(self, line):
        self.componentsInitDict[self.getComponentType(line)](self,line)
    # return the component type
    def getComponentType(self, line):
        parameter = line.split(" ")[0]
        for x in range(len(self.compTypeDict)):
            if self.compTypeDict[x] in parameter[:len(self.compTypeDict[x])]:
                return self.compTypeDict[x]
    # convert custom string to float
    def str2float(self, number):
        nb = number.lower()
        if nb.find('k') >= 0:
            return 1e3 * float(nb.replace('k', '.'))
        elif nb.find('m') >= 0:
            return 1e6 * float(nb.replace('m', '.'))
        else:
            return float(nb)
    # return list with all nets in the circuit
    def sortNets(self):
        netList = [self.base['net']]
        for x in range(len(self.compList)):
            if self.compList[x].net1 not in netList:
                netList.append(self.compList[x].net1)
                if self.compList[x].net2 not in netList:
                    netList.append(self.compList[x].net2)
        netList.remove('0')
        netList.sort()
        return netList
    # return list with all components in current net
    def sortComponentsInNet(self, net, vect):
        temp = [x for x in vect if x.net1 is net]
        temp.sort()
        return temp
    # get index of element with specified name
    def getIndexByName(self, name, vect):
        for x in range(len(vect)):
            if name in vect[x].name:
                return x
    # get Vb of specified net
    def getVbOfNet(self, net):
        pathToNet = self.getPathToNet(net)
        #print 'path to net ' + net + ' = ',
        #print [str(x) for x in pathToNet]
        return self.base['V'] * self.calcVbMultiplier(pathToNet)
        pass
    # return list of elements that goes from base net to specified net
    def getPathToNet(self, net):
        # remove all generators, motors and loads
        connectionsList = [x for x in self.compList if x.net2 is not '0']
        # init current net
        currentNet = self.base['net']
        # init vectors
        path = []
        branch = self.sortComponentsInNet(currentNet, connectionsList)
        #path += branch

        while currentNet is not net:
            # check if branch is empty
            if not branch:
                # remove component from connections list
                del connectionsList[self.getIndexByName(path[-1].name, connectionsList)]
                # update all vectors to remove deleted components
                path = [x for x in path if x in connectionsList]
                if self.sortComponentsInNet(self.base['net'], connectionsList):
                    branch = self.sortComponentsInNet(self.base['net'],connectionsList)
                if path:
                    branch.append(path[-1])
            # goto next component
            currentNet = branch[0].net2
            # append to path
            if branch[0] not in path:
                path.append(branch[0])
            # calculate next branch
            branch = [x for x in self.sortComponentsInNet(currentNet, connectionsList)]

        return [x.name for x in path]
    # get component voltage multiplier based on its name
    def getVoltageMultiplier(self, componentName):
        return self.compList[self.getIndexByName(componentName,self.compList)].Vmul
    # calculate the multiplier to get the new Vb
    def calcVbMultiplier(self,compVect):
        mul = 1
        for x in range(len(compVect)):
            mul *= self.compList[self.getIndexByName(compVect[x],self.compList)].Vmul
        return mul


    # ===== metodos publicos =====
    def printPu(self):
        self.pu()
        alphabet = 'VXR'
        for i in  range(len(self.compList)):
            temp = dir(self.compList[i])
            attrList = [x for x in temp if "_pu" in x]
            attr = sorted(attrList, key=lambda word: [alphabet.index(c) for c in word[0]])
            print self.compList[i].name + ' => ',
            for j in range(len(attr)):
                if getattr(self.compList[i], attr[j]):
                    print attr[j] + '= ' + str(getattr(self.compList[i],attr[j])) + ' ',
            print ''

    def pu(self):
        for x in range(len(self.compList)):
            #print 'finding path to: ' + self.compList[x].net1 + ', actual component: ' + self.compList[x].name
            currentVb = self.getVbOfNet(self.compList[x].net1)
            currentSb = self.base['S']
            #print 'current Vb = ' + str(currentVb) + ', current Sb = ' + str(currentSb)
            self.compList[x].initPu(currentVb, currentSb)
    def printCirc(self):
        pass
    def matrix(self):
        pass

