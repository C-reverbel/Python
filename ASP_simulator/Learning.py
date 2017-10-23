import copy

class Component:
    parameters = {
        "name" : "",
        "type" : "",
        "net1" : "",
        "net2" : "",
    }
    def __init__(self, parameters):
        self.parameters = dict(self.parameters)
        self.parameters["type"] = parameters[0]
        self.parameters["name"] = parameters[1]
        self.parameters["net1"] = parameters[2]
        self.parameters["net2"] = parameters[3]

class Circuit:

    # list of methods to initialize new components
    def addGenerator(self, paramList):
        parameters = paramList.split(" ")
        print parameters
        tempGen = Component(['G'] + parameters)
        # botar mais coisas aqui
        self.compList.append(tempGen)
        print map(lambda x : x.parameters['name'], self.compList)

    def addTransformer(self, paramList):
        print 'transformador'
    def addTransmissionLine(self, paramList):
        print 'linha'
    def addMotor(self, paramList):
        print 'motor'
    def addLoad(self, paramList):
        print 'carga'
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
    def getVbOfNet(self, net):
        pass
    def sortComponentsInNet(self, net, components):
        pass
    def sortNets(self):
        pass



    # metodos publicos
    def pu(self):
        pass

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