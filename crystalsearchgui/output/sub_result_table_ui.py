import matplotlib.pyplot as plt
from ..libs import *
from crystalsearch import saveToRes


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
        self.table.setColumnWidth(0, 160)
        self.table.setColumnWidth(1, 160)
        self.table.setColumnWidth(2, 160)
        self.table.setColumnWidth(3, 400)
        self.table.setSortingEnabled(True)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setHorizontalHeaderLabels(['匹配上原子数', '加权匹配比例', '坐标匹配残差', '操作'])

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

    def generate_button(self, pair: dict):
        button = QPushButton('查看图片')
        button_3d = QPushButton('查看3d图')
        button_res = QPushButton('另存为')
        bt_widget = QWidget()
        hLayout = QHBoxLayout()
        hLayout.addWidget(button)
        hLayout.addWidget(button_3d)
        hLayout.addWidget(button_res)
        hLayout.setContentsMargins(5, 2, 5, 2)
        bt_widget.setLayout(hLayout)
        button.clicked.connect(lambda: self.plot_result(self.result, pair))
        button_3d.clicked.connect(lambda: self.plot_result_3d(self.result, pair))
        button_res.clicked.connect(lambda: self.save_res(self.result, pair))
        return bt_widget

    def plot_result(self, result, pair: dict):
        plt.subplot(121)
        result.target.draw_graph(highlight=pair.keys(), rotation=self.result.rotation)
        plt.subplot(122)
        result.query.draw_graph(highlight=pair.values())
        plt.show()

    def plot_result_3d(self, result, pair: dict):
        result.target.draw_3d_graph(highlight=pair)
        plt.show()

    def save_res(self, result, pair: dict):
        output_file, success = QFileDialog.getSaveFileName(self, '选择新的RES保存路径', './', 'Res Files (*.res)')
        if success:
            saveToRes(output_file, result, pair)
