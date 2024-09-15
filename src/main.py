import sys
from PyQt5.QtCore import *
from views.views import *
import threading
from sensors.RoomTmpSensor import RoomTmpSensor
from sensors.FishTankSensor import FishTankSensor
from sensors.DoorMotionSensor import DoorMotionSensor

# Creating Client name - should be unique
r = random.randrange(1, 100000)
clientname = "IOT_client-Id-" + str(r)


class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)

        # Init of Mqtt_client class
        self.mc = Mqtt_client(self)

        # general GUI settings
        self.setUnifiedTitleAndToolBarOnMac(True)

        # set up main window
        self.setGeometry(30, 100, 900, 700)
        self.setWindowTitle('Monitor GUI')

        # Init QDockWidget objects
        self.publishDock = PublishDock(self.mc)
        self.subscribeDock = SubscribeDock(self.mc)
        self.fishTankDock = FishTankDock(clientname)
        self.acDock = AcDock(clientname)
        self.doorMotionSensorDock = DoorMotionSensorDock(clientname)
        self.connectionDock = ConnectionDock(self.mc,clientname,[self.fishTankDock, self.acDock,self.doorMotionSensorDock])

        self.addDockWidget(Qt.TopDockWidgetArea, self.connectionDock)
        self.addDockWidget(Qt.TopDockWidgetArea, self.publishDock)
        self.addDockWidget(Qt.TopDockWidgetArea, self.subscribeDock)
        self.addDockWidget(Qt.BottomDockWidgetArea, self.fishTankDock)
        self.addDockWidget(Qt.BottomDockWidgetArea, self.acDock)
        self.addDockWidget(Qt.BottomDockWidgetArea, self.doorMotionSensorDock)

def create_sensors():
    sensors = []
    room_sensor = RoomTmpSensor()
    fishtank_sensor = FishTankSensor()
    door_sensor = DoorMotionSensor()
    sensors.append(room_sensor)
    sensors.append(fishtank_sensor)
    sensors.append(door_sensor)
    return sensors

def start_sensors_producer(sensor):
    print(f"Starting producer for sensor {sensor}")
    sensor.sensor_producer_loop()

def start_sensors_consumer(sensor):
    print(f"Starting consumer for sensor {sensor}")
    sensor.sensor_consumer_loop()

def main():
    sensors = create_sensors()

    for sensor in sensors:
        thread_producer = threading.Thread(target=start_sensors_producer, args=(sensor,))
        thread_producer.daemon = True
        thread_producer.start()
        thread_consumer = threading.Thread(target=start_sensors_consumer, args=(sensor,))
        thread_consumer.daemon = True
        thread_consumer.start()

    app = QApplication(sys.argv)
    mainwin = MainWindow()
    mainwin.show()
    app.exec_()

if __name__ == '__main__':
    # init_db()
    main()