from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox

from BackEnd.mitigation import update_mitigation
from BackEnd.report_generation import report_main

class Ui_Mitigation(object):

    def __init__(self):
        self.detected_cameras = {}


    def setupUi(self, Mitigation, cameras, previous_window, ip_range):

        self.detected_cameras = cameras
        self.VA_window = previous_window
        self.ip_range = ip_range

        Mitigation.setObjectName("Mitigation")
        Mitigation.resize(1023, 745)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("cameras_television_system_security_camera_video_cam_cctv_casino_icon_255630.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Mitigation.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(Mitigation)
        self.centralwidget.setObjectName("centralwidget")

        push_button_label = """
            QPushButton {
                background-color: #3B82F6; /* Blue background */
                color: white; /* White text */
                font-size: 20px; /* Text size */
                border-radius: 10px; /* Rounded corners */
                padding: 8px; /* Padding */
                border: 2px solid #2563EB; /* Border color */
            }
            QPushButton:hover {
                background-color: #2563EB; /* Slightly darker blue on hover */
            }
            QPushButton:pressed {
                background-color: #1D4ED8; /* Even darker blue on press */
            }
        """

        list_widget_style = """
            QListWidget {
                background-color: #F9F9F9; /* Light background */
                border: 1px solid #CCCCCC; /* Light gray border */
                border-radius: 8px; /* Rounded corners */
                padding: 5px; /* Padding inside the list */
                font-size: 16px; /* Font size for items */
            }
            QListWidget::item {
                background-color: #FFFFFF; /* Default item background */
                color: #333333; /* Text color */
                padding: 1px; /* Padding for items */
                border: none; /* No border */
            }
            QListWidget::item:hover {
                background-color: #E0F7FA; /* Light blue on hover */
                color: #00796B; /* Darker text on hover */
            }
            QListWidget::item:selected {
                background-color: #ADD8E6; /* Light blue for selected item */
                color: #333333; /* Darker text for better contrast */
            }
            QListWidget::item:selected:active {
                background-color: #87CEEB; /* Slightly darker blue when active */
            }
            QScrollBar:vertical {
                border: none;
                background: #F0F0F0; /* Scrollbar track background */
                width: 10px; /* Width of the vertical scrollbar */
                margin: 0px 0px 0px 0px;
            }
            QScrollBar::handle:vertical {
                background: #CCCCCC; /* Handle color */
                min-height: 20px; /* Minimum height of the handle */
                border-radius: 5px; /* Rounded handle */
            }
            QScrollBar::handle:vertical:hover {
                background: #B0B0B0; /* Darker handle color on hover */
            }
            QScrollBar::add-line:vertical,
            QScrollBar::sub-line:vertical {
                height: 0px; /* Hide add and sub buttons */
            }
            QScrollBar::add-page:vertical,
            QScrollBar::sub-page:vertical {
                background: none; /* Transparent */
            }
        """

        self.vulnerabilities_label = QtWidgets.QLabel(self.centralwidget)
        self.vulnerabilities_label.setGeometry(QtCore.QRect(10, 10, 300, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.vulnerabilities_label.setFont(font)
        self.vulnerabilities_label.setObjectName("vulnerabilities_label")

        self.vulnerabilities_listWidget = QtWidgets.QListWidget(self.centralwidget)
        self.vulnerabilities_listWidget.setGeometry(QtCore.QRect(30, 50, 971, 221))
        self.vulnerabilities_listWidget.setStyleSheet(list_widget_style)
        self.vulnerabilities_listWidget.setObjectName("vulnerabilities_listWidget")

        for ip, data in self.detected_cameras.items():
            camera = f"IP: {ip}: \n"
            camera_vulnerabilities = ""

            for vulns in data['vulnerabilities']:
                camera_vulnerabilities = " | ".join(vulns)

                camera_vulns = f"{camera}{camera_vulnerabilities}\n"
                self.vulnerabilities_listWidget.addItem(camera_vulns)

        self.mitigation_pushButton = QtWidgets.QPushButton(self.centralwidget, clicked = lambda: self.mitigation_generation())
        self.mitigation_pushButton.setGeometry(QtCore.QRect(390, 290, 211, 51))
        self.mitigation_pushButton.setStyleSheet(push_button_label)
        self.mitigation_pushButton.setObjectName("mitigation_pushButton")

        self.mitigation_label = QtWidgets.QLabel(self.centralwidget)
        self.mitigation_label.setGeometry(QtCore.QRect(10, 350, 300, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.mitigation_label.setFont(font)
        self.mitigation_label.setObjectName("mitigation_label")

        self.mitigation_listWidget = QtWidgets.QListWidget(self.centralwidget)
        self.mitigation_listWidget.setGeometry(QtCore.QRect(30, 390, 971, 211))
        self.mitigation_listWidget.setStyleSheet(list_widget_style)
        self.mitigation_listWidget.setObjectName("mitigation_listWidget")

        self.report_pushButton = QtWidgets.QPushButton(self.centralwidget, clicked = lambda: self.report_generation())
        self.report_pushButton.setGeometry(QtCore.QRect(220, 630, 211, 51))
        self.report_pushButton.setStyleSheet(push_button_label)
        self.report_pushButton.setObjectName("report_pushButton")

        self.back_pushButton = QtWidgets.QPushButton(self.centralwidget, clicked = lambda: self.back_to_VA())
        self.back_pushButton.setGeometry(QtCore.QRect(590, 630, 211, 51))
        self.back_pushButton.setStyleSheet(push_button_label)
        self.back_pushButton.setObjectName("back_pushButton")

        Mitigation.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(Mitigation)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1023, 26))
        self.menubar.setObjectName("menubar")

        Mitigation.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(Mitigation)
        self.statusbar.setObjectName("statusbar")
        Mitigation.setStatusBar(self.statusbar)

        self.retranslateUi(Mitigation)
        QtCore.QMetaObject.connectSlotsByName(Mitigation)

        self.MR_window = Mitigation

    def retranslateUi(self, Mitigation):
        _translate = QtCore.QCoreApplication.translate
        Mitigation.setWindowTitle(_translate("Mitigation", "Mitigation & Report Generation"))
        self.vulnerabilities_label.setText(_translate("Mitigation", "Detected Vulnerabilities List:"))
        self.mitigation_pushButton.setText(_translate("Mitigation", "Mitigation Query"))
        self.mitigation_label.setText(_translate("Mitigation", "Recommended Mitigation:"))
        self.report_pushButton.setText(_translate("Mitigation", "Report Generation"))
        self.back_pushButton.setText(_translate("Mitigation", "Back"))

    def mitigation_generation(self):
        self.detected_cameras = update_mitigation(self.ip_range, self.detected_cameras)
        print(self.detected_cameras)

        for ip, data in self.detected_cameras.items():
            camera = f"IP: {ip}: \n"
            camera_vulnerabilities = ""

            for vulns in data['vulnerabilities']:
                camera_vulnerabilities = " | ".join(vulns[0:2])
                mitigation = vulns[2]

                camera_vulns = f"{camera}{camera_vulnerabilities}\n\tMitigation --> {mitigation}\n"
                self.mitigation_listWidget.addItem(camera_vulns)
    
    def report_generation(self):
        information = report_main("IP_Camera_Security_Report.pdf", self.detected_cameras)
        msg = QMessageBox()
        msg.setWindowTitle("Report Downloaded")
        msg.setText(information)
        msg.setIcon(QMessageBox.Information)
        msg.setWindowIcon(QtGui.QIcon("cameras_television_system_security_camera_video_cam_cctv_casino_icon_255630.ico"))
        msg.exec_()

    def back_to_VA(self):
        self.MR_window.close()
        



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Mitigation = QtWidgets.QMainWindow()
    ui = Ui_Mitigation()
    ui.setupUi(Mitigation)
    Mitigation.show()
    sys.exit(app.exec_())
