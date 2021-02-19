from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QTableWidget, QAbstractItemView, QTableWidgetItem, QPushButton


class ResultTableUI(QWidget):

    def __init__(self):
        super().__init__()
        self.init_ui()
        self.results = None
        self.bt_list = []

    def init_ui(self):
        self.layout = QHBoxLayout()
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setRowCount(6)
        self.table.setSortingEnabled(True)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setHorizontalHeaderLabels(['res文件', '匹配成功', '最大匹配原子数', '最大加权匹配比例', '最小坐标匹配误差', ''])
        self.layout.addWidget(self.table)

    def updateResults(self, results):
        self.results = results
        l = len(results)
        self.bt_list.clear()
        self.table.clearContents()
        self.table.setRowCount(l)
        for i in range(l):
            r = results[i]
            target = QTableWidgetItem()
            is_match = QTableWidgetItem()
            max_nm = QTableWidgetItem()
            max_rwm = QTableWidgetItem()
            min_mse = QTableWidgetItem()
            target.setText(r.target.name)
            is_match.setText('是' if r.is_matched else '否')
            max_nm.setData(Qt.DisplayRole, r.best_feature[0] if r.is_matched else 0)
            max_rwm.setText('%.1f%%' % (r.best_feature[1] * 100) if r.is_matched else '')
            min_mse.setText('%.2f' % (r.best_feature[2]) if r.is_matched else '')
            bt = QPushButton('查看')
            # bt.clicked.connect(lambda x: self.clickButton(i))
            self.bt_list.append(bt)

            self.table.setItem(i, 0, target)
            self.table.setItem(i, 1, is_match)
            self.table.setItem(i, 2, max_nm)
            self.table.setItem(i, 3, max_rwm)
            self.table.setItem(i, 4, min_mse)
            self.table.setCellWidget(i, 5, bt)

    def clickButton(self, index):
        print(self.results[index].target.name)
