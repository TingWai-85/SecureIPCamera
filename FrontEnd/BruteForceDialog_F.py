from PyQt5 import QtCore, QtGui, QtWidgets
from BruteForcingLog_F import Ui_BruteForcingLog # type: ignore



class Ui_BruteForceDialog(object):

    def __init__(self):
        self.detected_IP_cameras = {}

    def setupUi(self, BruteForceDialog, detected_cameras, previos_window, selected_ipaddress, previous_instance):
        
        self.detected_IP_cameras= detected_cameras
        self.VA_window = previos_window
        self.VA_instance = previous_instance
        self.selected_ip = selected_ipaddress

        print(self.detected_IP_cameras)
        print(self.selected_ip)
        
        BruteForceDialog.setObjectName("BruteForceDialog")
        BruteForceDialog.resize(1030, 428)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("cameras_television_system_security_camera_video_cam_cctv_casino_icon_255630.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        BruteForceDialog.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(BruteForceDialog)
        self.centralwidget.setObjectName("centralwidget")

        push_button_greenlabel = """
            QPushButton {
                background-color: #22C55E; /* Green background */
                color: white; /* White text */
                font-size: 20px;
                border-radius: 10px;
                padding: 8px;
                border: 2px solid #16A34A;
            }
            QPushButton:hover {
                background-color: #16A34A;
            }
            QPushButton:pressed {
                background-color: #15803D;
            }
        """

        push_button_redlabel = """
            QPushButton {
                background-color: #EF4444; /* Red background */
                color: white; /* White text */
                font-size: 16px;
                border-radius: 10px;
                padding: 8px;
                border: 2px solid #DC2626;
            }
            QPushButton:hover {
                background-color: #DC2626;
            }
            QPushButton:pressed {
                background-color: #B91C1C;
            }
        """

        self.bfan_label = QtWidgets.QLabel(self.centralwidget)
        self.bfan_label.setGeometry(QtCore.QRect(20, 20, 811, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.bfan_label.setFont(font)
        self.bfan_label.setObjectName("bfan_label")

        self.bfan_label_2 = QtWidgets.QLabel(self.centralwidget)
        self.bfan_label_2.setGeometry(QtCore.QRect(20, 50, 811, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.bfan_label_2.setFont(font)
        self.bfan_label_2.setObjectName("bfan_label_2")

        self.bfan_label_3 = QtWidgets.QLabel(self.centralwidget)
        self.bfan_label_3.setGeometry(QtCore.QRect(20, 80, 980, 41))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        self.bfan_label_3.setPalette(palette)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.bfan_label_3.setFont(font)
        self.bfan_label_3.setObjectName("bfan_label_3")

        self.bfan_label_4 = QtWidgets.QLabel(self.centralwidget)
        self.bfan_label_4.setGeometry(QtCore.QRect(20, 110, 991, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.bfan_label_4.setFont(font)
        self.bfan_label_4.setObjectName("bfan_label_4")

        self.bfan_label_5 = QtWidgets.QLabel(self.centralwidget)
        self.bfan_label_5.setGeometry(QtCore.QRect(20, 180, 991, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.bfan_label_5.setFont(font)
        self.bfan_label_5.setObjectName("bfan_label_5")

        self.bfan_label_6 = QtWidgets.QLabel(self.centralwidget)
        self.bfan_label_6.setGeometry(QtCore.QRect(50, 210, 991, 41))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(170, 0, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(170, 0, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        self.bfan_label_6.setPalette(palette)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.bfan_label_6.setFont(font)
        self.bfan_label_6.setObjectName("bfan_label_6")

        self.bfan_label_7 = QtWidgets.QLabel(self.centralwidget)
        self.bfan_label_7.setGeometry(QtCore.QRect(50, 240, 991, 41))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(170, 0, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(170, 0, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        self.bfan_label_7.setPalette(palette)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.bfan_label_7.setFont(font)
        self.bfan_label_7.setObjectName("bfan_label_7")

        self.bfan_label_8 = QtWidgets.QLabel(self.centralwidget)
        self.bfan_label_8.setGeometry(QtCore.QRect(50, 270, 991, 41))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(170, 0, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(170, 0, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        self.bfan_label_8.setPalette(palette)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.bfan_label_8.setFont(font)
        self.bfan_label_8.setObjectName("bfan_label_8")
        
        self.proceed_pushButton = QtWidgets.QPushButton(self.centralwidget, clicked = lambda: self.open_BFL_dialog())
        self.proceed_pushButton.setGeometry(QtCore.QRect(100, 320, 311, 51))
        self.proceed_pushButton.setStyleSheet(push_button_greenlabel)
        self.proceed_pushButton.setObjectName("proceed_pushButton")

        self.cancel_pushButton = QtWidgets.QPushButton(self.centralwidget , clicked = lambda: self.back_to_VA())
        self.cancel_pushButton.setGeometry(QtCore.QRect(600, 320, 311, 51))
        self.cancel_pushButton.setStyleSheet(push_button_redlabel)
        self.cancel_pushButton.setObjectName("cancel_pushButton")

        BruteForceDialog.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(BruteForceDialog)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1013, 26))
        self.menubar.setObjectName("menubar")
        BruteForceDialog.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(BruteForceDialog)
        self.statusbar.setObjectName("statusbar")
        BruteForceDialog.setStatusBar(self.statusbar)

        self.retranslateUi(BruteForceDialog)
        QtCore.QMetaObject.connectSlotsByName(BruteForceDialog)

        self.BFD_window = BruteForceDialog

    def retranslateUi(self, BruteForceDialog):
        _translate = QtCore.QCoreApplication.translate
        BruteForceDialog.setWindowTitle(_translate("BruteForceDialog", "Brute Force Attack"))
        self.bfan_label.setText(_translate("BruteForceDialog", "Now, the application wish to conduct a brute force attack against your selected IP camera"))
        self.bfan_label_2.setText(_translate("BruteForceDialog", "However, the brute force attack may be taken hours to be completed"))
        self.bfan_label_3.setText(_translate("BruteForceDialog", "(As each attempt is taken 30 seconds to be completed to test the connection to your IP Camera)"))
        self.bfan_label_4.setText(_translate("BruteForceDialog", "And this attack will give you an overview if the credential you\'re using for your IP Camera is secure or insecure"))
        self.bfan_label_5.setText(_translate("BruteForceDialog", "If you choose to proceed with the brute force attack, here are some insturctions:"))
        self.bfan_label_6.setText(_translate("BruteForceDialog", "1) Make sure your local network connection is stable"))
        self.bfan_label_7.setText(_translate("BruteForceDialog", "2) You can press \'q\' to quit the RTSP streaming at any time"))
        self.bfan_label_8.setText(_translate("BruteForceDialog", "3) You can press \'s\' to take screenshot of your IP Camera footage"))
        self.proceed_pushButton.setText(_translate("BruteForceDialog", "Proceed"))
        self.cancel_pushButton.setText(_translate("BruteForceDialog", "Cancel"))

    def back_to_VA(self):
        self.VA_window.show()
        self.BFD_window.close()

    def open_BFL_dialog(self):

        self.BFL_dialog = QtWidgets.QDialog()
        self.ui = Ui_BruteForcingLog()
        self.ui.setupUi(self.BFL_dialog, self.detected_IP_cameras, self.VA_window, self.selected_ip, self.VA_instance)
        self.BFL_dialog.show()
        self.BFD_window.close()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    BruteForceDialog = QtWidgets.QMainWindow()
    ui = Ui_BruteForceDialog()
    ui.setupUi(BruteForceDialog)
    BruteForceDialog.show()
    sys.exit(app.exec_())
