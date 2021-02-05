from PyQt5.QtWidgets import QWidget, QHBoxLayout, QTableWidget, QAbstractItemView


class ResultTableUI(QWidget):

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.layout = QHBoxLayout()
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setRowCount(6)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setHorizontalHeaderLabels(['res文件','匹配成功','匹配上原子数','加权匹配比例','坐标匹配误差'])
        self.layout.addWidget(self.table)
