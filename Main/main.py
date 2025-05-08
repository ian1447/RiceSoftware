import sys
import serial.tools.list_ports
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout, QPushButton,
    QComboBox, QHBoxLayout, QGridLayout
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Rice Software")
        self.setFixedSize(400, 250)

        # Buttons
        self.refresh_button = QPushButton("Refresh Ports")
        self.connect_button = QPushButton("Connect")

        # Serial port dropdown
        self.port_dropdown = QComboBox()
        self.port_dropdown.setPlaceholderText("Select a port")

        # Sensor value label (placed at the top-left)
        self.sensor_label = QLabel("Sensor Value: ---")
        self.sensor_label.setFont(QFont("Arial", 18))

        self.sensor_label2 = QLabel("Sensor Value: ---")
        self.sensor_label2.setFont(QFont("Arial", 18))

        # Align the sensor label to the top-left explicitly
        self.sensor_label.setAlignment(Qt.AlignLeft)
        self.sensor_label2.setAlignment(Qt.AlignLeft | Qt.AlignTop)

        # Connect buttons to actions
        self.refresh_button.clicked.connect(self.refresh_ports)
        self.connect_button.clicked.connect(self.connect_to_port)

        # Create the QGridLayout
        grid_layout = QGridLayout()

        # Add widgets to the grid (row, column)
        grid_layout.addWidget(self.sensor_label, 0, 0)  # Top-left
        # grid_layout.addWidget(self.sensor_label2, 0, 1)  # Top-right
        grid_layout.addWidget(self.port_dropdown, 1, 0)  # Below the label, left side
        grid_layout.addWidget(self.refresh_button, 1, 1)  # Right of the dropdown
        grid_layout.addWidget(self.connect_button, 2, 0, 1, 2)  # Spanning across two columns (bottom)

        # Set the layout for the main window
        self.setLayout(grid_layout)

        # Call refresh_ports after setting up the layout
        self.refresh_ports()

    def refresh_ports(self):
        self.port_dropdown.clear()
        ports = serial.tools.list_ports.comports()
        if len(ports) == 0:
            self.port_dropdown.addItem("No Available Ports")
            self.connect_button.setDisabled(True)
        else:
            self.connect_button.setDisabled(False)
            for port in ports:
                self.port_dropdown.addItem(f"{port.device} - {port.description}", port.device)

        self.port_dropdown.setCurrentIndex(0)

    def connect_to_port(self):
        selected_port = self.port_dropdown.currentData()
        if selected_port:
            print(f"Connecting to: {selected_port}")
            self.sensor_label.setText(f"Connected to {selected_port}")
        else:
            self.sensor_label.setText("No port selected")


app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec_())
