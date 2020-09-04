class Atom:
    def __init__(self, element, cords, intensity):
        self.element = element
        self.cords = cords
        self.intensity = intensity
        self.neighbors = set()

    def add_neighbor(self, atom):
        self.neighbors.add(atom)
