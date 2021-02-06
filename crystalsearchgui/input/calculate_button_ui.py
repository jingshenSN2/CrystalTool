from PyQt5.QtWidgets import QWidget, QFormLayout, QPushButton


class CalculateButtonUI(QWidget):

    def __init__(self, main):
        super().__init__()
        self.main = main
        self.init_ui()

    def init_ui(self):
        self.widget = QWidget()
        self.layout = QFormLayout()

        self.bt_match = QPushButton('开始匹配', self.widget)
        self.bt_coord_error = QPushButton('计算坐标匹配', self.widget)

        self.layout.addRow('', self.bt_match)
        self.layout.addRow('', self.bt_coord_error)

        self.bt_match.clicked.connect(self.match)
        self.bt_coord_error.clicked.connect(self.cal_coord_error)

    def match(self):
        self.main.match()

    def cal_coord_error(self):
        self.main.cal_coord_error()
