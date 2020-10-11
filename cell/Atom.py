class Atom:
    def __init__(self, element, index, mass, x, y, z, intensity):
        self.element = element
        self.index = index
        self.mass = mass
        self.x = x
        self.y = y
        self.z = z
        self.intensity = intensity
        self.neighbors = {}

    def add_neighbor(self, atom, distance):
        self.neighbors[atom] = distance

    def remove_neighbor(self, atom):
        del self.neighbors[atom]
