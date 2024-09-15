from src.connections.mqtt_client import Mqtt_client
from src.settings import *
import random
import time

r = random.randrange(1, 100000)
clientname = "IOT_client-Id-" + str(r)

class RoomTmpSensor():
    def __init__(self):
        self.mc = Mqtt_client(self, handle_message=self.handle_message)
        self.connection_status = True
        self.mc.set_broker(broker_ip)
        self.mc.set_port(int(broker_port))
        self.mc.set_clientName(clientname)
        self.mc.set_username(username)
        self.mc.set_password(password)
        self.topic = ac_topic
        self.mc.connect_to()

        self.room_tmp = 25
        self.room_tmp_max = 32.0
        self.room_tmp_min = 24

        self.ac_status = "OFF"

    def sensor_producer_loop(self):
        while True:
            message = "roomTmp " + str(round(self.room_tmp, 1))

            if self.ac_status == "OFF":
                if self.room_tmp < self.room_tmp_max:
                    self.room_tmp += 0.1
                    self.mc.publish_to(self.topic , message)
                else:
                    self.mc.publish_to(self.topic , message)
                time.sleep(5)

            if self.ac_status == "ON":
                if self.room_tmp > self.room_tmp_min:
                    self.room_tmp -= 0.1
                    self.mc.publish_to(self.topic , message)
                else:
                    self.mc.publish_to(self.topic , message)

                time.sleep(5)

    def sensor_consumer_loop(self):
        self.mc.start_listening()
        self.mc.subscribe_to(self.topic)

    def handle_message(self, message):
        key = str(message.split()[0])
        value = str(message.split()[1])
        if key == "AC":
            self.ac_status = value