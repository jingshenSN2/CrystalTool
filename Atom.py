class Atom:
    def __init__(self, element, x, y, z, intensity):
        self.element = element
        self.x = x
        self.y = y
        self.z = z
        self.intensity = intensity
        self.neighbors = {}

    def add_neighbor(self, atom, distance):
        self.neighbors[atom] = distance
