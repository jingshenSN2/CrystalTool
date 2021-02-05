from PyQt5.QtWidgets import QWidget, QGridLayout, QRadioButton, QTextEdit, QLineEdit, QComboBox, QFormLayout, \
    QButtonGroup


class ParameterUI(QWidget):

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.widget = QWidget()
        self.layout = QFormLayout()

        self.rb = QRadioButton(self.widget)
        self.rb.setAutoExclusive(False)
        self.cbb_mla = QComboBox(self.widget)
        self.cbb_mla.addItems([str(i) for i in range(11)])
        self.cbb_msbg = QComboBox(self.widget)
        self.cbb_msbg.addItems(['10','20','50','100','200','500','1000'])

        self.layout.addRow('保留骨架', self.rb)
        self.layout.addRow('最大删除原子数', self.cbb_mla)
        self.layout.addRow('最大子结构数', self.cbb_msbg)

    def keep_skeleton(self):
        return self.rb.isChecked()

    def get_max_loss_atom(self):
        return int(self.cbb_mla.currentText())

    def get_max_subgraph(self):
        return int(self.cbb_msbg.currentText())

