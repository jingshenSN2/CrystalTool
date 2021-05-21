import networkx as nx
import numpy as np

from .project import project3d


class Graph:
    """
    包装nx.Graph的图类
    """

    def __init__(self, name, nx_graph=None):
        self.name = name
        self.info = {}
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

    def draw_graph(self, axes, highlight=None, direction=(0, 0, 1), rotation=None):
        """用matlotlib画二维投影图"""
        axes.clear()
        points = self.get_node_attributes('location')
        if rotation is not None:
            for k in points:
                points[k] = np.dot(points[k], rotation)
        pos = project3d(points, np.array(direction))
        label = self.get_node_attributes('label')
        edge_label = self.get_edge_attributes('dist')
        nx.draw_networkx(self.g, pos, alpha=0.7, with_labels=False, edge_color='.4', ax=axes)
        if highlight is not None:
            nx.draw_networkx_nodes(self.g, pos=pos, nodelist=highlight, node_color='r', ax=axes)
        nx.draw_networkx_labels(self.g, pos, labels=label, ax=axes)
        nx.draw_networkx_edge_labels(self.g, pos, edge_labels=edge_label, ax=axes)
        axes.axis('off')

    def draw_3d_graph(self, axes, highlight=None):
        """用matlotlib画三维图"""
        axes.clear()
        points = self.get_node_attributes('location')
        label = self.get_node_attributes('label')
        if highlight is None:
            highlight = []
        for key, value in points.items():
            c = 'blue'  # 普通原子为蓝色
            if key in highlight:
                c = 'red'  # 高亮原子用红色表示
            xi, yi, zi = value
            axes.scatter(xi, yi, zi, label[key], c=c, alpha=0.9)
        for i, j in enumerate(self.edges()):
            # 用两端原子的坐标连线，绘制化学键
            x = np.array((points[j[0]][0], points[j[1]][0]))
            y = np.array((points[j[0]][1], points[j[1]][1]))
            z = np.array((points[j[0]][2], points[j[1]][2]))
            axes.plot(x, y, z, c='black', alpha=0.9)

    def number_of_edges(self, u, v):
        return self.g.number_of_edges(u, v)
