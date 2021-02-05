from PyQt5.QtWidgets import QWidget, QGridLayout, QRadioButton, QTextEdit, QLineEdit, QComboBox, QFormLayout, \
    QButtonGroup


class ResultParameterUI(QWidget):

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.widget = QWidget()
        self.layout = QFormLayout()

        self.rb = QRadioButton(self.widget)
        self.rb.setAutoExclusive(False)
        self.cbb = QComboBox(self.widget)
        self.cbb.addItems(['匹配原子数','加权匹配比例','坐标匹配误差'])

        self.layout.addRow('只显示最佳结果', self.rb)
        self.layout.addRow('最佳结果基于', self.cbb)

    def only_best_result(self):
        return self.rb.isChecked()

    def get_best_feature(self):
        return self.cbb.currentText()
