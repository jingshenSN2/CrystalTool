from crystalbase import parseFromRES, parseFromPDB
from ..matcher import GraphMatcherOld, GraphMatcherVF2
from .convert_cell import cellToGraph


def match_one(res_file: str, pdb_file: str, use_old_algorithm: bool, max_loss_atom: int, threshold: dict):
    """运行一个来自图形界面的任务"""
    target = cellToGraph(parseFromRES(res_file))
    query = cellToGraph(parseFromPDB(pdb_file)).max_subgraph()
    if use_old_algorithm:
        gm = GraphMatcherOld(target, query, loss_atom=max_loss_atom)
    else:
        gm = GraphMatcherVF2(target, query, loss_atom=max_loss_atom)
    result = gm.get_result(threshold)
    return result
