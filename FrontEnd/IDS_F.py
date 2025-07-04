from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QThread, pyqtSignal


import scapy.all as scapy # type: ignore
import joblib
from scapy.layers.inet import IP, TCP # type: ignore
from scapy.sendrecv import sniff # type: ignore
import os


from BackEnd.ids_implementation import extract_features
from BackEnd.ids_implementation import log_attack
from BackEnd.ids_implementation import play_alert_sound

class IDSThread(QThread):
    update_log_signal = pyqtSignal(str)  # Signal to send log messages to the list widget

    def __init__(self, cameras, model_path):
        super(IDSThread, self).__init__()
        self.cameras = cameras
        self.model_path = model_path
        self.running = True  # Control the thread execution

    def run(self):
        # Load the trained AI model
        model = joblib.load(self.model_path)

        # Prepare IP and port mappings
        ip_categories = {}
        reverse_ip_categories = {}
        ip_camera_list = []

        # Extracting IP and ports into a list of tuples
        for ip, data in self.cameras.items(): #iterate iver the camera dictionary
            services = data.get("services", []) #get the list of dictionary storing camera services
            for service in services: #iterate over the list (each service is a dictionary)
                ip_camera_list.append((ip, service['port']))
        
        for ip in self.cameras.keys():
            if ip not in ip_categories:
                category = len(ip_categories)
                ip_categories[ip] = category
                reverse_ip_categories[category] = ip

        def detect_attack(packet):
            """Callback to detect attacks and handle them."""
            if not self.running:  # Stop processing if the thread is stopped
                return
            features = extract_features(packet, ip_categories, reverse_ip_categories)
            if features is not None:
                prediction = model.predict(features)[0]  # Predict traffic type
                real_ip = reverse_ip_categories[features.iloc[0]["dst_ip"]]
                dst_port = features.iloc[0]["dst_port"]

                if prediction == 1:  # DoS attack detected
                    log_message = f"⚠️ ALERT! Potential DoS attack detected on IP Camera {real_ip}:{dst_port}!"
                    
                    current_path = os.getcwd()
                    # Execute additional actions for an attack
                    play_alert_sound(os.path.join(current_path, "BackEnd", "materials", "siren-alert-96052.wav"))  # Play the alert sound
                    log_attack(real_ip, dst_port)  # Log the attack
                    
                else:  # Normal traffic
                    log_message = f"✅ Normal Traffic to IP Camera {real_ip}:{dst_port}"
                
                # Send log message to the GUI
                self.update_log_signal.emit(log_message)


        # Generate BPF filter
        filter_parts = [f"(dst host {ip} and dst port {port})" for ip, port in ip_camera_list]
        filter_conditions = " or ".join(filter_parts)

        # Start sniffing packets
        print(filter_conditions)
        sniff(filter=filter_conditions, prn=detect_attack, store=0, stop_filter=lambda _: not self.running)

    def stop(self):
        """Stop the thread."""
        self.running = False
        self.quit()
        self.wait()

