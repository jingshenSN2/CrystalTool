import matplotlib.pyplot as plt
import networkx as nx


def convert_cell(cell):
    g = nx.Graph()
    for k in cell.atom_dict:
        atom = cell.atom_dict[k]
        g.add_node(atom, location=[atom.x, atom.y, atom.z], label=atom.element + atom.index, mass=atom.mass)
        for c in atom.connections:
            neigh = cell.atom_dict[c]
            if (atom, neigh) not in g.edges:
                g.add_edge(atom, neigh, dist=round(atom.connections[c], 2))
    return g


def max_subgraph(graph):
    c = max(nx.connected_components(graph), key=len)
    return graph.subgraph(c)


def max_subgraph_converter(cell):
    return max_subgraph(convert_cell(cell))


def draw_graph(graph, direction='c'):
    plt.figure(figsize=(10, 10))
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
    plt.show()


def draw_graph_highlight(graph, highlight, direction='c'):
    plt.figure(figsize=(10, 10))
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

