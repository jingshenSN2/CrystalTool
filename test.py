import networkx as nx

import CrystalParser
import GraphHandler


cell = CrystalParser.parse_res('c21_origin.res')
cell.calc_neighbors()
graph = GraphHandler.graph_converter(cell)
subgraph = GraphHandler.max_subgraph(graph)
GraphHandler.draw_graph(subgraph)
GraphHandler.draw_graph(graph)

print(cell.atom_list)
