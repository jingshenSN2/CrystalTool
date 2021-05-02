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
        self.tab.addTab(self.tabmatchdetail, '可视化')
        self.setCentralWidget(self.tab)

    def setEditTab(self):
        self.tab.setCurrentIndex(0)

    def setSolveTab(self):
        self.tab.setCurrentIndex(1)

    def setMatchTab(self):
        self.tab.setCurrentIndex(2)

    def setMatchResultTab(self):
        self.tab.setCurrentIndex(3)

    def setMatchDetailTab(self):
        self.tab.setCurrentIndex(4)
