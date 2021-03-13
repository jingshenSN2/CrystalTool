from PyQt5.QtWidgets import QWidget, QPushButton, QFileDialog, QLabel, QFormLayout

from crystalsearchgui import MainUI


class MatchUI(QWidget):

    def __init__(self, main: MainUI):
        super().__init__()
        self.init_ui()
        self.main = main
        self.has_hkl = False
        self.has_ins = False
        self.has_res = False
        self.has_pdb = False
        self.hkl_files = []
        self.ins_file = ''
        self.res_files = []
        self.pdb_file = ''

    def init_ui(self):
        self.widget = QWidget()
        self.layout = QFormLayout()

        self.lb_res = QLabel('未选择文件,请选择衍射res文件', self.widget)
        self.lb_res.setStyleSheet("color:red")
        self.lb_pdb = QLabel('未选择文件,请选择待搜索pdb文件', self.widget)
        self.lb_pdb.setStyleSheet("color:red")
        self.bt_match = QPushButton('开始匹配', self.widget)
        self.bt_match.setToolTip('如果没有RES文件，请先用左侧的求解结构，\n指定HKL和INS文件后，程序会用自带shelxt求解')
        self.lb_match_status = QLabel('', self.widget)

        self.bt_res = QPushButton('+', self.widget)
        self.bt_pdb = QPushButton('+', self.widget)

        self.layout.addRow(self.bt_res, self.lb_res)
        self.layout.addRow(self.bt_pdb, self.lb_pdb)
        self.layout.addRow(self.bt_match, self.lb_match_status)

        self.bt_res.clicked.connect(self.open_res)
        self.bt_pdb.clicked.connect(self.open_pdb)
        self.bt_match.clicked.connect(self.match)

    def match(self):
        if not self.has_res_files():
            self.set_text('缺失文件')
            return
        self.set_text('正在匹配...已完成0/%d' % len(self.res_files))
        self.main.match()
        self.set_text('匹配完成')

    def set_process(self, process: int):
        res_count = len(self.res_files)
        if res_count == 0:
            return
        self.set_text('正在匹配...已完成%d/%d' % (process, res_count))

    def set_text(self, text: str):
        self.lb_match_status.setText(text)
        self.lb_match_status.repaint()

    def open_res(self):
        self.res_files, success = QFileDialog.getOpenFileNames(self, '选择衍射结构的RES文件', './', 'Res Files (*.res)')
        if success:
            self.lb_res.setText('已选%d个文件(鼠标悬停以查看)' % len(self.res_files))
            self.lb_res.setToolTip('\n'.join(self.res_files))
            self.lb_res.setStyleSheet("color:black")
            self.has_res = True

    def open_pdb(self):
        self.pdb_file, success = QFileDialog.getOpenFileName(self, '选择待搜索结构的PDB文件', './', 'Pdb Files (*.pdb)')
        if success:
            self.lb_pdb.setText('已选%s' % self.pdb_file.split('/')[-1])
            self.lb_pdb.setToolTip(self.pdb_file)
            self.lb_pdb.setStyleSheet("color:black")
            self.has_pdb = True

    def has_res_files(self):
        return self.has_res and self.has_pdb

    def get_res_files(self):
        return self.res_files

    def get_pdb_file(self):
        return self.pdb_file
