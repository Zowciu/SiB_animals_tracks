from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtGui import QColor
import sys
import os
from detection import draw_bounding_box, return_image


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1200, 655)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.get_button = QtWidgets.QPushButton(self.centralwidget)
        self.get_button.setGeometry(QtCore.QRect(195, 50, 120, 40))
        self.get_button.setObjectName("get_button")
        self.detect_button = QtWidgets.QPushButton(self.centralwidget)
        self.detect_button.setGeometry(QtCore.QRect(1020, 50, 120, 40))
        self.detect_button.setAutoFillBackground(False)
        self.detect_button.setStyleSheet("background-color: red;")
        self.detect_button.setObjectName("detect_button")
        self.loaded_img = QtWidgets.QLabel(self.centralwidget)
        self.loaded_img.setGeometry(QtCore.QRect(30, 110, 480, 480))
        self.loaded_img.setFrameShape(QtWidgets.QFrame.Box)
        self.loaded_img.setScaledContents(True)
        self.loaded_img.setObjectName("loaded_img")
        self.detected_img = QtWidgets.QLabel(self.centralwidget)
        self.detected_img.setGeometry(QtCore.QRect(660, 110, 480, 480))
        self.detected_img.setFrameShape(QtWidgets.QFrame.Box)
        self.detected_img.setFrameShadow(QtWidgets.QFrame.Plain)
        self.detected_img.setText("")
        self.detected_img.setObjectName("detected_img")
        self.model_button = QtWidgets.QPushButton(self.centralwidget)
        self.model_button.setGeometry(QtCore.QRect(660, 50, 120, 40))
        self.model_button.setObjectName("model_button")
        self.model_name = QtWidgets.QLabel(self.centralwidget)
        self.model_name.setGeometry(QtCore.QRect(800, 50, 80, 40))
        self.model_name.setObjectName("model_name")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1200, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)

        self.get_button.clicked.connect(self.load_image)
        self.detect_button.clicked.connect(self.run_detection_script)
        self.model_button.clicked.connect(self.load_model)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("Animals by tracks", "Animals by tracks"))
        self.get_button.setText(_translate("MainWindow", "Browse for image"))
        self.detect_button.setText(_translate("MainWindow", "Detect"))
        self.model_button.setText(_translate("MainWindow", "Load model"))
        self.model_name.setText(_translate("MainWindow", "None"))

    def load_image(self):
        file_dialog = QFileDialog()
        file_dialog.setNameFilter("Images (*.png *.jpg *.bmp *.jpeg)")
        file_dialog.setViewMode(QFileDialog.Detail)
        file_dialog.setFileMode(QFileDialog.ExistingFile)

        if file_dialog.exec_():
            # Get the selected file
            selected_image_path = file_dialog.selectedFiles()[0]

            # Load the image and display it in "loaded_img"
            pixmap = QtGui.QPixmap(selected_image_path)
            self.loaded_img.setPixmap(pixmap)
            self.loaded_img.setScaledContents(True)

            # Store the selected image path
            self.selected_image = selected_image_path
    

    def load_model(self):
        file_dialog = QFileDialog()
        file_dialog.setNameFilter("Model *.onnx")
        file_dialog.setViewMode(QFileDialog.Detail)
        file_dialog.setFileMode(QFileDialog.ExistingFile)
        if file_dialog.exec_():
            # Get the selected file
            selected_model_path = file_dialog.selectedFiles()[0]

            # Store the selected model path
            self.selected_model = selected_model_path
            self.change_model_name()
            self.change_color()

    def change_model_name(self):
        self.model_name.setText(f"{os.path.basename(self.selected_model)}")
        self.model_name.adjustSize()

    def change_color(self):
        new_color = QColor(0, 255, 0)  
        self.detect_button.setStyleSheet(f"background-color: {new_color.name()};")

    def run_detection_script(self):
    # Check if an image and model are loaded
        if hasattr(self, 'selected_image') and self.selected_image and hasattr(self, 'selected_model') and self.selected_model:
            
            detected_image_path = str(return_image(self.selected_model, self.selected_image))

            # Load file
            pixmap = QtGui.QPixmap(detected_image_path)
            self.detected_img.setPixmap(pixmap)
            self.detected_img.setScaledContents(True)

            # Remove the temporary file
            os.remove(detected_image_path)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
