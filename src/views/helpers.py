from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from src.settings import *

class ConfigFishtankDialog(QDialog):
    '''
    Fishtank configuration dialog
    '''
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Configuration")

        # Create a form layout for configuration input
        layout = QFormLayout()

        self.minTmpThreshold = QLineEdit()
        self.minTmpThreshold.setText(min_tmp_threshold)

        self.maxTmpThreshold = QLineEdit()
        self.maxTmpThreshold.setText(max_tmp_threshold)

        self.minOxygenLevel = QLineEdit()
        self.minOxygenLevel.setText(min_ox_level)

        self.maxOxygenLevel = QLineEdit()
        self.maxOxygenLevel.setText(max_ox_level)

        layout.addRow("min_tmp", self.minTmpThreshold)
        layout.addRow("max_tmp", self.maxTmpThreshold)
        layout.addRow("min_ox_level", self.minOxygenLevel)
        layout.addRow("max_ox_level", self.maxOxygenLevel)

        # Add dialog buttons (OK)
        buttons = QDialogButtonBox(QDialogButtonBox.Ok)
        buttons.accepted.connect(self.accept)

        layout.addWidget(buttons)
        self.setLayout(layout)

class ConfigDoorSensorDialog(QDialog):
    '''
    Door sensor configuration dialog
    '''
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Configuration")

        # Create a form layout for configuration input
        layout = QFormLayout()

        self.phoneNumber = QLineEdit()
        self.phoneNumber.setText(phone_number)
        self.email = QLineEdit()
        self.email.setText(email)

        layout.addRow("Phone Number:", self.phoneNumber)
        layout.addRow("Email:", self.email)

        # Add dialog buttons (OK)
        buttons = QDialogButtonBox(QDialogButtonBox.Ok)
        buttons.accepted.connect(self.accept)

        layout.addWidget(buttons)
        self.setLayout(layout)