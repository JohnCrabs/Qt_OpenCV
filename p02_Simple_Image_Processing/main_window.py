import sys

from lib.image_io import *
from lib.image_processing import *

from helping_dialogs.color_processing import *

from p02_Simple_Image_Processing.ui_main import *

from PyQt5.Qt import (Qt, QDir, QSize, QTimer, QImage, QPixmap, QFileDialog)


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
        self.Q_ASPECT_RATIO = Qt.KeepAspectRatio
        # ------------------------
        # Flags Section ends here
        # ---------------------------------------------------------------------------------------------------------- #
        # ------------------------
        # Set class items
        # ------------------------
        self.q_img = QImage()
        self.img_view_timer = QTimer()

        self.img = Image()
        self.img_proc = ImageProcessing()
        self.is_img_Open = False
        self.is_img_Save = False

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

        self.DialogColor = QtWidgets.QDialog()
        self.ui_color = Ui_DialogColoring()
        self.ui_color.setupUi(self.DialogColor)
        # ------------------------
        # Setting up ends here
        # ---------------------------------------------------------------------------------------------------------- #
        # ------------------------
        # Actions list starts here
        # ------------------------
        self.ui.actionOpen.triggered.connect(self.open)
        self.ui.actionSave.triggered.connect(self.save)
        self.ui.actionSave_as.triggered.connect(self.save_as)
        self.ui.actionExit.triggered.connect(self.exit_window)

        self.ui.actionLight_Contrast.triggered.connect(self.open_color_light_dialog)

        self.ui.light_spinbox.valueChanged.connect(self.light_spinbox_value_changed)
        self.ui.contrast_spinbox.valueChanged.connect(self.contrast_spinbox_value_changed)

        self.img_view_timer.timeout.connect(self.update_img_view)
        self.img_view_timer.start(250)

        self.ui_color.l_radio_all_bands.clicked.connect(self.dialog_color_light_all_checked)
        self.ui_color.l_radio_rgb.clicked.connect(self.dialog_color_light_rgb_checked)
        self.ui_color.c_radio_all_bands.clicked.connect(self.dialog_color_contrast_all_checked)
        self.ui_color.c_radio_rgb.clicked.connect(self.dialog_color_contrast_rgb_checked)

        self.ui_color.cancel_button.clicked.connect(self.dialog_color_cancel)
        self.ui_color.compute_button.clicked.connect(self.dialog_color_compute)

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

    def enable_options(self):
        # Enable Menu/Actions
        self.ui.actionSave.setEnabled(self.UP)
        self.ui.actionSave_as.setEnabled(self.UP)
        self.ui.menuFilters.setEnabled(self.UP)
        self.ui.menuTransformations.setEnabled(self.UP)

        # Enable Spinbox
        self.ui.light_spinbox.setEnabled(self.UP)
        self.ui.light_spinbox.setValue(0)
        self.ui.contrast_spinbox.setEnabled(self.UP)
        self.ui.contrast_spinbox.setValue(1.0)

    def update_img_view(self):
        if self.is_img_Open:
            #print(self.ui.img_view.size())
            width = self.ui.img_view.width()
            height = self.ui.img_view.height()
            if self.img.width < width or self.img.height < height:
                width = self.q_img.width()
                height = self.q_img.height()
            size = QSize(width, height)
            pixmap = QPixmap()
            pixmap = pixmap.fromImage(self.q_img)
            pixmap = pixmap.scaled(size, self.Q_ASPECT_RATIO)
            self.ui.img_view.setPixmap(pixmap)
            self.ui.img_view.show()

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

    def save_img_path(self):
        """
        Open the dialog and take the path.
        :return: True/False, path_string/empty_string
        """
        file_dialog = QFileDialog()
        f_path = file_dialog.getSaveFileName(parent=None,
                                             caption="Save Image as",
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
            self.img.set_img_tmp(self.img.img)
            self.q_img = QImage(self.img.img_tmp_RGB(), self.img.width, self.img.height,
                                bytes_per_line, QImage.Format_RGB888)
            self.enable_options()  # Enable all image processing utilities

    def save(self):
        """
        Save an image to a given path. (If image has already been saved to a path reuses this path)
        :return: Nothing
        """
        if not self.is_img_Save:
            self.save_as()  # Open dialog and take the path
        else:  # Check if user gave a path or not (aka pressed "Open" or "Cancel")
            self.img.set_img_from_img_tmp()
            self.img.save_image()

    def save_as(self):
        """
        Save an image to a given path. (Asks every time the user to specify a path)
        :return: Nothing
        """
        self.is_img_Save, f_path = self.save_img_path()  # Open dialog and take the path
        if self.is_img_Save:  # Check if user gave a path or not (aka pressed "Open" or "Cancel"
            self.img.set_img_from_img_tmp()
            self.img.save_image_as(f_path)

    def exit_window(self):
        """
        Signal exit application
        :return: Nothing
        """
        self.MainWindow.close()  # Close The window

    def light_spinbox_value_changed(self):
        self.img_proc.set_light(self.ui.light_spinbox.value())
        self.ui_color.l_spin_light_for_all.setValue(self.ui.light_spinbox.value())
        img_rgb = self.img.img_RGB()
        img_rgb = self.img_proc.compute_light_contrast(img_rgb)
        self.img.set_img_tmp(self.img.img_RGB2BGR(img_rgb))
        bytes_per_line = 3 * self.img.width
        self.q_img = QImage(self.img.img_tmp_RGB(), self.img.width, self.img.height,
                            bytes_per_line, QImage.Format_RGB888)

    def contrast_spinbox_value_changed(self):
        self.img_proc.set_contrast(self.ui.contrast_spinbox.value())
        self.ui_color.c_contrast_for_all.setValue(self.ui.contrast_spinbox.value())
        img_rgb = self.img.img_RGB()
        img_rgb = self.img_proc.compute_light_contrast(img_rgb)
        self.img.set_img_tmp(self.img.img_RGB2BGR(img_rgb))
        bytes_per_line = 3 * self.img.width
        self.q_img = QImage(self.img.img_tmp_RGB(), self.img.width, self.img.height,
                            bytes_per_line, QImage.Format_RGB888)

    def open_color_light_dialog(self):
        self.DialogColor.show()

    def dialog_color_cancel(self):
        self.DialogColor.close()

    def dialog_color_light_all_checked(self):
        self.ui_color.l_all_bands_widget.setEnabled(self.UP)
        self.ui_color.l_rgb_widget.setEnabled(self.DOWN)

    def dialog_color_light_rgb_checked(self):
        self.ui_color.l_all_bands_widget.setEnabled(self.DOWN)
        self.ui_color.l_rgb_widget.setEnabled(self.UP)
        self.img_proc.set_default_light_contrast_rgb()

    def dialog_color_contrast_all_checked(self):
        self.ui_color.c_all_bands_widget.setEnabled(self.UP)
        self.ui_color.c_rgb_widget.setEnabled(self.DOWN)

    def dialog_color_contrast_rgb_checked(self):
        self.ui_color.c_all_bands_widget.setEnabled(self.DOWN)
        self.ui_color.c_rgb_widget.setEnabled(self.UP)

    def dialog_color_compute(self):
        if self.ui_color.l_radio_all_bands.isChecked():
            self.img_proc.set_light(self.ui_color.l_spin_light_for_all.value())
            self.ui_color.l_spin_red.setValue(self.ui_color.l_spin_light_for_all.value())
            self.ui_color.l_spin_green.setValue(self.ui_color.l_spin_light_for_all.value())
            self.ui_color.l_spin_blue.setValue(self.ui_color.l_spin_light_for_all.value())
            self.ui.light_spinbox.setValue(self.ui_color.l_spin_light_for_all.value())
            img_rgb = self.img.img_RGB()
            img_rgb = self.img_proc.compute_light_contrast(img_rgb)
            self.img.set_img_tmp(self.img.img_RGB2BGR(img_rgb))

        if self.ui_color.c_radio_all_bands.isChecked():
            self.img_proc.set_contrast(self.ui.contrast_spinbox.value())
            self.ui.contrast_spinbox.setValue(self.ui_color.c_contrast_for_all.value())
            self.ui_color.c_double_spin_red.setValue(self.ui_color.c_contrast_for_all.value())
            self.ui_color.c_double_spin_green.setValue(self.ui_color.c_contrast_for_all.value())
            self.ui_color.c_double_spin_blue.setValue(self.ui_color.c_contrast_for_all.value())
            img_rgb = self.img.img_RGB()
            img_rgb = self.img_proc.compute_light_contrast(img_rgb)
            self.img.set_img_tmp(self.img.img_RGB2BGR(img_rgb))

        if self.ui_color.l_radio_rgb.isChecked() or self.ui_color.c_radio_rgb.isChecked():
            self.img_proc.set_light_contrast_rgb(self.ui_color.l_spin_red.value(), self.ui_color.l_spin_green.value(),
                                                 self.ui_color.l_spin_blue.value(),
                                                 self.ui_color.c_double_spin_red.value(),
                                                 self.ui_color.c_double_spin_green.value(),
                                                 self.ui_color.c_double_spin_blue.value())
            img_rgb = self.img.img_RGB()
            img_rgb = self.img_proc.compute_light_contrast_per_channel(img_rgb)
            self.img.set_img_tmp(self.img.img_RGB2BGR(img_rgb))
            bytes_per_line = 3 * self.img.width
            self.q_img = QImage(self.img.img_tmp_RGB(), self.img.width, self.img.height,
                                bytes_per_line, QImage.Format_RGB888)
            self.img_proc.compute_light_contrast_per_channel(self.img.img_tmp)

        bytes_per_line = 3 * self.img.width
        self.q_img = QImage(self.img.img_tmp_RGB(), self.img.width, self.img.height,
                            bytes_per_line, QImage.Format_RGB888)