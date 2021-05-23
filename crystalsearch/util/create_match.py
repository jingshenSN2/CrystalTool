from crystalbase import parseFromRES, parseFromPDB
from crystalsearch.graph.convert import cellToGraph
from ..matcher import GraphMatcherOld, GraphMatcherVF2


def match_one(res_file, pdb_file, use_old_algorithm: bool, max_loss_atom: int, multilayer: tuple, threshold: dict,
              sort_by: list):
    """运行一个来自图形界面的任务"""
    target = cellToGraph(parseFromRES(res_file, multilayer))
    query = cellToGraph(parseFromPDB(pdb_file)).max_subgraph()
    if use_old_algorithm:
        # 旧算法
        gm = GraphMatcherOld(target, query, loss_atom=max_loss_atom)
    else:
        gm = GraphMatcherVF2(target, query, loss_atom=max_loss_atom)
    result = gm.get_result(threshold, sort_by)
    return result
