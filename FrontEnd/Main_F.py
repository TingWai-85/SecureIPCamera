from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox

from BackEnd.ip_camera_discovery import get_network_detail # type: ignore
from BackEnd.ip_camera_discovery import subnet_calculation # type: ignore
from BackEnd.ip_camera_discovery import scan_for_cameras # type: ignore
from BackEnd.general_function import validate_ip # type: ignore

from VulnerabilityAssessment_F import Ui_VulnerabilityAssessment # type: ignore
from IDS_F import Ui_IntrusionDetectionSystem # type: ignore

class Ui_SecureIPCamera(object):

    def __init__(self):
            self.detected_IP_cameras = {}

    def setupUi(self, SecureIPCamera):

        SecureIPCamera.setObjectName("SecureIPCamera")
        SecureIPCamera.setWindowModality(QtCore.Qt.ApplicationModal)
        SecureIPCamera.resize(839, 704)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("cameras_television_system_security_camera_video_cam_cctv_casino_icon_255630.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        SecureIPCamera.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(SecureIPCamera)
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
        
        radio_button_label = """
            QRadioButton {
                font-size: 14px; /* Font size */
                color: #333333; /* Text color */
            }
            QRadioButton::indicator {
                width: 16px; /* Indicator size */
                height: 16px;
            }
            QRadioButton::indicator:checked {
                background-color: #ADD8E6; /* Light blue background for checked state */
                border: 2px solid #5F9EA0; /* Light blue border color */
                border-radius: 8px; /* Rounded indicator */
            }
            QRadioButton::indicator:unchecked {
                background-color: #FFFFFF; /* Default background */
                border: 2px solid #888888; /* Border color */
                border-radius: 8px; /* Rounded indicator */
            }
        """
        combo_box_label = """
            QComboBox {
                background-color: #FFFFFF; /* White background */
                border: 2px solid #888888; /* Border color */
                border-radius: 8px; /* Rounded corners */
                padding: 5px; /* Padding */
                font-size: 14px; /* Font size */
                color: #333333; /* Text color */
            }
            QComboBox:hover {
                border-color: #4CAF50; /* Border changes on hover */
            }
            QComboBox::drop-down {
                width: 30px; /* Dropdown button width */
                background-color: #F1F1F1; /* Button background */
                border-left: 2px solid #888888; /* Separator */
            }
            QComboBox QAbstractItemView {
                background-color: #FFFFFF; /* Dropdown list background */
                border: 1px solid #888888; /* Border */
                font-size: 14px; /* Font size */
            }
        """
        text_edit_label = """
            QTextEdit {
                background-color: #F9F9F9; /* Light gray background */
                border: 2px solid #CCCCCC; /* Border color */
                border-radius: 10px; /* Rounded corners */
                font-size: 14px; /* Font size */
                color: #333333; /* Text color */
                padding: 8px; /* Padding */
            }
            QTextEdit:focus {
                border-color: #4CAF50; /* Border changes when focused */
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
                padding: 10px; /* Padding for items */
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

        self.NetworkScanning_pushButton = QtWidgets.QPushButton(self.centralwidget, clicked = lambda: self.network_detail())
        self.NetworkScanning_pushButton.setEnabled(True)
        self.NetworkScanning_pushButton.setGeometry(QtCore.QRect(30, 25, 191, 45))
        self.NetworkScanning_pushButton.setStyleSheet(push_button_label)
        self.NetworkScanning_pushButton.setObjectName("NetworkScanning_pushButton")

        self.hostname_label = QtWidgets.QLabel(self.centralwidget)
        self.hostname_label.setGeometry(QtCore.QRect(140, 80, 220, 16))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.hostname_label.setFont(font)
        self.hostname_label.setObjectName("hostname_label")

        self.IP_label = QtWidgets.QLabel(self.centralwidget)
        self.IP_label.setGeometry(QtCore.QRect(40, 110, 310, 16))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.IP_label.setFont(font)
        self.IP_label.setObjectName("IP_label")

        self.SubnetBase_label = QtWidgets.QLabel(self.centralwidget)
        self.SubnetBase_label.setGeometry(QtCore.QRect(38, 140, 310, 16))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.SubnetBase_label.setFont(font)
        self.SubnetBase_label.setObjectName("SubnetBase_label")

        self.SubnetOption_label = QtWidgets.QLabel(self.centralwidget)
        self.SubnetOption_label.setGeometry(QtCore.QRect(198, 170, 160, 20))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.SubnetOption_label.setFont(font)
        self.SubnetOption_label.setObjectName("SubnetOption_label")
        
        self.DefaultSubnetMask_radioButton = QtWidgets.QRadioButton(self.centralwidget)
        self.DefaultSubnetMask_radioButton.setGeometry(QtCore.QRect(380, 170, 311, 20))
        self.DefaultSubnetMask_radioButton.setStyleSheet(radio_button_label)
        self.DefaultSubnetMask_radioButton.setObjectName("DefaultSubnetMask_radioButton")

        self.CustomSubnetMask_radioButton = QtWidgets.QRadioButton(self.centralwidget)
        self.CustomSubnetMask_radioButton.setGeometry(QtCore.QRect(380, 200, 231, 20))
        self.CustomSubnetMask_radioButton.setStyleSheet(radio_button_label)
        self.CustomSubnetMask_radioButton.setObjectName("CustomSubnetMask_radioButton")

        self.SpecificIP_radioButton = QtWidgets.QRadioButton(self.centralwidget)
        self.SpecificIP_radioButton.setGeometry(QtCore.QRect(380, 230, 201, 20))
        self.SpecificIP_radioButton.setStyleSheet(radio_button_label)
        self.SpecificIP_radioButton.setObjectName("SpecificIP_radioButton")


        label_for_scan_result = """
            QLabel {
                color: rgb(85, 0, 255); /* Purple text */
                font-size: 16px; /* Font size */
            }
        """
        self.Hostname_label = QtWidgets.QLabel(self.centralwidget)
        self.Hostname_label.setGeometry(QtCore.QRect(380, 80, 171, 16))
        self.Hostname_label.setStyleSheet(label_for_scan_result)
        self.Hostname_label.setText("")
        self.Hostname_label.setObjectName("Hostname_label")

        self.WirelessIP_label = QtWidgets.QLabel(self.centralwidget)
        self.WirelessIP_label.setGeometry(QtCore.QRect(380, 110, 171, 20))
        self.WirelessIP_label.setStyleSheet(label_for_scan_result)
        self.WirelessIP_label.setText("")
        self.WirelessIP_label.setObjectName("WirelessIP_label")

        self.SubnetBase_label_2 = QtWidgets.QLabel(self.centralwidget)
        self.SubnetBase_label_2.setGeometry(QtCore.QRect(380, 140, 171, 20))
        self.SubnetBase_label_2.setStyleSheet(label_for_scan_result)
        self.SubnetBase_label_2.setText("")
        self.SubnetBase_label_2.setObjectName("SubnetBase_label_2")

        self.SubnetOption_comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.SubnetOption_comboBox.setEnabled(False)
        self.SubnetOption_comboBox.setGeometry(QtCore.QRect(570, 200, 181, 25))
        self.SubnetOption_comboBox.setStyleSheet(combo_box_label)
        self.SubnetOption_comboBox.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.SubnetOption_comboBox.addItem("/24")
        self.SubnetOption_comboBox.addItem("/16")
        self.SubnetOption_comboBox.addItem("/8")
        self.SubnetOption_comboBox.setObjectName("SubnetOption_comboBox")
        self.SubnetOption_comboBox.hide()

        self.SpecificIP_textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.SpecificIP_textEdit.setEnabled(False)
        self.SpecificIP_textEdit.setGeometry(QtCore.QRect(570, 230, 231, 37))
        self.SpecificIP_textEdit.setStyleSheet(text_edit_label)
        self.SpecificIP_textEdit.setObjectName("SpecificIP_textEdit")
        self.SpecificIP_textEdit.hide()

        self.CameraScan_pushButton = QtWidgets.QPushButton(self.centralwidget, clicked = lambda: self.network_range())
        self.CameraScan_pushButton.setGeometry(QtCore.QRect(320, 260, 221, 41))
        self.CameraScan_pushButton.setStyleSheet(push_button_label)
        self.CameraScan_pushButton.setObjectName("CameraScan_pushButton")

        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setGeometry(QtCore.QRect(20, 310, 801, 20))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.line.setFont(font)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setLineWidth(2)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setObjectName("line")

        self.DetectedIPCameras_label = QtWidgets.QLabel(self.centralwidget)
        self.DetectedIPCameras_label.setGeometry(QtCore.QRect(50, 340, 300, 16))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.DetectedIPCameras_label.setFont(font)
        self.DetectedIPCameras_label.setObjectName("DetectedIPCameras_label")

        self.IPCameras_listWidget = QtWidgets.QListWidget(self.centralwidget)
        self.IPCameras_listWidget.setGeometry(QtCore.QRect(50, 370, 751, 192))
        self.IPCameras_listWidget.setStyleSheet(list_widget_style)
        self.IPCameras_listWidget.setObjectName("IPCameras_listWidget")

        self.VA_pushButton = QtWidgets.QPushButton(self.centralwidget, clicked = lambda: self.open_VA_window())
        self.VA_pushButton.setGeometry(QtCore.QRect(100, 590, 301, 51))
        self.VA_pushButton.setStyleSheet(push_button_label)
        self.VA_pushButton.setObjectName("VA_pushButton")

        self.IDS_pushButton = QtWidgets.QPushButton(self.centralwidget, clicked = lambda: self.open_IDS_window())
        self.IDS_pushButton.setGeometry(QtCore.QRect(440, 590, 321, 51))
        self.IDS_pushButton.setStyleSheet(push_button_label)
        self.IDS_pushButton.setObjectName("IDS_pushButton")

        SecureIPCamera.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(SecureIPCamera)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 839, 26))
        self.menubar.setObjectName("menubar")

        SecureIPCamera.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(SecureIPCamera)
        self.statusbar.setObjectName("statusbar")
        SecureIPCamera.setStatusBar(self.statusbar)

        # Connect the toggled signals
        self.CustomSubnetMask_radioButton.toggled.connect(self.toggle_combo_box)
        self.SpecificIP_radioButton.toggled.connect(self.toggle_text_edit)

        self.retranslateUi(SecureIPCamera)
        QtCore.QMetaObject.connectSlotsByName(SecureIPCamera)

        self.ICP_window = SecureIPCamera

    def retranslateUi(self, SecureIPCamera):
        _translate = QtCore.QCoreApplication.translate
        SecureIPCamera.setWindowTitle(_translate("SecureIPCamera", "SecureIPCamera"))
        self.NetworkScanning_pushButton.setText(_translate("SecureIPCamera", "Network Scanning"))
        self.hostname_label.setText(_translate("SecureIPCamera", "Detected Hostname:"))
        self.IP_label.setText(_translate("SecureIPCamera", "Detected Wireless IP Address:"))
        self.SubnetBase_label.setText(_translate("SecureIPCamera", "Detected Default Subnet Base:"))
        self.SubnetOption_label.setText(_translate("SecureIPCamera", "Subnet Option:"))
        self.DefaultSubnetMask_radioButton.setText(_translate("SecureIPCamera", "Use Default Subnet Mask (/24)"))
        self.CustomSubnetMask_radioButton.setText(_translate("SecureIPCamera", "Custom Subnet Mask"))
        self.SpecificIP_radioButton.setText(_translate("SecureIPCamera", "Specific IP Address"))
        self.CameraScan_pushButton.setText(_translate("SecureIPCamera", "Scan for IP Cameras"))
        self.DetectedIPCameras_label.setText(_translate("SecureIPCamera", "Detected IP Cameras:"))
        self.VA_pushButton.setText(_translate("SecureIPCamera", "Vulnerability Assessment"))
        self.IDS_pushButton.setText(_translate("SecureIPCamera", "Intrusion Detection System (IDS)"))

    def network_detail(self):
        my_network_detail = get_network_detail()
        hostname = my_network_detail[0]
        local_ip = my_network_detail[1]
        default_subnet = my_network_detail[2]
        self.Hostname_label.setText(hostname)
        self.WirelessIP_label.setText(local_ip)
        self.SubnetBase_label_2.setText(f"{default_subnet}.X")

    def toggle_combo_box(self, checked):
        if checked:
            # Enable the combo box only if the CustomSubnetMask radio button is checked
            self.SubnetOption_comboBox.show()
            self.SubnetOption_comboBox.setEnabled(checked)
        else:
            self.SubnetOption_comboBox.hide()

    def toggle_text_edit(self, checked):
        if checked:
            # Enable the text edit only if the SpecificIP radio button is checked
            self.SpecificIP_textEdit.show()
            self.SpecificIP_textEdit.setEnabled(checked)
        else:
            self.SpecificIP_textEdit.hide()
            

    def network_range(self):
        msg = QMessageBox()
        msg.setWindowTitle("Error in IP Subnet for Scannnig")
        msg.setText("Please try again on the subnet option to get a valid IP Subnet Range for Scanning!")
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowIcon(QtGui.QIcon("cameras_television_system_security_camera_video_cam_cctv_casino_icon_255630.ico"))
        ip_subnet_address = ""
        ip_cameras = {}

        if self.DefaultSubnetMask_radioButton.isChecked() == True:
            if self.SubnetBase_label_2.text() != "":
                ip_subnet = ".".join(self.SubnetBase_label_2.text().split(".")[:3])
                ip_subnet_address = subnet_calculation(ip_subnet,24)
                ip_cameras = scan_for_cameras(ip_subnet_address)
            else:
                x = msg.exec()
            
        elif self.CustomSubnetMask_radioButton.isChecked() == True:
            if self.SubnetBase_label_2.text() != "":
                mask_string = self.SubnetOption_comboBox.currentText()
                mask = int(mask_string.lstrip('/'))
                ip_subnet = ".".join(self.SubnetBase_label_2.text().split(".")[:3])
                ip_subnet_address = subnet_calculation(ip_subnet, mask)
                ip_cameras = scan_for_cameras(ip_subnet_address)
            else:
                x = msg.exec()

        elif self.SpecificIP_radioButton.isChecked() == True:
            specific_ip = self.SpecificIP_textEdit.toPlainText()
            if validate_ip(specific_ip) == True:
                ip_subnet_address = specific_ip + "/32"
                ip_cameras = scan_for_cameras(ip_subnet_address)
            else:
                x = msg.exec_()

        else:
            x = msg.exec_()
            
        self.detected_IP_cameras = ip_cameras
        for ip, services in self.detected_IP_cameras.items():
            camera = f"IP: {ip}: \n"
            camera_service = ""

            for service in services['services']:
                camera_service = f"{camera_service} \tPort: {service['port']} | Service: {service['service']} | Product: {service['product']} | Version: {service['version']}\n"

            camera = f"{camera}{camera_service}"
            self.IPCameras_listWidget.addItem(camera)

    def open_VA_window(self):
        self.VA_window = QtWidgets.QMainWindow()
        self.ui = Ui_VulnerabilityAssessment()
        self.ui.setupUi(self.VA_window, self.detected_IP_cameras, self.ICP_window)
        self.VA_window.show()
        self.ICP_window.close()

    def open_IDS_window(self):
        self.IDS_window = QtWidgets.QMainWindow()
        self.ui = Ui_IntrusionDetectionSystem()
        self.ui.setupUi(self.IDS_window, self.detected_IP_cameras, self.ICP_window)
        self.IDS_window.show()
        self.ICP_window.close()
        pass


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    SecureIPCamera = QtWidgets.QMainWindow()
    ui = Ui_SecureIPCamera()
    ui.setupUi(SecureIPCamera)
    SecureIPCamera.show()
    sys.exit(app.exec_())
