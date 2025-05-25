import sys
import os
import requests
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLineEdit, QFileDialog, 
                             QLabel, QMessageBox)
from PyQt6.QtGui import QDragEnterEvent, QDropEvent, QIcon

# File to store the saved IP address
IP_FILE = 'saved_ip.txt'

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Y.A.P.S")
        self.setMinimumSize(500, 300)

        # Set the application icon
        self.setWindowIcon(QIcon("icon.ico"))  # Replace with your icon file name
        
        # Color Palette
        self.setStyleSheet("""
            QMainWindow, QWidget {
                background-color: #1E1E1E;
                color: #FFFFFF;
            }
            QPushButton {
                background-color: #2D2D2D;
                color: #FFD700;
                border: 1px solid #FFD700;
                border-radius: 4px;
                padding: 8px 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #3D3D3D;
            }
            QPushButton:pressed {
                background-color: #FFD700;
                color: #1E1E1E;
            }
            QLineEdit {
                background-color: #2D2D2D;
                color: #FFFFFF;
                border: 1px solid #444444;
                border-radius: 4px;
                padding: 8px;
            }
            QLabel {
                color: #FFD700;
                font-weight: bold;
            }
        """)
        
        # Central Widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)

        # File Selection
        file_layout = QHBoxLayout()
        self.file_path = QLineEdit()
        self.file_path.setPlaceholderText("Path to .bin file...")
        self.file_path.setReadOnly(True)
        self.file_path.setAcceptDrops(True)  # Enable drag and drop

        # Drag and drop events
        self.file_path.dragEnterEvent = self.dragEnterEvent
        self.file_path.dropEvent = self.dropEvent
        
        browse_button = QPushButton("Browse")
        browse_button.clicked.connect(self.browse_file)
        browse_button.setFixedWidth(100)
        
        file_layout.addWidget(QLabel("File:"))
        file_layout.addWidget(self.file_path)
        file_layout.addWidget(browse_button)
        layout.addLayout(file_layout)
        
        # IP Address
        ip_layout = QHBoxLayout()
        self.ip_address = QLineEdit()
        self.ip_address.setPlaceholderText("IP Address...")
        
        ip_layout.addWidget(QLabel("IP:"))
        ip_layout.addWidget(self.ip_address)
        layout.addLayout(ip_layout)
        
        # Port
        port_layout = QHBoxLayout()
        self.port = QLineEdit("9090")
        self.port.setPlaceholderText("Port...")
        
        port_layout.addWidget(QLabel("Port:"))
        port_layout.addWidget(self.port)
        layout.addLayout(port_layout)
        
        # Send Button
        layout.addSpacing(20)
        self.send_button = QPushButton("SEND")
        self.send_button.setFixedHeight(50)
        self.send_button.clicked.connect(self.send_request)
        layout.addWidget(self.send_button)

        # Load saved IP address
        self.load_saved_ip()

    def browse_file(self):
        file_dialog = QFileDialog()
        file_dialog.setNameFilter("BIN Files (*.bin)")
        if file_dialog.exec():
            file_path = file_dialog.selectedFiles()[0]
            self.file_path.setText(file_path)
    
    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
    
    def dropEvent(self, event: QDropEvent):
        if event.mimeData().hasUrls():
            file_url = event.mimeData().urls()[0].toLocalFile()
            if file_url.endswith('.bin'):
                self.file_path.setText(file_url)
            else:
                QMessageBox.warning(self, "Error", "Please drop a .bin file.")
    
    def send_request(self):
        file_path = self.file_path.text()
        ip = self.ip_address.text()
        port = self.port.text()
        
        if not file_path:
            QMessageBox.warning(self, "Error", "Please select a .bin file")
            return
        
        if not ip:
            QMessageBox.warning(self, "Error", "Please enter an IP address")
            return
        
        if not port:
            port = "9090"
        
        try:
            url = f"http://{ip}:{port}"
            with open(file_path, 'rb') as f:
                file_content = f.read()
            
            response = requests.post(url, data=file_content)
            
            if response.status_code == 200:
                QMessageBox.information(self, "Success", "File sent successfully!")
                self.save_ip(ip)  # Save the IP address if the request is successful
            else:
                QMessageBox.critical(self, "Error", f"Failed to send: {response.status_code}")
        
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error during sending: {str(e)}")
    
    def save_ip(self, ip):
        with open(IP_FILE, 'w') as f:
            f.write(ip)
    
    def load_saved_ip(self):
        if os.path.exists(IP_FILE):
            with open(IP_FILE, 'r') as f:
                saved_ip = f.read().strip()
                self.ip_address.setText(saved_ip)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())