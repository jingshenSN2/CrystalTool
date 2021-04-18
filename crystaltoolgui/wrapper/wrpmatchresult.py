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
        self.selected_result = None
        self.selected_pair = None
        self.ui.tV_results.doubleClicked.connect(self.show_detail)
        self.ui.tV_results_detail.doubleClicked.connect(self.send_to_detail)
        self.ui.pB_result_to_res.clicked.connect(self.to_res)

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
            for j in range(len(row_data)):
                sim.setData(sim.index(row_index, j), row_data[j])
            print('\t'.join(row_data))

        for i in range(result_len):
            add_one_row(sim, self.results[i], i)
        self.ui.tV_results.setModel(sim)

    def show_detail(self, mi):
        row_index = mi.row()
        sim = QStandardItemModel()
        sim.setHorizontalHeaderLabels(self.header[2:])
        self.selected_result = self.results[row_index]
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
            for j in range(len(row_data)):
                sim.setData(sim.index(row_index, j), row_data[j])

        for i in range(len(detail)):
            add_one_detail(sim, detail[i], i)
        self.ui.tV_results_detail.setModel(sim)

    def send_to_detail(self, mi):
        row_index = mi.row()
        self.selected_pair = self.selected_result.results[row_index]['pair']
        from ..main import MainUI
        MainUI().tabmatchdetail.update_and_draw(self.selected_result, self.selected_pair)
        MainUI().tab.setCurrentIndex(4)

    def to_res(self):
        # TODO
        pass
