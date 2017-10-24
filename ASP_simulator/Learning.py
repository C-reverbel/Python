import copy

class Component:
    name = ""
    type = ""
    net1 = ""
    net2 = ""

    def __init__(self, parameters):
        #self.parameters = dict(self.parameters)
        self.name = parameters[0]
        self.net1 = parameters[1]
        self.net2 = parameters[2]
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
class Generator(Component):
    V = 0
    S = 0
    X = 0
    def __init__(self, parameters):
        self.type = 'G'
        Component.__init__(self, parameters)
        self.V = self.str2float(parameters[3])
        self.S = self.str2float(parameters[4])
        self.X = self.str2float(parameters[5])
class Transformer(Component):
    Pri = ''
    VPri = 0
    Sec = ''
    VSec = 0
    S = 0
    X = 0
    def __init__(self, parameters):
        self.type = 'T'
        Component.__init__(self, parameters)
        self.Pri = parameters[3]
        self.VPri = self.str2float(parameters[4])
        self.Sec = parameters[5]
        self.VSec = self.str2float(parameters[6])
        self.S = self.str2float(parameters[7])
        self.X = self.str2float(parameters[8])
class TransmissionLine(Component):
    R = 0
    L = 0
    C = 0
    def __init__(self, parameters):
        self.type = 'LT'
        Component.__init__(self, parameters)
        self.R = self.str2float(parameters[3])
        self.L = self.str2float(parameters[4])
        self.C = self.str2float(parameters[5])
class Motor(Component):
    V = 0
    S = 0
    X = 0
    def __init__(self, parameters):
        self.type = 'M'
        Component.__init__(self, parameters)
        self.V = self.str2float(parameters[3])
        self.S = self.str2float(parameters[4])
        self.X = self.str2float(parameters[5])

class Circuit:

    # list of methods to initialize new components
    def addGenerator(self, paramList):
        parameters = paramList.split(" ")
        tempGen = Generator(parameters)
        self.compList.append(tempGen)
    def addTransformer(self, paramList):
        parameters = paramList.split(" ")
        tempTrafo = Transformer(parameters)
        self.compList.append(tempTrafo)
    def addTransmissionLine(self, paramList):
        parameters = paramList.split(" ")
        tempTL = TransmissionLine(parameters)
        self.compList.append(tempTL)
    def addMotor(self, paramList):
        parameters = paramList.split(" ")
        tempMotor = Motor(parameters)
        self.compList.append(tempMotor)
    # faltou isso
    def addLoad(self, paramList):
        pass
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
        'Vb': addVbase,
        'Sb': addSbase,
    }
    compTypeDict = ['G', 'T','LT','M','C', 'Vb', 'Sb']
    base = {
        'V' : None,
        'S' : None,
        'net' : ''
    }
    circFile = ""
    compList = []
    circFile = ""

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
    def unionWithoutDuplicate(self,vect1,vect2):
        vect = []
        for i in vect1:
            if i not in vect:
                vect.append(i)
        for i in vect2:
            if i not in vect:
                vect.append(i)
        return vect
    # get Vb of specified net
    def getVbOfNet(self, net):
        pathToNet = self.getPathToNet(net)
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

        while currentNet is not net:
            # check if branch is empty
            if not branch:
                # remove component from connections list
                del connectionsList[self.getIndexByName(path[-1].name, connectionsList)]
                # update all vectors to remove deleted components
                path = [x for x in path if x in connectionsList]
                branch.append(path[-1])
            # goto next component
            currentNet = branch[0].net2
            # append to path
            if branch[0] not in path:
                path.append(branch[0])
            # calculate next branch
            branch = [x for x in self.sortComponentsInNet(currentNet, connectionsList)]
        return [x.name for x in path]

    def calcPu(self,compVect, Vb):
        pass


    # ===== metodos publicos =====
    def pu(self):
        # get list of all nets in the circuit
        netStack = self.sortNets()
        for x in range(len(netStack)):
            # get list of components for current net
            compVect = self.sortComponentsInNet(netStack[x], self.compList)
            # get Vb for current net
            currentVb = self.getVbOfNet(netStack[x])
            # calculate and update PU values of components in current net
            self.calcPu(compVect,currentVb)


    def printCirc(self):
        pass
    def matrix(self):
        pass

# nets = sortNets()
# for net in nets:
#     V = getVbOfNet[net]
#     componentsList = sortComponentsInNet[net, components]
#     for component in componentsList:
#         calcPu[component,V]