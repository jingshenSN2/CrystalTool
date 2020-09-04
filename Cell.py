import itertools
import math

import numpy as np

from Atom import Atom


class Cell:
    def __init__(self):
        self.a = 0
        self.b = 0
        self.c = 0
        self.alpha = 0
        self.beta = 0
        self.gamma = 0
        self.atom_list = []

    def set_lat_para(self, a, b, c, alpha, beta, gamma):
        self.a = a
        self.b = b
        self.c = c
        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma

    def add_atom(self, element, cord, intensity):
        self.atom_list.append(Atom(element, cord, intensity))

    def expand(self):
        for atom in self.atom_list.copy():
            for i, j, k in itertools.permutations([0, 1, 2]):
                print(i, j, k)
                if i * j * k != 0:
                    self.add_atom(atom.element, atom.cords + np.array([i, j, k]), atom.intensity)

    def distance(self, atom1, atom2):
        atom1.cords * np.array([self.a, self.b, self.c])
        return math.inf

    def calc_neighbors(self, max_distance):
        for ind1 in range(len(self.atom_list)):
            for ind2 in range(ind1 + 1, len(self.atom_list)):
                if self.distance(self.atom_list[ind1], self.atom_list[ind2]) <= max_distance:
                    self.atom_list[ind1].add_neighbor(self.atom_list[ind2])
