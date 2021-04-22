
import matplotlib.pyplot as plt

from crystalbase import parseFromRES
from crystalsearch import cellToGraph

target = cellToGraph(parseFromRES('./test3/0620_expF_0_7_expS_1_4_0620_b.res', multilayer=(False, False, False)))
fig = plt.Figure()
target.draw_3d_graph(fig)
fig.savefig('./11.png')

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


