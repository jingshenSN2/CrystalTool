from PyQt5.QtWidgets import QWidget, QPushButton, QFileDialog, QGridLayout, QLabel, QFormLayout, QFrame


class FileInputUI(QWidget):

    def __init__(self):
        super().__init__()
        self.init_ui()
        self.has_res = False
        self.res_files = []
        self.has_pdb = False
        self.pdb_file = ''

    def init_ui(self):
        self.widget = QWidget()
        self.layout = QFormLayout()

        self.lb_res = QLabel('未选择文件,请选择衍射res文件', self.widget)
        self.lb_res.setStyleSheet("color:red")
        self.lb_pdb = QLabel('未选择文件,请选择待搜索pdb文件', self.widget)
        self.lb_pdb.setStyleSheet("color:red")
        self.bt_res = QPushButton('+', self.widget)
        self.bt_pdb = QPushButton('+', self.widget)

        self.layout.addRow(self.bt_res, self.lb_res)
        self.layout.addRow(self.bt_pdb, self.lb_pdb)

        self.bt_res.clicked.connect(self.open_res)
        self.bt_pdb.clicked.connect(self.open_pdb)

    def open_res(self):
        self.res_files, success = QFileDialog.getOpenFileNames(self,
                                                               '选择衍射结构的res文件', './', 'Res Files (*.res)')
        if success:
            self.lb_res.setText('已选%d个文件' % len(self.res_files))
            self.lb_res.setStyleSheet("color:black")
            self.has_res = True

    def open_pdb(self):
        self.pdb_file, success = QFileDialog.getOpenFileName(self,
                                                             '选择待搜索结构的pdb文件', './', 'Pdb Files (*.pdb)')
        if success:
            self.lb_pdb.setText(self.pdb_file.split('/')[-1])
            self.lb_pdb.setStyleSheet("color:black")
            self.has_pdb = True
