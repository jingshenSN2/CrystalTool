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

        self.layout.addRow('', self.bt_match)
        self.bt_match.clicked.connect(self.match)

    def match(self):
        self.main.match()
