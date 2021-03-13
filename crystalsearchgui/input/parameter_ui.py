import os

from PyQt5.QtWidgets import QWidget, QRadioButton, QFormLayout, QSpinBox, QPushButton


class ParameterUI(QWidget):

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.widget = QWidget()
        self.layout = QFormLayout()

        self.rb = QRadioButton(self.widget)
        self.rb.setAutoExclusive(False)
        self.rb.setToolTip('解析结构中缺失较多原子导致匹配失败时使用，\n' +
                           '可能得到正确的匹配结果，但匹配时间也会显著增加。\n' +
                           '开启此选项时，建议最大删除原子数不超过4。')
        self.mla = QSpinBox()
        self.mla.setRange(0, 10)
        self.bt_cfg = QPushButton('+')

        self.layout.addRow('使用旧算法', self.rb)
        self.layout.addRow('可缺失原子数', self.mla)
        self.layout.addRow('查看配置文件', self.bt_cfg)

        self.bt_cfg.clicked.connect(self.open_cfg)

    def use_old_algorithm(self):
        return self.rb.isChecked()

    def get_max_loss_atom(self):
        return self.mla.value()

    def open_cfg(self):
        current_path = os.path.dirname(__file__)
        cfg_path = current_path + '/../../crystalsearch/config/atom_properties.json'
        os.system(r'c:\windows\system32\notepad.exe %s' % cfg_path)
