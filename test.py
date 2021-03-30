# graph.cellToGraph(util.parseFromRES('./test/c21.res')).draw_3d_graph()
# plt.show()

# target = graph.cellToGraph(util.parseFromRES('./test2/3.res'))
# query = graph.cellToGraph(util.parseFromPDB('./test2/mdcb.pdb')).max_subgraph()

# gm = matcher.GraphMatcher(target, query, True, 2, 1000)
# result = gm.match()
# print(result.is_matched)
# for p,a,b,c in result.results:
#    target.draw_3d_graph(p)
#    plt.show()
#    break
import numpy as np

print(np.array((0,0,1)) @ np.array([[0,0,1],[0,1,0],[1,0,0]]))


