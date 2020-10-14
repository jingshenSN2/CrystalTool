import sys
import getopt
import CrystalParser as CP
import GraphHandler as GH
import MatchRater as MR


def main(argv):
    target_file = None
    query_file = None
    match = None
    loss_atom = None
    show_graph = False
    silent = False
    result = None
    best_result = None
    rmsd = -1
    opts, args = getopt.getopt(argv, '-h-t:-q:-m:-l:-g-s', ['help', 'graph', 'silent', 'target=', 'query=', 'match=', 'lossatom='])
    for opt, arg in opts:
        if opt == '-h':
            print('dos.py -t <res_file> -q <pdb_file> -m <1 or 2> [-g]')
            sys.exit()
        elif opt in ('-t', '--target'):
            target_file = arg
        elif opt in ('-q', '--query'):
            query_file = arg
        elif opt in ('-m', '--match'):
            match = arg
        elif opt in ('-l', '--lossatom'):
            if '.' in arg:
                loss_atom = float(arg)
            else:
                loss_atom = int(arg)
        elif opt in ('-g', '--graph'):
            show_graph = True
        elif opt in ('-s', '--silent'):
            silent = True
    print('读取res文件...') if not silent else ''
    target = GH.graph_converter(CP.parse_res(target_file))
    print('读取pdb文件...') if not silent else ''
    query = GH.max_subgraph_converter(CP.parse_pdb(query_file))
    print('开始匹配，匹配算法为match_%s' % match) if not silent else ''
    if match == '1':
        result = MR.match_1(target, query, loss_atom)
    elif match == '2':
        result = MR.match_2(target, query, loss_atom)
    print('匹配成功！' if result else '匹配失败，请调整参数。') if not silent else ''
    if result:
        rmsd, best_result = MR.best_result(result)
        if show_graph:
            GH.draw_graph_highlight(target, best_result)
    print('True %.2f' % rmsd) if result else print('False')


if __name__ == '__main__':
    main(sys.argv[1:])