from PyQt5.QtCore import QRect
from PyQt5.QtWidgets import QWidget, QApplication, QGridLayout, QPushButton, QHBoxLayout, QLabel, QFormLayout

from crystalsearch.run import run
from crystalsearchgui.input.calculate_button_ui import CalculateButtonUI
from crystalsearchgui.input.file_input_ui import FileInputUI
from crystalsearchgui.input.parameter_ui import ParameterUI
from crystalsearchgui.output.result_table_ui import ResultTableUI

test_info = '''res文件:
%s
pdb文件:%s
keep_skeleton:%s
最大删除原子数:%d
最大子结构数:%d
只显示最佳结果:%s
最佳结果根据:%s'''


class MainGUI(QWidget):

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setFixedSize(800, 600)
        self.setWindowTitle('电子衍射结构解析评分程序')

        self.layout = QGridLayout(self)
        self.layout.setGeometry(QRect(20, 20, 800, 600))

        self.input_layout = QHBoxLayout(self)
        self.layout.addLayout(self.input_layout, 0, 0)

        self.file_input_ui = FileInputUI()
        self.para_input_ui = ParameterUI()
        self.cal_button_ui = CalculateButtonUI(self)

        self.input_layout.addLayout(self.file_input_ui.layout, 2)
        self.input_layout.addLayout(self.para_input_ui.layout, 1)
        self.input_layout.addLayout(self.cal_button_ui.layout, 1)

        self.output_layout = QHBoxLayout(self)
        self.layout.addLayout(self.output_layout, 1, 0)

        self.result_table_ui = ResultTableUI()
        self.output_layout.addLayout(self.result_table_ui.layout)

        self.test_layout = QFormLayout()
        self.layout.addLayout(self.test_layout, 2, 0)
        self.bt = QPushButton()
        self.bt.clicked.connect(self.show_info)
        self.q = QLabel()
        self.test_layout.addRow(self.bt)
        self.test_layout.addRow(self.q)

    def show_info(self):
        res_f = self.file_input_ui.res_files
        pdb_f = self.file_input_ui.pdb_file
        k = self.para_input_ui.keep_skeleton()
        mla = self.para_input_ui.get_max_loss_atom()
        msb = self.para_input_ui.get_max_subgraph()
        self.q.setText(test_info
                       % ('\n'.join(res_f), pdb_f,
                          k, mla, msb))

    def match(self):
        if not self.file_input_ui.has_files():
            return
        results = run(self.file_input_ui.res_files, self.file_input_ui.pdb_file,
                      self.para_input_ui.keep_skeleton(), self.para_input_ui.get_max_loss_atom(),
                      self.para_input_ui.get_max_subgraph())
        self.result_table_ui.updateResults(results)


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    window = MainGUI()
    window.show()
    sys.exit(app.exec_())
