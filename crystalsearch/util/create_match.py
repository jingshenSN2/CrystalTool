from crystalbase import parseFromRES, parseFromPDB
from .convert_cell import cellToGraph
from ..matcher import GraphMatcherOld, GraphMatcherVF2


def match_one(res_file, pdb_file, use_old_algorithm: bool, max_loss_atom: int, threshold: dict, sort_by: list):
    """运行一个来自图形界面的任务"""
    target = cellToGraph(parseFromRES(res_file))
    query = cellToGraph(parseFromPDB(pdb_file)).max_subgraph()
    if use_old_algorithm:
        gm = GraphMatcherOld(target, query, loss_atom=max_loss_atom)
    else:
        gm = GraphMatcherVF2(target, query, loss_atom=max_loss_atom)
    result = gm.get_result(threshold, sort_by)
    return result
