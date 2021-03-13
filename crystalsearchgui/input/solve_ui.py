from PyQt5.QtWidgets import QWidget, QPushButton, QFileDialog, QLabel, QFormLayout

from crystalsearchgui import MainUI


class SolveUI(QWidget):

    def __init__(self, main: MainUI):
        super().__init__()
        self.init_ui()
        self.main = main
        self.has_hkl = False
        self.has_ins = False
        self.hkl_files = []
        self.ins_file = ''

    def init_ui(self):
        self.widget = QWidget()
        self.layout = QFormLayout()

        self.lb_hkl = QLabel('未选择文件,请选择衍射hkl文件', self.widget)
        self.lb_hkl.setStyleSheet("color:red")
        self.lb_ins = QLabel('未选择文件,请选择衍射ins文件', self.widget)
        self.lb_ins.setStyleSheet("color:red")
        self.bt_solve = QPushButton('求解结构', self.widget)
        self.bt_solve.setToolTip('如果已有RES文件，请跳过此部分')
        self.lb_solve_status = QLabel('', self.widget)

        self.bt_hkl = QPushButton('+', self.widget)
        self.bt_ins = QPushButton('+', self.widget)

        self.layout.addRow(self.bt_hkl, self.lb_hkl)
        self.layout.addRow(self.bt_ins, self.lb_ins)
        self.layout.addRow(self.bt_solve, self.lb_solve_status)

        self.bt_hkl.clicked.connect(self.open_hkl)
        self.bt_ins.clicked.connect(self.open_ins)
        self.bt_solve.clicked.connect(self.solve)

    def solve(self):
        if not self.has_hkl_files():
            self.set_text('缺失文件')
            return
        self.set_text('正在求解...')
        self.main.solve()
        self.set_text('求解完成')

    def set_process(self, process: int):
        hkl_count = len(self.hkl_files)
        if hkl_count == 0:
            return
        self.set_text('正在求解...已完成%d/%d' % (process, hkl_count))

    def set_text(self, text: str):
        self.lb_solve_status.setText(text)
        self.lb_solve_status.repaint()

    def open_hkl(self):
        self.hkl_files, success = QFileDialog.getOpenFileNames(self, '选择衍射结构的HKL文件', './', 'Hkl Files (*.hkl)')
        if success:
            self.lb_hkl.setText('已选%d个文件(鼠标悬停以查看)' % len(self.hkl_files))
            self.lb_hkl.setToolTip('\n'.join(self.hkl_files))
            self.lb_hkl.setStyleSheet("color:black")
            self.has_hkl = True

    def open_ins(self):
        self.ins_file, success = QFileDialog.getOpenFileName(self, '选择待搜索结构的INS文件', './', 'Ins Files (*.ins)')
        if success:
            self.lb_ins.setText('已选%s' % self.ins_file.split('/')[-1])
            self.lb_ins.setToolTip(self.ins_file)
            self.lb_ins.setStyleSheet("color:black")
            self.has_ins = True

    def has_hkl_files(self):
        return self.has_hkl and self.has_ins

    def get_hkl_files(self):
        return self.hkl_files

    def get_ins_file(self):
        return self.ins_file
