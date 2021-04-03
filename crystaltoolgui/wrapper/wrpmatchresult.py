from ..libs import *
from ..tabs import Ui_tabmatchresult


@singleton
class MatchResult(QWidget):

    def __init__(self):
        super().__init__()
        self.ui = Ui_tabmatchresult()
        self.ui.setupUi(self)
        self.results = None
        self.report_feats = None
        self.header = None
        self.ui.tV_results.doubleClicked.connect(self.show_detail)

    def update_result(self, results: list, report_feats: list):
        self.results = results
        self.report_feats = report_feats
        result_len = len(results)
        self.header = ['res文件', '匹配成功']
        self.header.extend(report_feats)
        sim = QStandardItemModel()
        sim.setHorizontalHeaderLabels(self.header)
        sim.setRowCount(result_len)

        def add_one_row(sim, result, row_index):
            row_data = [result.target.name, '是' if result.is_matched else '否']
            for feat in self.report_feats:
                if feat == 'Nm':
                    row_data.append('%d' % result.best_feature[feat])
                else:
                    row_data.append('%.1f%%' % (result.best_feature[feat] * 100))
            for i in range(len(row_data)):
                sim.setData(sim.index(row_index, i), row_data[i])

        idx = 0
        for r in self.results:
            add_one_row(sim, r, idx)
            idx += 1
        self.ui.tV_results.setModel(sim)

    def show_detail(self, mi):
        row_index = mi.row()
        sim = QStandardItemModel()
        sim.setHorizontalHeaderLabels(self.header[2:])
        if not self.results[row_index].is_matched:
            self.ui.tV_results_detail.setModel(sim)
            return
        detail = self.results[row_index].results
        sim.setRowCount(len(detail))

        def add_one_detail(sim, result, row_index):
            row_data = []
            for feat in self.report_feats:
                if feat == 'Nm':
                    row_data.append('%d' % result[feat])
                else:
                    row_data.append('%.1f%%' % (result[feat] * 100))
            for i in range(len(row_data)):
                sim.setData(sim.index(row_index, i), row_data[i])

        idx = 0
        for r in detail:
            add_one_detail(sim, r, idx)
            idx += 1
        self.ui.tV_results_detail.setModel(sim)
