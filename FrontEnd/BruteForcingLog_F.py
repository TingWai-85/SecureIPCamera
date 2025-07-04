from PyQt5 import QtCore, QtGui, QtWidgets


from BackEnd.vulnerability_assessment import brute_force_login_front # type: ignore

class Ui_BruteForcingLog(object):

    def __init__(self):

        self.detected_IP_cameras = {}
        self.vulnerabilities = []

    def setupUi(self, BruteForcingLog, detected_cameras, previos_window, selected_ipaddress, previous_instance):

        self.detected_IP_cameras = detected_cameras
        self.VA_window = previos_window
        self.VA_instance = previous_instance
        self.selected_IP = selected_ipaddress

        BruteForcingLog.setObjectName("BruteForcingLog")
        BruteForcingLog.resize(701, 635)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("cameras_television_system_security_camera_video_cam_cctv_casino_icon_255630.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        BruteForcingLog.setWindowIcon(icon)

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


        self.bfl_label = QtWidgets.QLabel(BruteForcingLog)
        self.bfl_label.setGeometry(QtCore.QRect(40, 20, 291, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.bfl_label.setFont(font)
        self.bfl_label.setObjectName("bfl_label")

        self.bfl_listWidget = QtWidgets.QListWidget(BruteForcingLog)
        self.bfl_listWidget.setGeometry(QtCore.QRect(40, 70, 631, 451))
        self.bfl_listWidget.setStyleSheet(list_widget_style)
        self.bfl_listWidget.setObjectName("bfl_listWidget")

        self.back_pushButton = QtWidgets.QPushButton(BruteForcingLog, clicked = lambda: self.back_to_VA())
        self.back_pushButton.setGeometry(QtCore.QRect(390, 550, 161, 51))
        self.back_pushButton.setStyleSheet(push_button_redlabel)
        self.back_pushButton.setObjectName("back_pushButton")

        self.start_pushButton = QtWidgets.QPushButton(BruteForcingLog, clicked = lambda: self.brute_forcing())
        self.start_pushButton.setGeometry(QtCore.QRect(140, 550, 161, 51))
        self.start_pushButton.setStyleSheet(push_button_greenlabel)
        self.start_pushButton.setObjectName("start_pushButton")

        self.retranslateUi(BruteForcingLog)
        QtCore.QMetaObject.connectSlotsByName(BruteForcingLog)

        self.BFL_window = BruteForcingLog



    def retranslateUi(self, BruteForcingLog):
        _translate = QtCore.QCoreApplication.translate
        BruteForcingLog.setWindowTitle(_translate("BruteForcingLog", "Brute Forcing"))
        self.bfl_label.setText(_translate("BruteForcingLog", "IP Camera Brute Forcing Log:"))
        self.back_pushButton.setText(_translate("BruteForcingLog", "Back"))
        self.start_pushButton.setText(_translate("BruteForcingLog", "Start"))


    def back_to_VA(self):
        
        self.VA_instance.get_second_vulns(self.vulnerabilities)
        self.BFL_window.close()
        self.VA_window.show()
    
    def brute_forcing(self):
        services_list = self.detected_IP_cameras[self.selected_IP]
        port_num = []

        for definition,data in services_list.items():
            if definition == 'services':
                for service in data:
                        port_num.append(service['port'])
        
        getting_response = True
        while getting_response:
            for port in port_num:
                vulns, output_string = brute_force_login_front(self.selected_IP,port)
                output_string.append("\n")
                for i in output_string:
                    self.bfl_listWidget.addItem(i)
            getting_response = False
            break

        self.vulnerabilities = self.vulnerabilities + vulns



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    BruteForcingLog = QtWidgets.QDialog()
    ui = Ui_BruteForcingLog()
    ui.setupUi(BruteForcingLog)
    BruteForcingLog.show()
    sys.exit(app.exec_())
