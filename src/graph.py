import matplotlib.pyplot as plt
import networkx as nx
import numpy as np


def project(points, direction):
    d = direction / np.linalg.norm(direction)
    y0 = np.array([1, 0, 0]) if np.array([0, 0, 1]).dot(d) == 1 else np.array([0, 0, 1])
    y1 = y0 - np.dot(d, y0) * d
    norm_y = y1 / np.linalg.norm(y1)
    x0 = np.cross(norm_y, d)
    norm_x = x0 / np.linalg.norm(x0)
    pos = {}
    for k in points:
        p0 = np.array(points[k])
        p1 = p0 - np.dot(d, p0) * d
        pos[k] = (np.dot(norm_y, p1), np.dot(norm_x, p1))
    return pos


class Graph:
    def __init__(self, nx_graph=None):
        self.g = nx.Graph(nx_graph)

    def copy(self):
        return Graph(self.g)

    def add_node(self, node, **attr):
        self.g.add_node(node, **attr)

    def add_edge(self, node1, node2, **attr):
        self.g.add_edge(node1, node2, **attr)

    def remove_node(self, node):
        self.g.remove_node(node)

    def nodes(self):
        return self.g.nodes

    def edges(self):
        return self.g.edges

    def degree(self):
        return self.g.degree

    def subgraph(self, nodes):
        return Graph(self.g.subgraph(nodes))

    def max_subgraph(self):
        mc = max(nx.connected_components(self.g), key=len)
        return Graph(self.g.subgraph(mc))

    def is_connected(self):
        return nx.is_connected(self.g)

    def get_node_attributes(self, attr):
        return nx.get_node_attributes(self.g, attr)

    def get_edge_attributes(self, attr):
        return nx.get_edge_attributes(self.g, attr)

    def draw_graph(self, highlight=None, direction=(0, 0, 1)):
        plt.figure(figsize=(10, 10))
        points = self.get_node_attributes('location')
        pos = project(points, np.array(direction))
        label = self.get_node_attributes('label')
        edge_label = self.get_edge_attributes('dist')
        nx.draw_networkx(self.g, pos, alpha=0.7, with_labels=False, edge_color='.4')
        if highlight is not None:
            nx.draw_networkx_nodes(self.g, pos=pos, nodelist=highlight, node_color='r')
        nx.draw_networkx_labels(self.g, pos, labels=label)
        nx.draw_networkx_edge_labels(self.g, pos, edge_labels=edge_label)
        plt.axis('off')


def convert_cell(cell):
    g = Graph()
    for k in cell.atom_dict:
        atom = cell.atom_dict[k]
        g.add_node(atom, location=(atom.x, atom.y, atom.z), label=atom.element + atom.index, mass=atom.mass)
        for c in atom.connections:
            neigh = cell.atom_dict[c]
            if (atom, neigh) not in g.edges():
                g.add_edge(atom, neigh, dist=round(atom.connections[c], 2))
    return g
