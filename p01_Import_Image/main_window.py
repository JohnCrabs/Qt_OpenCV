import sys
from lib.image_io import *
from p01_Import_Image.ui_main import *

from PyQt5.Qt import (Qt, QDir, QLabel, QImage, QFileDialog)

class Window:
    def __init__(self):
        # ------------------------
        # Set flags
        # ------------------------
        self.UP = True
        self.DOWN = False

        self.ALL_IMG_FORMAT = "All Supported (*.jpg *.jpeg *.jpe *.png *.bmp *.tif *.tiff " \
                              "*.dib *.pbm *.pgm *.ppm *.sr *.ras)"
        self.JPG_FORMAT = "JPG (*.jpg *.jpeg *.jpe)"
        self.PNG_FORMAT = "PNG (*.png)"
        self.BMP_FORMAT = "BMP (*.bmp)"
        self.TIF_FORMAT = "TIFF (*.tif *.tiff)"
        self.DIB_FORMAT = "DIB (*.dib)"
        self.PBM_FORMAT = "PBM (*.pbm)"
        self.PGM_FORMAT = "PGM (*.pgm)"
        self.PPM_FORMAT = "PPM (*.ppm)"
        self.SR__FORMAT = "SR (*.sr)"
        self.RAS_FORMAT = "RAS (*.ras)"
        self.DD = ";;"

        self.IMG_FILTER = self.ALL_IMG_FORMAT + self.DD + self.JPG_FORMAT + self.DD + self.PNG_FORMAT + self.DD + \
                          self.BMP_FORMAT + self.DD + self.TIF_FORMAT + self.DD + self.DIB_FORMAT + self.DD + \
                          self.PBM_FORMAT + self.DD + self.PGM_FORMAT + self.DD + self.PPM_FORMAT + self.DD + \
                          self.SR__FORMAT + self.DD + self.RAS_FORMAT

        self.DIALOG_FLAG = QFileDialog.DontUseNativeDialog

        # ------------------------
        # Flags Section ends here
        # ---------------------------------------------------------------------------------------------------------- #
        # ------------------------
        # Set class items
        # ------------------------
        self.q_img = QImage()

        self.img = Image()
        self.is_img_Open = False

        # ------------------------
        # Class items ends here
        # ---------------------------------------------------------------------------------------------------------- #
        # ------------------------
        # Set up the ui
        # ------------------------
        self.app = QtWidgets.QApplication(sys.argv)
        self.ui = Ui_MainWindow()
        self.MainWindow = QtWidgets.QMainWindow()
        self.ui.setupUi(self.MainWindow)
        # ------------------------
        # Setting up ends here
        # ---------------------------------------------------------------------------------------------------------- #
        # ------------------------
        # Actions list starts here
        # ------------------------
        self.ui.actionOpen.triggered.connect(self.open)
        self.ui.actionSave.triggered.connect(self.save)
        self.ui.actionExit.triggered.connect(self.exit_window)
        # ------------------------
        # Actions list ends here
        # ---------------------------------------------------------------------------------------------------------- #
        # ------------------------
        # Main loop and exit app
        # ------------------------
        self.MainWindow.show()
        sys.exit(self.app.exec_())
        # ------------------------
        # END OF APPLICATION
        # ---------------------------------------------------------------------------------------------------------- #

    def open_img_path(self):
        """
        Open the dialog and take the path.
        :return: True/False, path_string/empty_string
        """
        file_dialog = QFileDialog()
        f_path = file_dialog.getOpenFileName(parent=None,
                                             caption="Open Image",
                                             directory=QDir.homePath(),
                                             filter=self.IMG_FILTER,
                                             initialFilter="",
                                             options=self.DIALOG_FLAG)[0]
        if f_path:
            return True, f_path
        return False, ""

    def open(self):
        """
        Open an image and create a QImage() item for view.
        :return: Nothing
        """
        self.is_img_Open, f_path = self.open_img_path()  # Open dialog and take the path
        if self.is_img_Open:  # Check if user gave a path or not (aka pressed "Open" or "Cancel"
            self.img.open_image_from(f_path)  # Open image
            self.img.print_img_info()  # Print info for debugging
            # Transform Image() to QImage()
            bytes_per_line = 3 * self.img.width
            self.q_img = QImage(self.img.img_RGB(), self.img.width, self.img.height,
                                bytes_per_line, QImage.Format_RGB888)
            self.ui.actionSave.setEnabled(self.UP)  # Enable save (currently not so useful)

    def save(self):
        print("save")

    def exit_window(self):
        """
        Signal exit application
        :return: Nothing
        """
        self.MainWindow.close()  # Close The window
