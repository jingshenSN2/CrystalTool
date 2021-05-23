from crystalbase import parse_from_res, parse_from_pdb
from crystalsearch.graph.convert import cell_to_graph
from ..matcher import GraphMatcherOld, GraphMatcherVF2


def match_one(res_file, pdb_file, use_old_algorithm: bool, max_loss_atom: int, multilayer: tuple, threshold: dict,
              sort_by: list):
    """运行一个来自图形界面的任务"""
    target = cell_to_graph(parse_from_res(res_file, multilayer))
    query = cell_to_graph(parse_from_pdb(pdb_file)).max_subgraph()
    if use_old_algorithm:
        # 旧算法
        gm = GraphMatcherOld(target, query, loss_atom=max_loss_atom)
    else:
        gm = GraphMatcherVF2(target, query, loss_atom=max_loss_atom)
    result = gm.get_result(threshold, sort_by)
    return result
