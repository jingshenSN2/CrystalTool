import math

class Atom():
    def __int__(self, type, cords):
        self.type = type
        self.cords = cords
        self.neighbors = set()

    def addNeighbor(self, atom):
        self.neighbors.add(atom)


class Cell():
    def __init__(self):
        self.latParaA = 0
        self.latParaB = 0
        self.latParaC = 0
        self.latParaAlpha = 0
        self.latParaBeta = 0
        self.latParaGamma = 0
        self.atomList = []

    def setLatPara(self, a, b, c):
        self.latParaA = a
        self.latParaB = b
        self.latParaC = c

    def setLatPara(self, a, b, c, alpha, beta, gamma):
        self.setLatPara(self, a, b, c)
        self.latParaAlpha = alpha
        self.latParaBeta = beta
        self.latParaGamma = gamma

    def addAtom(self, atom):
        self.atomList.append(atom)

    def expand(self):
        for atom in self.atomList:
            newAtomList = []
            for i in range(2):
                for j in range(2):
                    for k in range(2):
                        if i * j * k != 0:
                            newAtomList.append(
                                Atom(atom.type, (atom.cords[0] + i, atom.cords[1] + j, atom.cords[2] + k)))
            for newAtom in newAtomList:
                self.atomList.append(newAtom)
        # 我的想法是expand不变晶胞参数,然后新加的原子也可以用大于1的分数坐标表示,这样计算距离也很方便

    def calcDist(self, atom1, atom2):
        return math.inf

    def calcNeighbors(self, distThres): # distThres表示距离阈值
        for ind1 in range(len(self.atomList)):
            for ind2 in range(ind1 + 1, len(self.atomList)):
                if self.calcDist(self.atomList[ind1], self.atomList[ind2]) <= distThres:
                    self.atomList[ind1].addNeighbor(self.atomList[ind2])