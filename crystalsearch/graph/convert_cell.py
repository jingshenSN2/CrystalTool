from crystalsearch.Atom import AtomGroup
from crystalsearch.graph import Graph


def convert_cell(cell: AtomGroup):
    """晶胞类转图类"""
    g = Graph()
    for k in cell.atom_dict:
        atom = cell.atom_dict[k]
        g.add_node(atom, location=(atom.x, atom.y, atom.z), label=atom.label, mass=atom.mass)
    for b, d in cell.bond_dict.items():
        k1, k2 = list(b)
        g.add_edge(cell.atom_dict[k1], cell.atom_dict[k2], dist=round(d, 2))
    return g
