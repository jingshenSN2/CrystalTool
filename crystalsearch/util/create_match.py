from crystalbase import parseFromRES, parseFromPDB
from .convert_cell import cellToGraph
from ..matcher import GraphMatcherOld, GraphMatcherVF2


def match_one(res_file, pdb_file, use_old_algorithm: bool, max_loss_atom: int, threshold: dict, sort_by: list):
    """运行一个来自图形界面的任务"""
    target = cellToGraph(parseFromRES(res_file))  # 读取RES并转化为目标图
    query = cellToGraph(parseFromPDB(pdb_file)).max_subgraph()  # 读取PDB并转化为查询图
    if use_old_algorithm:
        # 旧算法
        gm = GraphMatcherOld(target, query, loss_atom=max_loss_atom)
    else:
        gm = GraphMatcherVF2(target, query, loss_atom=max_loss_atom)
    result = gm.get_result(threshold, sort_by)
    return result
