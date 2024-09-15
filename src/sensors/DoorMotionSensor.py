from src.connections.mqtt_client import Mqtt_client
from src.settings import *
import random
import time

r = random.randrange(1, 100000)
clientname = "IOT_client-Id-" + str(r)

class DoorMotionSensor():
    def __init__(self):
        self.mc = Mqtt_client(self, handle_message=self.handle_message)
        self.connection_status = True
        self.mc.set_broker(broker_ip)
        self.mc.set_port(int(broker_port))
        self.mc.set_clientName(clientname)
        self.mc.set_username(username)
        self.mc.set_password(password)
        self.topic = door_sensor_topic
        self.mc.connect_to()

        self.door_alert = "None"


    def sensor_producer_loop(self):
        while True:
            r =random.randrange(1, 100)
            if r > 70:
                if self.door_alert == "None":
                    self.door_alert = "Detected"
                    message = f'Motion {self.door_alert}'
                    self.mc.publish_to(self.topic, message)
            else:
                if self.door_alert == "Detected":
                    self.door_alert = "None"
                    message = f'Motion {self.door_alert}'
                    self.mc.publish_to(self.topic, message)
            time.sleep(5)

    def sensor_consumer_loop(self):
        self.mc.start_listening()
        self.mc.subscribe_to(self.topic)

    def handle_message(self, message):
        key = str(message.split()[0])
        value = str(message.split()[1])