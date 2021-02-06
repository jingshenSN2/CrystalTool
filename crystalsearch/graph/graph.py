import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

from crystalsearch import graph


class Graph:
    """
    包装nx.Graph的图类
    """

    def __init__(self, name, nx_graph=None):
        self.name = name
        self.g = nx.Graph(nx_graph)

    def copy(self):
        return Graph(self.name, self.g)

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
        return Graph(self.name, self.g.subgraph(nodes))

    def max_subgraph(self):
        mc = max(nx.connected_components(self.g), key=len)
        return Graph(self.name, self.g.subgraph(mc))

    def is_connected(self):
        return nx.is_connected(self.g)

    def get_node_attributes(self, attr):
        return nx.get_node_attributes(self.g, attr)

    def get_edge_attributes(self, attr):
        return nx.get_edge_attributes(self.g, attr)

    def draw_graph(self, highlight=None, direction=(0, 0, 1)):
        plt.figure(figsize=(10, 10))
        points = self.get_node_attributes('location')
        pos = graph.project3d(points, np.array(direction))
        label = self.get_node_attributes('label')
        edge_label = self.get_edge_attributes('dist')
        nx.draw_networkx(self.g, pos, alpha=0.7, with_labels=False, edge_color='.4')
        if highlight is not None:
            nx.draw_networkx_nodes(self.g, pos=pos, nodelist=highlight, node_color='r')
        nx.draw_networkx_labels(self.g, pos, labels=label)
        nx.draw_networkx_edge_labels(self.g, pos, edge_labels=edge_label)
        plt.axis('off')
