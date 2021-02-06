from PyQt5.QtWidgets import QWidget, QHBoxLayout, QTableWidget, QAbstractItemView, QTableWidgetItem


class ResultTableUI(QWidget):

    def __init__(self):
        super().__init__()
        self.init_ui()
        self.results = None

    def init_ui(self):
        self.layout = QHBoxLayout()
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setRowCount(6)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setHorizontalHeaderLabels(['res文件', '匹配成功', '匹配上原子数', '加权匹配比例', '坐标匹配误差'])
        self.layout.addWidget(self.table)

    def updateResults(self, results):
        self.results = results
        l = len(results)
        self.table.clearContents()
        self.table.setRowCount(l)
        for i in range(l):
            r = results[i]
            target = r.target.name
            is_match = '是' if r.is_matched else '否'
            self.table.setItem(i, 0, QTableWidgetItem(target))
            self.table.setItem(i, 1, QTableWidgetItem(is_match))
