from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog, QGraphicsScene
import subprocess
import os
from pathlib import Path
import json

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
        self.detect_button.setGeometry(QtCore.QRect(845, 50, 120, 40))
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
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1200, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.get_button.clicked.connect(self.load_image)
        self.detect_button.clicked.connect(self.run_detection_script)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("Animals by tracks", "Animals by tracks"))
        self.get_button.setText(_translate("MainWindow", "Browse for image"))
        self.detect_button.setText(_translate("MainWindow", "Detect"))

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

    def run_detection_script(self):
    # Check if an image is loaded
        if hasattr(self, 'selected_image') and self.selected_image:
            # Run the detection script with the selected image as an argument
            process = subprocess.run(["python", "detection.py", self.selected_image], capture_output=True, text=True)

            # Get the file path of the detected image from the script output
            detected_image_path = process.stdout.strip()

            # Load and display the detected image in QGraphicsView
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
