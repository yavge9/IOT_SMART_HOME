import random

# from src.settings import *
from src.connections.mqtt_client import Mqtt_client
from src.connections.db_manager import DbManager
from src.views.helpers import *
from src.views.design import *

class ConnectionDock(QDockWidget):
    """Main """

    def __init__(self, mc, clientname, widgets_to_connect=[]):
        QDockWidget.__init__(self)

        self.mc = mc
        self.mc.set_on_connected_to_form(self.on_connected)
        self.widgets_to_connect = widgets_to_connect
        self.eHostInput = QLineEdit()
        self.eHostInput.setInputMask('999.999.999.999')
        self.eHostInput.setText(broker_ip)

        self.ePort = QLineEdit()
        self.ePort.setValidator(QIntValidator())
        self.ePort.setMaxLength(4)
        self.ePort.setText(broker_port)

        self.eClientID = QLineEdit()
        self.clientname = clientname
        self.eClientID.setText(clientname)

        self.eUserName = QLineEdit()
        self.eUserName.setText(username)

        self.ePassword = QLineEdit()
        self.ePassword.setEchoMode(QLineEdit.Password)
        self.ePassword.setText(password)

        self.eKeepAlive = QLineEdit()
        self.eKeepAlive.setValidator(QIntValidator())
        self.eKeepAlive.setText("60")

        self.eSSL = QCheckBox()

        self.eCleanSession = QCheckBox()
        self.eCleanSession.setChecked(True)

        self.eConnectbtn = QPushButton("Connect", self)
        self.eConnectbtn.setToolTip("click me to connect")
        self.eConnectbtn.clicked.connect(self.on_button_connect_click)
        self.eConnectbtn.setStyleSheet(change_btn_color(color_red))
        self.button_pressed = False

        formLayot = QFormLayout()
        formLayot.addRow("Host", self.eHostInput)
        formLayot.addRow("Port", self.ePort)
        formLayot.addRow("Client ID", self.eClientID)
        formLayot.addRow("User Name", self.eUserName)
        formLayot.addRow("Password", self.ePassword)
        formLayot.addRow("Keep Alive", self.eKeepAlive)
        formLayot.addRow("SSL", self.eSSL)
        formLayot.addRow("Clean Session", self.eCleanSession)
        formLayot.addRow("", self.eConnectbtn)

        widget = QWidget(self)
        widget.setLayout(formLayot)
        self.setTitleBarWidget(widget)
        self.setWidget(widget)
        self.setWindowTitle("Connect")

    def on_connected(self):
        self.eConnectbtn.setStyleSheet(change_btn_color(color_green))

    def on_button_connect_click(self):
        self.eConnectbtn.setStyleSheet(change_btn_color(color_green))
        self.button_pressed = True
        self.connection_status = True
        self.mc.set_broker(self.eHostInput.text())
        self.mc.set_port(int(self.ePort.text()))
        self.mc.set_clientName(self.eClientID.text())
        self.mc.set_username(self.eUserName.text())
        self.mc.set_password(self.ePassword.text())
        self.mc.connect_to()
        self.mc.start_listening()

        for widget in self.widgets_to_connect:
            widget.on_button_connect_click()


class PublishDock(QDockWidget):
    """Publisher """

    def __init__(self, mc):
        QDockWidget.__init__(self)

        self.mc = mc

        self.ePublisherTopic = QLineEdit()
        self.ePublisherTopic.setText(pub_topic)

        self.eQOS = QComboBox()
        self.eQOS.addItems(["0", "1", "2"])

        self.eRetainCheckbox = QCheckBox()

        self.eMessageBox = QPlainTextEdit()
        self.ePublishButton = QPushButton("Publish", self)

        formLayot = QFormLayout()
        formLayot.addRow("Topic", self.ePublisherTopic)
        formLayot.addRow("QOS", self.eQOS)
        formLayot.addRow("Retain", self.eRetainCheckbox)
        formLayot.addRow("Message", self.eMessageBox)
        formLayot.addRow("", self.ePublishButton)

        self.ePublishButton.clicked.connect(self.on_button_publish_click)

        widget = QWidget(self)
        widget.setLayout(formLayot)
        self.setWidget(widget)
        self.setWindowTitle("Publish")

    def on_button_publish_click(self):
        if self.mc.isConnected:
            self.mc.publish_to(self.ePublisherTopic.text(), self.eMessageBox.toPlainText())
        else:
            print("Client not connected")


