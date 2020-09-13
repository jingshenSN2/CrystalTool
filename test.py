import matplotlib.pyplot as plt
import networkx as nx

import CrystalParser
import GraphConverter

cell = CrystalParser.parse_res('c21_origin.res')
cell.calc_neighbors()
graph = GraphConverter.graph_converter(cell)
c = max(nx.connected_components(graph), key=len)
graph = graph.subgraph(c)
plt.figure(figsize=(10, 9))
pos = nx.get_node_attributes(graph, 'location')
label = nx.get_node_attributes(graph, 'label')
edge_label = nx.get_edge_attributes(graph, 'dist')
nx.draw_networkx(graph, pos, alpha=0.7, with_labels=False, edge_color='.4')
nx.draw_networkx_labels(graph, pos, labels=label)
nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_label)
plt.axis('off')
plt.tight_layout()
plt.show()

print(cell.atom_list)
