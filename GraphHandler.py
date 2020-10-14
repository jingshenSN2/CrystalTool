import matplotlib.pyplot as plt
import networkx as nx


def graph_converter(cell):
    g = nx.Graph()
    for atom in cell.atom_list:
        g.add_node(atom, location=[atom.x, atom.y, atom.z], label=atom.element + atom.index, mass=atom.mass)
        for neighbor in atom.neighbors.keys():
            if (atom, neighbor) not in g.edges:
                g.add_edge(atom, neighbor, dist=round(atom.neighbors[neighbor], 2))
    return g


def max_subgraph(graph):
    c = max(nx.connected_components(graph), key=len)
    return graph.subgraph(c)


def max_subgraph_converter(cell):
    return max_subgraph(graph_converter(cell))


def draw_graph(graph, direction='c'):
    plt.figure(figsize=(10, 9))
    cord = nx.get_node_attributes(graph, 'location')
    pos = {}
    for key in cord.keys():
        tmp = cord[key]
        if direction == 'a':
            pos[key] = (tmp[1], tmp[2])
        elif direction == 'b':
            pos[key] = (tmp[0], tmp[2])
        elif direction == 'c':
            pos[key] = (tmp[0], tmp[1])
        else:
            print('invalid direction.')
            return
    label = nx.get_node_attributes(graph, 'label')
    edge_label = nx.get_edge_attributes(graph, 'dist')
    nx.draw_networkx(graph, pos, alpha=0.7, with_labels=False, edge_color='.4')
    nx.draw_networkx_labels(graph, pos, labels=label)
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_label)
    plt.axis('off')
    plt.tight_layout()
    plt.show()


def draw_graph_highlight(graph, highlight, direction='c'):
    plt.figure(figsize=(10, 9))
    cord = nx.get_node_attributes(graph, 'location')
    pos = {}
    for key in cord.keys():
        tmp = cord[key]
        if direction == 'a':
            pos[key] = (tmp[1], tmp[2])
        elif direction == 'b':
            pos[key] = (tmp[0], tmp[2])
        elif direction == 'c':
            pos[key] = (tmp[0], tmp[1])
        else:
            print('invalid direction.')
            return
    label = nx.get_node_attributes(graph, 'label')
    edge_label = nx.get_edge_attributes(graph, 'dist')
    nx.draw_networkx(graph, pos, alpha=0.7, with_labels=False, edge_color='.4')
    nx.draw_networkx_nodes(graph, pos=pos, nodelist=highlight, node_color='r')
    nx.draw_networkx_labels(graph, pos, labels=label)
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_label)
    plt.axis('off')
    plt.tight_layout()
    plt.show()

