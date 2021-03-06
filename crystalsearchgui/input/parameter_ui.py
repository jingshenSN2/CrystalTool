from PyQt5.QtWidgets import QWidget, QRadioButton, QComboBox, QFormLayout, QSpinBox, QHBoxLayout, QDoubleSpinBox


class ParameterUI(QWidget):

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.widget = QWidget()
        self.layout = QHBoxLayout()

        self.rb = QRadioButton(self.widget)
        self.rb.setAutoExclusive(False)
        self.mla = QSpinBox()
        self.mla.setRange(0, 10)
        self.msbg = QSpinBox()
        self.msbg.setRange(10, 5000)

        self.layout.addRow('保留骨架', self.rb)
        self.layout.addRow('最大删除原子数', self.mla)
        self.layout.addRow('最大子结构数', self.msbg)

    def keep_skeleton(self):
        return self.rb.isChecked()

    def get_max_loss_atom(self):
        return self.mla.value()

    def get_max_subgraph(self):
        return self.msbg.value()