class SubscribeDock(QDockWidget):
    """Subscribe """

    def __init__(self, mc):
        QDockWidget.__init__(self)
        self.mc = mc
        self.mc.handle_message = self.handle_message

        self.eSubscribeTopic = QLineEdit()
        self.eSubscribeTopic.setText(sub_topic)

        self.eQOS = QComboBox()
        self.eQOS.addItems(["0", "1", "2"])

        self.eRecMess = QTextEdit()

        self.eSubscribeButton = QPushButton("Subscribe", self)
        self.eSubscribeButton.clicked.connect(self.on_button_subscribe_click)
        self.was_clicked = False

        formLayot = QFormLayout()
        formLayot.addRow("Topic", self.eSubscribeTopic)
        formLayot.addRow("QOS", self.eQOS)
        formLayot.addRow("Received", self.eRecMess)
        formLayot.addRow("", self.eSubscribeButton)

        widget = QWidget(self)
        widget.setLayout(formLayot)
        self.setWidget(widget)
        self.setWindowTitle("Subscribe")

    def on_button_subscribe_click(self):
        if self.mc.isConnected:
            if not self.was_clicked:
                self.mc.subscribe_to(self.eSubscribeTopic.text())
                self.eSubscribeButton.setStyleSheet(change_btn_color(color_navy_blue))
                self.mc.start_listening()
        else:
            print("Client not connected")

    def handle_message(self, message):
        self.eRecMess.append(message)

class FishTankDock(QDockWidget):
    """FishTankDock """
    def __init__(self, clientname):
        QDockWidget.__init__(self)
        r = random.randrange(1, 100000)
        clientname = "IOT_client-Id-" + str(r)

        self.mc = Mqtt_client(self, handle_message=self.handle_message)
        self.mc.set_on_connected_to_form(self.on_connected)

        self.db = DbManager(fishtank_db_name, 'temperature REAL, oxygen REAL, pump TEXT')
        self.db.init_db()


        self.eHostInput = QLineEdit()
        self.eHostInput.setInputMask('999.999.999.999')
        self.eHostInput.setText(broker_ip)

        self.ePort = QLineEdit()
        self.ePort.setValidator(QIntValidator())
        self.ePort.setMaxLength(4)
        self.ePort.setText(broker_port)

        self.eClientID = QLineEdit()
        self.clientname = clientname
        self.eClientID.setText(clientname)

        self.eUserName = QLineEdit()
        self.eUserName.setText(username)

        self.ePassword = QLineEdit()
        self.ePassword.setEchoMode(QLineEdit.Password)
        self.ePassword.setText(password)

        self.eKeepAlive = QLineEdit()
        self.eKeepAlive.setValidator(QIntValidator())
        self.eKeepAlive.setText("60")

        self.eSSL = QCheckBox()

        self.eCleanSession = QCheckBox()
        self.eCleanSession.setChecked(True)

        self.eConnectbtn = QPushButton("", self)
        self.eConnectbtn.setDisabled(True)
        self.eConnectbtn.setStyleSheet(change_btn_color(color_gray))

        self.pumpStatus = "OFF"
        self.ePumpStatus = QPushButton(self.pumpStatus, self)
        self.ePumpStatus.setDisabled(True)
        self.fishtankControlTopic = fishtank_control

        self.ePublisherTopic = QLineEdit()
        self.ePublisherTopic.setText(fishtank_topic)
        self.eSubscribeTopic = fishtank_topic

        self.Temperature = QLineEdit()
        self.Temperature.setText('')

        self.Oxygen = QLineEdit()
        self.Oxygen.setText('')

        self.food_dispancer = QPushButton("Drop food", self)
        self.food_dispancer.clicked.connect(self.push_button_click)

        self.configurations = ConfigFishtankDialog()
        self.configurationPanel = QPushButton("Configure", self)
        self.configurationPanel.clicked.connect(self.open_configuration)


        formLayot = QFormLayout()
        formLayot.addRow("Connection status:", self.eConnectbtn)
        formLayot.addRow("topic", self.ePublisherTopic)
        formLayot.addRow("Temperature (°C)", self.Temperature)
        formLayot.addRow("Oxygen (mg/liter)", self.Oxygen)
        formLayot.addRow("", self.food_dispancer)
        formLayot.addRow("Pump", self.ePumpStatus)
        formLayot.addRow("" ,self.configurationPanel)

        widget = QWidget(self)
        widget.setLayout(formLayot)
        self.setTitleBarWidget(widget)
        self.setWidget(widget)
        self.setWindowTitle("Fishtank")

    def on_connected(self):
        self.eConnectbtn.setStyleSheet(change_btn_color(color_green))

    def on_button_connect_click(self):
        self.mc.set_broker(self.eHostInput.text())
        self.mc.set_port(int(self.ePort.text()))
        self.mc.set_clientName(self.eClientID.text())
        self.mc.set_username(self.eUserName.text())
        self.mc.set_password(self.ePassword.text())
        self.mc.connect_to()
        self.mc.start_listening()
        self.mc.subscribe_to(self.eSubscribeTopic)

    def open_configuration(self):
        self.configurations.exec_()

    def handle_message(self, message):
        ''' Parse message and update the database and the GUI '''

        tmp = float(message.split()[1])
        oxygen = float(message.split()[3])
        data_to_update = (tmp, oxygen, self.pumpStatus)
        self.db.insert_data(data_to_update)

        self.Temperature.setText(str(tmp))
        self.Oxygen.setText(str(oxygen))

        if ((tmp > float(self.configurations.maxTmpThreshold.text()) or tmp < float(self.configurations.minTmpThreshold.text())) and
                (oxygen > float(self.configurations.maxOxygenLevel.text()) or oxygen < float(self.configurations.minOxygenLevel.text()))):
            if self.pumpStatus == "OFF":
                self.pumpStatus = "ON"
                self.mc.publish_to(self.fishtankControlTopic, f"pump {self.pumpStatus}")
                self.ePumpStatus.setStyleSheet(change_btn_color(color_green))
                self.ePumpStatus.setText(self.pumpStatus)
            else:
                if self.pumpStatus == "ON":
                    self.pumpStatus = "OFF"
                    self.mc.publish_to(self.fishtankControlTopic, f"pump {self.pumpStatus}")
                    self.ePumpStatus.setStyleSheet(change_btn_color(color_gray))
                    self.ePumpStatus.setText(self.pumpStatus)

    def push_button_click(self):
        print("Dispense food")
        self.mc.publish_to(self.fishtankControlTopic, "food Dispense")

