import time

import CrystalParser
import GraphHandler
import MatchRater

pattern = CrystalParser.parse_pdb('test/C15H21NO3S_C2.pdb')
graph2 = GraphHandler.graph_converter(pattern)
query = GraphHandler.max_subgraph(graph2)
GraphHandler.draw_graph(query, direction='c')


def test(filename, loss_atom):
    cell = CrystalParser.parse_res('test/' + filename)
    target = GraphHandler.graph_converter(cell)
    # target = GraphHandler.max_subgraph(graph)
    # GraphHandler.draw_graph(target, direction='a')
    # GraphHandler.draw_graph(target, direction='b')
    GraphHandler.draw_graph(target, direction='c')
    print('test:'+filename)
    print('match_1:')
    start = time.process_time()
    result1 = MatchRater.match_1(target, query, loss_atom)
    end = time.process_time()
    if result1:
        min_rmsd = 10000
        best_result = None
        for i in result1:
            rmsd = MatchRater.rmsd(i)
            if rmsd < min_rmsd:
                min_rmsd = rmsd
                best_result = i
        print('rmsd %.2f' % min_rmsd)
        GraphHandler.draw_graph_highlight(target, best_result)
    print('time=%.2f s' % (end - start))
    print('match_2:')
    start = time.process_time()
    result2 = MatchRater.match_2(target, query, loss_atom)
    end = time.process_time()
    if result2:
        min_rmsd = 10000
        best_result = None
        for i in result2:
            rmsd = MatchRater.rmsd(i)
            if rmsd < min_rmsd:
                min_rmsd = rmsd
                best_result = i
        print('rmsd %.2f' % min_rmsd)
        GraphHandler.draw_graph_highlight(target, best_result)
    print('time=%.2f s' % (end - start))


'''test('test-Q1.res', 10)
test('test-Q2.res', 10)
test('test-S1.res', 10)
test('test+Qinben.res', 10)'''
test('c21_origin.res', 5)
