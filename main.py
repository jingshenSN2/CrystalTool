import sys

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication

from crystaltoolgui import MainUI

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon('crystaltoolgui/icon.png'))
    window = MainUI()
    window.show()
    sys.exit(app.exec_())
