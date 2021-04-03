from .libs import *
from .wrapper import *


@singleton
class MainUI(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle('CrystalTool')
        self.tab = QTabWidget()
        self.tabhkleditor = HklEditor()
        self.tabhklsolver = HklSolver()
        self.tabresmatcher = ResMatcher()
        self.tabmatchresult = MatchResult()
        self.tabmatchdetail = MatchDetail()
        self.tab.addTab(self.tabhkleditor, 'HKL编辑器')
        self.tab.addTab(self.tabhklsolver, 'HKL求解器')
        self.tab.addTab(self.tabresmatcher, 'RES匹配器')
        self.tab.addTab(self.tabmatchresult, '匹配结果')
        self.tab.addTab(self.tabmatchdetail, '匹配结果详情')
        self.setCentralWidget(self.tab)
