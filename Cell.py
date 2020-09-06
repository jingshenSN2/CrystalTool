import itertools
import math

import DistanceHelper
from Atom import Atom


def square_distance(a, b, c, alpha, beta, gamma, dx, dy, dz):
    return a ** 2 * dx ** 2 + b ** 2 * dy ** 2 + c ** 2 * dz ** 2 + 2 * b * c * dy * dz * math.cos(alpha) \
           + 2 * a * c * dx * dz * math.cos(beta) + 2 * a * b * dx * dy * math.cos(gamma)


class Cell:
    def __init__(self):
        self.a = 0
        self.b = 0
        self.c = 0
        self.alpha = 0
        self.beta = 0
        self.gamma = 0
        self.atom_list = []
        self.max_distances = DistanceHelper.gen_max_distances('atom_properties.txt')

    def set_lat_para(self, a, b, c, alpha, beta, gamma):
        self.a = a
        self.b = b
        self.c = c
        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma

    def add_atom(self, element, index, x, y, z, intensity):
        self.atom_list.append(Atom(element, index, x, y, z, intensity))

    def expand(self):
        for i, j, k in itertools.product(*[0, 1] * 3):
            if i == j == k == 0:
                continue
            print(i, j, k)
            for atom in self.atom_list.copy():
                self.add_atom(atom.element, atom.index, atom.x + i, atom.y + j, atom.z + k, atom.intensity)

    def distance_judge(self, atom1, atom2):
        dx = atom2.x - atom1.x
        dy = atom2.y - atom1.y
        dz = atom2.z - atom1.z
        dist = math.sqrt(square_distance(self.a, self.b, self.c, self.alpha, self.beta, self.gamma, dx, dy, dz))
        atom_pair = frozenset([atom1.element, atom2.element])
        return True, dist if dist <= self.max_distances[atom_pair] else False

    def calc_neighbors(self):
        for atom1, atom2 in itertools.combinations(self.atom_list, 2):
            res = self.distance_judge(atom1, atom2)
            if res[0]:
                atom1.add_neighbor(atom2, res[1])
                atom2.add_neighbor(atom1, res[1])
