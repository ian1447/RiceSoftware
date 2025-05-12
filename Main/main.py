import sys
import serial.tools.list_ports
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout, QPushButton,
    QComboBox, QHBoxLayout, QGridLayout
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, QTimer


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Rice Software")
        self.setFixedSize(400, 250)

        self.refresh_button = QPushButton("Refresh Ports")
        self.connect_button = QPushButton("Connect")
        self.start_button = QPushButton("Start")

        self.start_button.setStyleSheet("background-color: green; color: white;")

        self.port_dropdown = QComboBox()
        self.port_dropdown.setPlaceholderText("Select a port")

        self.sensor_label = QLabel("Temperature: ---")
        self.sensor_label.setFont(QFont("Arial", 18))

        self.sensor_label2 = QLabel("Humidity: ---")
        self.sensor_label2.setFont(QFont("Arial", 18))

        self.timer_label = QLabel("Time: 0s")
        self.timer_label.setFont(QFont("Arial", 14))

        # Device status labels
        self.fan_label = QLabel("Fan: OFF")
        self.fan_label.setFont(QFont("Arial", 14))
        self.fan_label.setStyleSheet("color: white; background-color: red; padding: 4px;")

        self.heater_label = QLabel("Heater: OFF")
        self.heater_label.setFont(QFont("Arial", 14))
        self.heater_label.setStyleSheet("color: white; background-color: red; padding: 4px;")

        self.exhaust_label = QLabel("Exhaust: OFF")
        self.exhaust_label.setFont(QFont("Arial", 14))
        self.exhaust_label.setStyleSheet("color: white; background-color: red; padding: 4px;")

        self.sensor_label.setAlignment(Qt.AlignLeft)
        self.sensor_label2.setAlignment(Qt.AlignLeft | Qt.AlignTop)

        self.refresh_button.clicked.connect(self.refresh_ports)
        self.connect_button.clicked.connect(self.connect_to_port)
        self.start_button.clicked.connect(self.start_action)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)

        # Create the QGridLayout
        grid_layout = QGridLayout()
        grid_layout.setVerticalSpacing(10)
        grid_layout.setHorizontalSpacing(10)
        grid_layout.setContentsMargins(10, 10, 10, 10)

        # Row 0: Sensor labels
        grid_layout.addWidget(self.sensor_label, 0, 0, 1, 2)
        grid_layout.addWidget(self.sensor_label2, 0, 2)  # Span 2 columns

        # Row 1: Fan/heater/exhaust labels
        grid_layout.addWidget(self.fan_label, 1, 0)
        grid_layout.addWidget(self.heater_label, 1, 1)
        grid_layout.addWidget(self.exhaust_label, 1, 2)

        # Row 2: Start button centered across all 3 columns
        grid_layout.addWidget(self.start_button, 2, 0, 1, 3)

        # Row 3: Port dropdown and refresh button
        grid_layout.addWidget(self.port_dropdown, 3, 0, 1, 2)
        grid_layout.addWidget(self.refresh_button, 3, 2)

        # Row 4: Connect button spans all 3 columns
        grid_layout.addWidget(self.connect_button, 4, 0, 1, 3)

        # Row 5: Timer label centered across all 3 columns
        grid_layout.addWidget(self.timer_label, 5, 0, 1, 3)

        self.setLayout(grid_layout)
        self.refresh_ports()

    def refresh_ports(self):
        self.start_button.setDisabled(True)
        self.start_button.setStyleSheet("background-color: black; color: white;")
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
            self.start_button.setDisabled(False)
            self.start_button.setStyleSheet("background-color: green; color: white;")

    def start_action(self):
        print("Start button pressed")
        self.refresh_button.setDisabled(True)
        self.connect_button.setDisabled(True)
        self.port_dropdown.setDisabled(True)
        self.start_button.setDisabled(True)
        self.start_button.setStyleSheet("")
        self.sensor_label.setText("Temperature: 36°C")
        self.sensor_label2.setText("Humidity: 41%")

        self.fan_label.setText("Fan: ON")
        self.fan_label.setStyleSheet("color: white; background-color: green; padding: 4px;")

        self.heater_label.setText("Heater: ON")
        self.heater_label.setStyleSheet("color: white; background-color: green; padding: 4px;")

        self.exhaust_label.setText("Exhaust: ON")
        self.exhaust_label.setStyleSheet("color: white; background-color: green; padding: 4px;")

        self.time_elapsed = 0
        self.timer.start(1000)

    def update_timer(self):
        self.time_elapsed += 1

        hours = self.time_elapsed // 3600
        minutes = (self.time_elapsed % 3600) // 60
        seconds = self.time_elapsed % 60

        time_string = f"{hours:02}:{minutes:02}:{seconds:02}"
        self.timer_label.setText(f"Time: {time_string}")


app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec_())
