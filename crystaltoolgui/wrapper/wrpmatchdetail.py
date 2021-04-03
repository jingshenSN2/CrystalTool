from ..libs import *
from ..tabs import Ui_tabmatchdetail


@singleton
class MatchDetail(QWidget):

    def __init__(self):
        super().__init__()
        self.ui = Ui_tabmatchdetail()
        self.ui.setupUi(self)
