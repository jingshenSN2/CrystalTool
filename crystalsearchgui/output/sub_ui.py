from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QPushButton, QHBoxLayout, \
    QTableWidget, QTableWidgetItem, QAbstractItemView
import matplotlib.pyplot as plt


class SubResultUI(QWidget):

    def __init__(self, result):
        super().__init__()
        self.result = result
        self.init_ui()

    def init_ui(self):
        self.setFixedSize(1000, 800)
        self.setWindowTitle('%s的所有结果' % self.result.target.name)
        self.layout = QHBoxLayout(self)

        l = len(self.result.results)
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setRowCount(l)
        self.table.setSortingEnabled(True)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setHorizontalHeaderLabels(['匹配上原子数', '加权匹配比例', '坐标匹配误差', '操作'])

        for i in range(l):
            pair, n, wr, ce = self.result.results[i]
            nm = QTableWidgetItem()
            rwm = QTableWidgetItem()
            mse = QTableWidgetItem()
            nm.setData(Qt.DisplayRole, n)
            rwm.setText('%.1f%%' % (wr * 100))
            mse.setText('%.2f' % ce)
            self.table.setItem(i, 0, nm)
            self.table.setItem(i, 1, rwm)
            self.table.setItem(i, 2, mse)
            bt_view = self.generate_button(pair)
            self.table.setCellWidget(i, 3, bt_view)

        self.layout.addWidget(self.table)

    def generate_button(self, pair):
        button = QPushButton('查看图片')
        button_3d = QPushButton('查看3d图')
        bt_widget = QWidget()
        hLayout = QHBoxLayout()
        hLayout.addWidget(button)
        hLayout.addWidget(button_3d)
        hLayout.setContentsMargins(5, 2, 5, 2)
        bt_widget.setLayout(hLayout)
        button.clicked.connect(lambda: self.plot_result(self.result, pair))
        button_3d.clicked.connect(lambda: self.plot_result_3d(self.result, pair))
        return bt_widget

    def plot_result(self, result, pair):
        plt.subplot(121)
        result.target.draw_graph(pair.keys())
        plt.subplot(122)
        result.query.draw_graph(pair.values())
        plt.show()

    def plot_result_3d(self, result, pair):
        result.target.draw_3d_graph(pair)
        plt.show()