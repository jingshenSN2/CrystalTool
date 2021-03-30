from ..libs import *
from . import SubResultUI


class ResultTableUI(QWidget):

    def __init__(self):
        super().__init__()
        self.init_ui()
        self.results = None
        self.results_ui = {}

    def init_ui(self):
        self.layout = QHBoxLayout()
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setRowCount(6)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)
        self.table.setSortingEnabled(True)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setHorizontalHeaderLabels(['序号', 'res文件', '匹配成功', '匹配上原子数', '加权匹配比例', '坐标匹配残差', '操作'])
        self.table.verticalHeader().setHidden(True)
        self.layout.addWidget(self.table)

    def updateResults(self, results):
        self.results = results
        self.results_ui = {}
        l = len(results)
        self.table.clearContents()
        self.table.sortByColumn(0, Qt.AscendingOrder)
        self.table.setRowCount(l)
        for i in range(l):
            r = results[i]
            index = QTableWidgetItem()
            target = QTableWidgetItem()
            is_match = QTableWidgetItem()
            max_nm = QTableWidgetItem()
            max_rwm = QTableWidgetItem()
            min_mse = QTableWidgetItem()
            index.setData(Qt.DisplayRole, i + 1)
            target.setText(r.target.name)
            is_match.setText('是' if r.is_matched else '否')
            max_nm.setData(Qt.DisplayRole, r.best_feature[0] if r.is_matched else 0)
            max_rwm.setText('%.1f%%' % (r.best_feature[1] * 100) if r.is_matched else '')
            min_mse.setText('%.2f' % (r.best_feature[2]) if r.is_matched else '')
            self.table.setItem(i, 0, index)
            self.table.setItem(i, 1, target)
            self.table.setItem(i, 2, is_match)
            self.table.setItem(i, 3, max_nm)
            self.table.setItem(i, 4, max_rwm)
            self.table.setItem(i, 5, min_mse)

            if r.is_matched:
                bt_view = self.generate_button(r)
                self.table.setCellWidget(i, 6, bt_view)

    def generate_button(self, result):
        button = QPushButton('查看')
        bt_widget = QWidget()
        hLayout = QHBoxLayout()
        hLayout.addWidget(button)
        hLayout.setContentsMargins(5, 2, 5, 2)
        bt_widget.setLayout(hLayout)
        button.clicked.connect(lambda: self.view_result(result))
        return bt_widget

    def view_result(self, result):
        if result not in self.results_ui:
            self.results_ui[result] = SubResultUI(result)
        self.results_ui[result].show()
