import os


def str2float(number):
	nb = number.lower()
	if nb.find('k') >= 0:
		return 1e3 * float(nb.replace('k', '.'))
	elif nb.find('m') >= 0:
		return 1e6 * float(nb.replace('m', '.'))
	else:
		return float(nb)

class Generator:
	def __init__(self, parameters = []):
		self.name = parameters[0]
		self.V = str2float(parameters[3])
		self.S = str2float(parameters[4])
		self.X = str2float(parameters[5])
		self.nets = parameters[1:3]
class TransmissionLine:
	def __init__(self, parameters = []):
		self.name = parameters[0]
		self.R = str2float(parameters[3])
		self.L = str2float(parameters[4])
		self.C = str2float(parameters[5])
		self.nets = parameters[1:3]
class Transformer:
	def __init__(self, parameters = []):
		self.name = parameters[0]
		self.Pri = parameters[3]
		self.Sec = parameters[5]
		self.VPri = str2float(parameters[4])
		self.VSec = str2float(parameters[6])
		self.S = str2float(parameters[7])
		self.X = str2float(parameters[8])
		self.nets = parameters[1:3]

class Circuit:

	generators = []
	transmissionLines = []
	loads = []
	transformers = []

	Vb = []
	Sb =  None

	circFIFO = []
	branchFILO = []

	# metodos publicos
	def __init__(self, circFile):
		self.circFile = circFile

		with open(circFile) as f:
			lines = f.readlines()
		for line in lines:
			lineSplit = line.split(" ")
			self.initCircuit(lineSplit)

	def printParam(self):
		try:
			print 'Vb = ' + str(self.Vb[0]) + '; Sb = ' + str(self.Sb)
		except:
			pass
		if self.generators.__len__() > 0:
			print 'Generators:'
			for x in range (0,self.generators.__len__()):
				print '	' + self.generators[x].name + ' : ',
				print 'V = ' + str(self.generators[x].V) + '; ',
				print 'S = ' + str(self.generators[x].S) + '; ',
				print 'X = ' + str(self.generators[x].X);
		if self.transformers.__len__() > 0:
			print 'Transformers:'
			for x in range(0, self.transformers.__len__()):
				print '	' + self.transformers[x].name + ' : ',
				print self.transformers[x].Pri + '/' + self.transformers[x].Sec + '   ',
				print str(self.transformers[x].VPri) + '/' + str(self.transformers[x].VSec) + '; ',
				print 'S = ' + str(self.transformers[x].S) + '; ',
				print 'X = ' + str(self.transformers[x].X);
		# faltam as linhas de transmissao

	def calcPU(self):
		pass

	def printParamPU(self):
		pass

	# metodos privados
	def initCircuit(self, lineSplit):
		if lineSplit[0][0] == 'G':  # init new generator
			tempGen = Generator(lineSplit)
			self.generators.append(tempGen)
		elif lineSplit[0][0] == 'T':
			tempTrans = Transformer(lineSplit)
			self.transformers.append(tempTrans)
		elif lineSplit[0][0] == 'L':
			if lineSplit[0][1] == 'T':
				tempLine = TransmissionLine(lineSplit)
				self.transmissionLines.append(tempLine)
		elif lineSplit[0][0] == 'V':
			if lineSplit[0][1] == 'b':
				self.Vb = [str2float(lineSplit[1]), lineSplit[2].rstrip('\n')]
		elif lineSplit[0][0] == 'S':
			if lineSplit[0][1] == 'b':
				self.Sb = str2float(lineSplit[1])
	def calcFIFO(self):
		currentNet = 0
		compVec = []
		netList = []
		netList.append(currentNet)

		#calcula numero de elementos
		fifoSize = self.generators.__len__() + self.transformers.__len__() + self.transmissionLines.__len__()

		# inicializa a fila
		for gen in self.generators:
			if gen.nets[0] == self.Vb[1] and gen.V == self.Vb[0]:
				self.circFIFO.append(gen.name)
				currentNet = gen.nets[0]
				netList.append(currentNet)
				break
		# segue preenchendo a fila partindo do primeiro elemento
		#while self.circFIFO.__len__() != fifoSize:
		# verifica componentes ligados a barra atual
		compVec = self.getCompsInNet(currentNet)
		for comp in compVec:
			if (comp not in self.circFIFO):
				self.circFIFO.append(comp)
		# decide o proximo net



	def getCompsInNet(self,net):
		compVec = []
		# geradores
		for gen in self.generators:
			if net in gen.nets:
				compVec.append(gen.name)
		# trafos
		for trafo in self.transformers:
			if net in trafo.nets:
				compVec.append(trafo.name)
		# linhas
		for line in self.transmissionLines:
			if net in line.nets:
				compVec.append(line.name)
		return compVec
	def getNetsFromComp(self,label):
		pass

