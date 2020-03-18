import sys
from p00_Create_Window.ui_main import *


class Window:
    def __init__(self):
        # Set flags
        self.UP = True
        self.DOWN = False

        # Set up the ui
        self.app = QtWidgets.QApplication(sys.argv)
        self.ui = Ui_MainWindow()
        self.MainWindow = QtWidgets.QMainWindow()
        self.ui.setupUi(self.MainWindow)

        # Actions list starts here
        # ------------------------
        self.ui.actionOpen.triggered.connect(self.open)
        self.ui.actionSave.triggered.connect(self.save)
        self.ui.actionExit.triggered.connect(self.exit_window)

        # Actions list ends here
        # ------------------------
        self.MainWindow.show()
        sys.exit(self.app.exec_())

    def open(self):
        print("open")
        self.ui.actionSave.setEnabled(self.UP)

    def save(self):
        print("save")

    def exit_window(self):
        self.MainWindow.close()  # Close The window
