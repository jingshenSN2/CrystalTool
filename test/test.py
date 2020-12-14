import time

from src import parser, matcher, graph

cell = parser.parse_res('test/c21_origin.res')
cell.calc_neighbors()
graph = graph.convert_cell(cell)
target = graph.max_subgraph(graph)
# GraphHandler.draw_graph(target, direction='a')
# GraphHandler.draw_graph(target, direction='b')
graph.draw_graph(target, direction='c')

pattern = parser.parse_pdb('test/query.pdb')
pattern.calc_neighbors()
graph2 = graph.convert_cell(pattern)
query = graph.max_subgraph(graph2)
# GraphHandler.draw_graph(query, direction='a')
# GraphHandler.draw_graph(query, direction='b')
graph.draw_graph(query, direction='c')

start = time.process_time()
result1 = matcher.match_1(target, query, 10)
if result1:
    for i in result1:
        graph.draw_graph_highlight(target, i)
        rmsd = matcher.rmsd(i)
        print('rmsd %.2f' % rmsd)
        break
end = time.process_time()
print(end - start)

start = time.process_time()
result2 = matcher.match_2(target, query, 5)
if result2:
    for i in result2:
        graph.draw_graph_highlight(target, i)
        rmsd = matcher.rmsd(i)
        print('rmsd %.2f' % rmsd)
        break
end = time.process_time()
print(end - start)
