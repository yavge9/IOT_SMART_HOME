from src.connections.mqtt_client import Mqtt_client
from src.settings import *
import random
import time

r = random.randrange(1, 100000)
clientname = "IOT_client-Id-" + str(r)

class FishTankSensor():
    def __init__(self):
        self.mc = Mqtt_client(self, handle_message=self.handle_message)
        self.connection_status = True
        self.mc.set_broker(broker_ip)
        self.mc.set_port(int(broker_port))
        self.mc.set_clientName(clientname)
        self.mc.set_username(username)
        self.mc.set_password(password)
        self.topic = fishtank_topic
        self.fishtank_control = fishtank_control
        self.mc.connect_to()

        self.pump_status = "OFF"
        self.food_dispenser = "OFF"

    def sensor_producer_loop(self):
        while True:
            temp = random.randrange(200, 300) / 10
            oxygen = 6 + random.randrange(1, 20) / 10
            current_data = 'Temperature ' + str(temp) + ' Oxyegen ' + str(oxygen)
            if self.mc.isConnected:
                self.mc.publish_to(self.topic, current_data)
            else:
                print("Client not connected")
            time.sleep(5)

    def sensor_consumer_loop(self):
        self.mc.start_listening()
        self.mc.subscribe_to(self.fishtank_control)

    def handle_message(self, message):
        key = str(message.split()[0])
        value = str(message.split()[1])

        if key == "Pump":
            self.pump_status = value

        if key == "FOOD":
            self.food_dispenser = value