class AcDock(QDockWidget):
    '''AcDock'''''

    def __init__(self, clientname):
        QDockWidget.__init__(self)
        r = random.randrange(1, 100000)
        clientname = "IOT_client-Id-" + str(r)

        self.mc = Mqtt_client(self, handle_message=self.handle_message)
        self.mc.set_on_connected_to_form(self.on_connected)

        self.db = DbManager(ac_db_name, 'temperature REAL, AC TEXT')
        self.db.init_db()


        self.eHostInput = QLineEdit()
        self.eHostInput.setInputMask('999.999.999.999')
        self.eHostInput.setText(broker_ip)

        self.ePort = QLineEdit()
        self.ePort.setValidator(QIntValidator())
        self.ePort.setMaxLength(4)
        self.ePort.setText(broker_port)

        self.eClientID = QLineEdit()
        self.clientname = clientname
        self.eClientID.setText(self.clientname)

        self.eUserName = QLineEdit()
        self.eUserName.setText(username)

        self.ePassword = QLineEdit()
        self.ePassword.setEchoMode(QLineEdit.Password)
        self.ePassword.setText(password)

        self.eKeepAlive = QLineEdit()
        self.eKeepAlive.setValidator(QIntValidator())
        self.eKeepAlive.setText("60")

        self.eSSL = QCheckBox()

        self.eCleanSession = QCheckBox()
        self.eCleanSession.setChecked(True)

        self.eConnectbtn = QPushButton("", self)
        self.eConnectbtn.setDisabled(True)
        self.eConnectbtn.setStyleSheet(change_btn_color(color_gray))

        self.ac_status = "OFF"
        self.ePushtbtn = QPushButton(self.ac_status, self)
        self.ePushtbtn.setToolTip("Push me to turn on AC")
        self.ePushtbtn.clicked.connect(self.push_button_click)
        self.ePushtbtn.setStyleSheet(change_btn_color(color_red))

        self.ePublisherTopic = QLineEdit()
        self.ePublisherTopic.setText(ac_topic)

        self.roomTemperature = QLineEdit()
        self.roomTemperature.setText('')


        formLayot = QFormLayout()
        formLayot.addRow("Connection status:", self.eConnectbtn)
        formLayot.addRow("topic", self.ePublisherTopic)
        formLayot.addRow("Room temp (°C)", self.roomTemperature)
        formLayot.addRow("AC status", self.ePushtbtn)

        widget = QWidget(self)
        widget.setLayout(formLayot)
        self.setTitleBarWidget(widget)
        self.setWidget(widget)
        self.setWindowTitle("AC")

    def on_connected(self):
        self.eConnectbtn.setStyleSheet(change_btn_color(color_green))

    def on_button_connect_click(self):
        self.mc.set_broker(self.eHostInput.text())
        self.mc.set_port(int(self.ePort.text()))
        self.mc.set_clientName(self.eClientID.text())
        self.mc.set_username(self.eUserName.text())
        self.mc.set_password(self.ePassword.text())
        self.mc.connect_to()
        self.mc.start_listening()
        self.mc.subscribe_to(self.ePublisherTopic.text())

    def push_button_click(self):
        if self.ac_status == "OFF":
            self.ac_status = "ON"
            self.ePushtbtn.setStyleSheet(change_btn_color(color_green))
            self.ePushtbtn.setText(self.ac_status)
            self.mc.publish_to(self.ePublisherTopic.text(), "AC ON")
        else:
            self.ac_status = "OFF"
            self.ePushtbtn.setStyleSheet(change_btn_color(color_red))
            self.ePushtbtn.setText(self.ac_status)
            self.mc.publish_to(self.ePublisherTopic.text(), "AC OFF")

    def handle_message(self, message):
        key = str(message.split()[0])
        value = str(message.split()[1])

        if key == "roomTmp":
            self.roomTemperature.setText(value)
            data = (float(value), self.ac_status)

            self.db.insert_data(data)

