from crystalsearch import parser, matcher, graph
import matplotlib.pyplot as plt

#graph.cell2graph(parser.parseFromRES('./test/c21.res')).draw_3d_graph()
#plt.show()

target = graph.cell2graph(parser.parseFromRES('./test2/3.res'))
query = graph.cell2graph(parser.parseFromPDB('./test2/mdcb.pdb')).max_subgraph()

gm = matcher.GraphMatcher(target, query, True, 2, 1000)
result = gm.match()
print(result.is_matched)
for p,a,b,c in result.results:
    target.draw_3d_graph(p)
    plt.show()
    break