from ..graph import Graph
from crystalbase import AtomGroup


def cellToGraph(cell: AtomGroup):
    """晶胞类转图类"""
    g = Graph(cell.name)
    for k in cell.atom_dict:
        # 将晶胞中所有原子作为图的节点
        atom = cell.atom_dict[k]
        g.add_node(atom, location=(atom.x, atom.y, atom.z), label=atom.label, mass=atom.mass)
    for b, d in cell.bond_dict.items():
        # 将晶胞中所有化学键作为图的边
        k1, k2 = list(b)
        g.add_edge(cell.atom_dict[k1], cell.atom_dict[k2], dist=round(d, 2))
    return g
