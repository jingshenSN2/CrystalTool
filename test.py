import matplotlib.pyplot as plt
import networkx as nx

import CrystalParser
import GraphConverter

cell = CrystalParser.parse_res('c21.res')
cell.calc_neighbors()
graph = GraphConverter.graph_converter(cell)
c = max(nx.connected_components(graph), key=len)
graph = graph.subgraph(c)
plt.figure(figsize=(10, 9))
pos = nx.random_layout(graph)
nx.draw_networkx(graph, pos, alpha=0.7, with_labels=False, edge_color='.4')
plt.axis('off')
plt.tight_layout()
plt.show()

print(cell.atom_list)
