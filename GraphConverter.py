import networkx as nx


def graph_converter(cell):
    g = nx.Graph()
    for atom in cell.atom_list:
        g.add_node(atom, location=(atom.x, atom.y), label=atom.element + atom.index)
        for neighbor in atom.neighbors.keys():
            if (atom, neighbor) not in g.edges:
                g.add_edge(atom, neighbor, dist=round(atom.neighbors[neighbor], 2))
    return g