class Ui_IntrusionDetectionSystem(object):

    def __init__(self):
        self.detected_cameras = {}

    def setupUi(self, IntrusionDetectionSystem, cameras, previous_window):

        self.ICP_window = previous_window
        self.iface = scapy.conf.iface
        self.detected_cameras = cameras

        self.ip_camera_list = []

        # Extracting IP and ports into a list of tuples
        for ip, data in self.detected_cameras.items(): #iterate iver the camera dictionary
            services = data.get("services", []) #get the list of dictionary storing camera services
            for service in services: #iterate over the list (each service is a dictionary)
                self.ip_camera_list.append((ip, service['port']))

        print(self.detected_cameras)

        IntrusionDetectionSystem.setObjectName("IntrusionDetectionSystem")
        IntrusionDetectionSystem.resize(1156, 656)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("cameras_television_system_security_camera_video_cam_cctv_casino_icon_255630.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        IntrusionDetectionSystem.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(IntrusionDetectionSystem)
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
                font-size: 20px;
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

        self.interface_label = QtWidgets.QLabel(self.centralwidget)
        self.interface_label.setGeometry(QtCore.QRect(20, 20, 550, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.interface_label.setFont(font)
        self.interface_label.setObjectName("interface_label")

        self.interface2_label = QtWidgets.QLabel(self.centralwidget)
        self.interface2_label.setGeometry(QtCore.QRect(500, 20, 600, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.interface2_label.setFont(font)
        self.interface2_label.setObjectName("interface2_label")

        self.cameras_label = QtWidgets.QLabel(self.centralwidget)
        self.cameras_label.setGeometry(QtCore.QRect(272, 60, 250, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.cameras_label.setFont(font)
        self.cameras_label.setObjectName("cameras_label")

        self.cameras2_label = QtWidgets.QLabel(self.centralwidget)
        self.cameras2_label.setGeometry(QtCore.QRect(500, 60, 480, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.cameras2_label.setFont(font)
        self.cameras2_label.setObjectName("cameras2_label")

        self.ids_label = QtWidgets.QLabel(self.centralwidget)
        self.ids_label.setGeometry(QtCore.QRect(25, 130, 121, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.ids_label.setFont(font)
        self.ids_label.setObjectName("ids_label")

        self.listWidget = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget.setGeometry(QtCore.QRect(40, 180, 1081, 311))
        self.listWidget.setStyleSheet(list_widget_style)
        self.listWidget.setObjectName("listWidget")

        self.start_pushButton = QtWidgets.QPushButton(self.centralwidget, clicked = lambda: self.start_monitoring())
        self.start_pushButton.setGeometry(QtCore.QRect(220, 510, 331, 51))
        self.start_pushButton.setStyleSheet(push_button_greenlabel)
        self.start_pushButton.setObjectName("start_pushButton")

        self.back_pushButton = QtWidgets.QPushButton(self.centralwidget, clicked = lambda: self.back_to_ICP())
        self.back_pushButton.setGeometry(QtCore.QRect(670, 510, 331, 51))
        self.back_pushButton.setStyleSheet(push_button_redlabel)
        self.back_pushButton.setObjectName("back_pushButton")

        IntrusionDetectionSystem.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(IntrusionDetectionSystem)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1156, 26))
        self.menubar.setObjectName("menubar")

        IntrusionDetectionSystem.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(IntrusionDetectionSystem)
        self.statusbar.setObjectName("statusbar")
        IntrusionDetectionSystem.setStatusBar(self.statusbar)

        self.retranslateUi(IntrusionDetectionSystem)
        QtCore.QMetaObject.connectSlotsByName(IntrusionDetectionSystem)

        self.IDS_window = IntrusionDetectionSystem

    def retranslateUi(self, IntrusionDetectionSystem):
        _translate = QtCore.QCoreApplication.translate
        IntrusionDetectionSystem.setWindowTitle(_translate("IntrusionDetectionSystem", "Intrusion Detection System (IDS)"))
        self.interface_label.setText(_translate("IntrusionDetectionSystem", "Capturing Network Traffic Through Interface:"))
        self.cameras_label.setText(_translate("IntrusionDetectionSystem", "Monitoring Cameras:"))
        self.ids_label.setText(_translate("IntrusionDetectionSystem", "IDS Log:"))
        self.start_pushButton.setText(_translate("IntrusionDetectionSystem", "Start Monitoring"))
        self.back_pushButton.setText(_translate("IntrusionDetectionSystem", "Back"))

        self.interface2_label.setText(f"{self.iface}")
        self.cameras2_label.setText(f"{self.ip_camera_list}")

    def back_to_ICP(self):
        """Stop the IDS thread and go back to the previous window."""
        try:
            if self.ids_thread or self.ids_thread.isRunning():
                self.ids_thread.stop()  # Stop the IDS thread before closing
            self.IDS_window.close()
            self.ICP_window.show()
        except:
            self.IDS_window.close()
            self.ICP_window.show()

    def start_monitoring(self):
        self.listWidget.addItem("Initialize the Intrusion Detection System (IDS)....")
        """Start the IDS monitoring in a separate thread."""
        # Initialize the IDS thread with the detected cameras and AI model path
        current_path = os.getcwd()
        ai_model_path = os.path.join(current_path, "BackEnd" , "materials", "ai_model", "ids_model_v2.pkl")
        self.ids_thread = IDSThread(self.detected_cameras, ai_model_path)
        
        # Connect the thread's signal to the list widget
        self.ids_thread.update_log_signal.connect(self.listWidget.addItem)
        
        # Start the thread
        self.ids_thread.start()
        self.listWidget.addItem("The Intrusion Detection System (IDS) has been successfully initialized")
    



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    IntrusionDetectionSystem = QtWidgets.QMainWindow()
    ui = Ui_IntrusionDetectionSystem()
    ui.setupUi(IntrusionDetectionSystem)
    IntrusionDetectionSystem.show()
    sys.exit(app.exec_())