class DoorMotionSensorDock(QDockWidget):
    '''DoorMotionSensorDock'''''

    def __init__(self, clientname):
        QDockWidget.__init__(self)
        r = random.randrange(1, 100000)
        clientname = "IOT_client-Id-" + str(r)

        self.mc = Mqtt_client(self,handle_message=self.handle_message)
        self.mc.set_on_connected_to_form(self.on_connected)

        self.db = DbManager(door_sensor_db_name, 'motion TEXT, sms_sent_to TEXT, email_sent_to TEXT, alert BOOL')
        self.db.init_db()

        self.eHostInput = QLineEdit()
        self.eHostInput.setInputMask('999.999.999.999')
        self.eHostInput.setText(broker_ip)

        self.ePort = QLineEdit()
        self.ePort.setValidator(QIntValidator())
        self.ePort.setMaxLength(4)
        self.ePort.setText(broker_port)

        self.eClientID = QLineEdit()
        self.clientname = clientname
        self.eClientID.setText(self.clientname)

        self.eUserName = QLineEdit()
        self.eUserName.setText(username)

        self.ePassword = QLineEdit()
        self.ePassword.setEchoMode(QLineEdit.Password)
        self.ePassword.setText(password)

        self.eKeepAlive = QLineEdit()
        self.eKeepAlive.setValidator(QIntValidator())
        self.eKeepAlive.setText("60")

        self.eSSL = QCheckBox()

        self.eCleanSession = QCheckBox()
        self.eCleanSession.setChecked(True)

        self.eConnectbtn = QPushButton("", self)
        self.eConnectbtn.setDisabled(True)
        self.eConnectbtn.setStyleSheet(change_btn_color(color_gray))

        self.eStatusBtn = QPushButton("", self)
        self.eStatusBtn.setDisabled(True)
        self.eStatusBtn.setStyleSheet(change_btn_color(color_gray))

        self.ePublisherTopic = QLineEdit()
        self.ePublisherTopic.setText(door_sensor_topic)

        self.configurations = ConfigDoorSensorDialog()
        self.configurationPanel = QPushButton("Configure", self)
        self.configurationPanel.clicked.connect(self.open_configuration)

        self.motion_detected = "None"
        self.alert = 0

        formLayot = QFormLayout()
        formLayot.addRow("Connection status", self.eConnectbtn)
        formLayot.addRow("topic", self.ePublisherTopic)
        formLayot.addRow("Motion detected", self.eStatusBtn)
        formLayot.addRow("\n", self.configurationPanel)
        # formLayot.setAlignment(Qt.AlignCenter)

        widget = QWidget(self)
        widget.setLayout(formLayot)
        self.setTitleBarWidget(widget)
        self.setWidget(widget)
        self.setWindowTitle("Door sensor")

    def on_connected(self):
        self.eConnectbtn.setStyleSheet(change_btn_color(color_green))

    def open_configuration(self):
        self.configurations.exec_()

    def on_button_connect_click(self):
        self.mc.set_broker(self.eHostInput.text())
        self.mc.set_port(int(self.ePort.text()))
        self.mc.set_clientName(self.eClientID.text())
        self.mc.set_username(self.eUserName.text())
        self.mc.set_password(self.ePassword.text())
        self.mc.connect_to()
        self.mc.start_listening()
        self.mc.subscribe_to(self.ePublisherTopic.text())

    def handle_message(self, message):
        message = message.split()[1]

        if message == "Detected":
            print("Alert Motion near the door detected")
            print("Sending SMS and Email message: someone is at the door, open link to view the door camera: https://example.com")
            print(f"Message sent to phone and sms {self.configurations.phoneNumber.text()} {self.configurations.email.text()}")

            self.alert =1
            self.eStatusBtn.setStyleSheet(change_btn_color(color_orange))
            data = (message, self.configurations.phoneNumber.text(), self.configurations.email.text(), self.alert)
        else:
            self.alert = 0
            self.eStatusBtn.setStyleSheet(change_btn_color(color_gray))
            data = (message, "None", "None", self.alert)

        self.db.insert_data(data)
