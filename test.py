import networkx as nx

import CrystalParser
import GraphHandler


cell = CrystalParser.parse_res('c21_origin.res')
cell.calc_neighbors()
graph = GraphHandler.graph_converter(cell)
subgraph = GraphHandler.max_subgraph(graph)
GraphHandler.draw_graph(subgraph)
GraphHandler.draw_graph(graph)

benz = nx.Graph([(1,2),(2,3),(3,4),(4,5),(5,6),(6,1),(6,7),(7,8),(7,9),(7,10)])

gm = nx.algorithms.isomorphism.GraphMatcher(subgraph, benz, node_match=lambda x,y: True,
                                             edge_match=lambda x,y:True)
print(gm.subgraph_is_isomorphic())
for i in gm.subgraph_isomorphisms_iter():
    GraphHandler.draw_graph_highlight(subgraph, i)
    print(i)

