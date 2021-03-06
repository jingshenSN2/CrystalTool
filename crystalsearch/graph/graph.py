import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

from crystalsearch import graph


class Graph:
    """
    包装nx.Graph的图类
    """

    def __init__(self, name, nx_graph=None):
        self.name = name
        self.g = nx.Graph(nx_graph)

    def __len__(self):
        return len(self.nodes())

    def __getitem__(self, node):
        return self.g[node]

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

    def degree(self, node=None):
        if node is not None:
            return self.g.degree[node]
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
        """用matlotlib画二维投影图"""
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

    def draw_3d_graph(self, highlight=None):
        """用matlotlib画三维图"""
        points = self.get_node_attributes('location')
        label = self.get_node_attributes('label')
        fig = plt.figure(figsize=(10, 7))
        ax = Axes3D(fig)
        for key, value in points.items():
            c = 'blue'
            if key in highlight:
                c = 'red'
            xi, yi, zi = value
            ax.scatter(xi, yi, zi, label[key], c=c, alpha=0.9)
        for i, j in enumerate(self.edges()):
            x = np.array((points[j[0]][0], points[j[1]][0]))
            y = np.array((points[j[0]][1], points[j[1]][1]))
            z = np.array((points[j[0]][2], points[j[1]][2]))
            ax.plot(x, y, z, c='black', alpha=0.9)

    def number_of_edges(self, u, v):
        return self.g.number_of_edges(u, v)



