from .tabs import *
from .wrapper import *
from .libs import *


class MainUI(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle('CrystalTool')
        self.tab = QTabWidget()
        self.tabhkleditor = QWidget()
        self.tabhklsolver = HklSolver()
        self.tabresmatcher = ResMatcher()
        self.tabmatchresult = QWidget()
        self.tabmatchdetail = QWidget()
        self.tab.addTab(self.tabhkleditor, 'HKL编辑器')
        self.tab.addTab(self.tabhklsolver, 'HKL求解器')
        self.tab.addTab(self.tabresmatcher, 'RES匹配器')
        self.tab.addTab(self.tabmatchresult, '匹配结果')
        self.tab.addTab(self.tabmatchdetail, '匹配结果详情')
        self.hkleditor = HklEditor()
        self.matchresult = MatchResult()
        self.matchdetail = MatchDetail()
        self.hkleditor.setupUi(self.tabhkleditor)
        self.matchresult.setupUi(self.tabmatchresult)
        self.matchdetail.setupUi(self.tabmatchdetail)
        self.setCentralWidget(self.tab)
        pass


