import sys

from PySide2.QtWidgets import QApplication

from gui.gui import MainGui

if __name__ == "__main__":
    app = QApplication(sys.argv)
    scrWindow = MainGui()
    scrWindow.showFullScreen()
    # scrWindow.show()
    sys.exit(app.exec_())
