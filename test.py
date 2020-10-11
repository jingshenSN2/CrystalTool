import CrystalParser
import GraphHandler
import MatchRater


cell = CrystalParser.parse_res('test/c21_origin.res')
cell.calc_neighbors()
graph = GraphHandler.graph_converter(cell)
target = GraphHandler.max_subgraph(graph)
# GraphHandler.draw_graph(target, direction='a')
# GraphHandler.draw_graph(target, direction='b')
GraphHandler.draw_graph(target, direction='c')

pattern = CrystalParser.parse_pdb('test/C15H21NO3S_C2.pdb')
pattern.calc_neighbors()
graph2 = GraphHandler.graph_converter(pattern)
query = GraphHandler.max_subgraph(graph2)
# GraphHandler.draw_graph(query, direction='a')
# GraphHandler.draw_graph(query, direction='b')
GraphHandler.draw_graph(query, direction='c')

mr = MatchRater.MatchRater(target, query)
result = mr.shirnk_match()
if result:
    for i in result:
        print(i)
        GraphHandler.draw_graph_highlight(target, i)

print(1)
