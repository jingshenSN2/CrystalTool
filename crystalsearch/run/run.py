from crystalsearch import parser, matcher, graph


def run(res_files, pdb_file, keep_skeleton, max_loss_atom, max_subgraph):
    """运行所有来自图形界面的任务"""
    results = []
    for res in res_files:
        result = run_one(res, pdb_file, keep_skeleton, max_loss_atom, max_subgraph)
        results.append(result)
    return results


def run_one(res_file, pdb_file, keep_skeleton, max_loss_atom, max_subgraph):
    """运行一个来自图形界面的任务"""
    target = graph.cell2graph(parser.parseFromRES(res_file))
    query = graph.cell2graph(parser.parseFromPDB(pdb_file)).max_subgraph()
    gm = matcher.GraphMatcher(target, query, keep_skeleton, max_loss_atom, max_subgraph)
    result = gm.match()
    return result
