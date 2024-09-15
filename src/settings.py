import socket


##General MQTT settings
nb=1 # 0- HIT-"139.162.222.115", 1 - open HiveMQ - broker.hivemq.com
brokers=[str(socket.gethostbyname('vmm1.saaintertrade.com')), str(socket.gethostbyname('broker.hivemq.com'))]
ports=['80','1883']
usernames = ['MATZI',''] # should be modified for HIT
passwords = ['MATZI',''] # should be modified for HIT
broker_ip=brokers[nb]
port=ports[nb]
username = usernames[nb]
password = passwords[nb]
conn_time = 0 # 0 stands for endless
mzs=['matzi/','']
sub_topics =[mzs[nb]+'matzi/206056905/#','matzi/206056905/#']
pub_topics = [mzs[nb]+'matzi/206056905/all','matzi/206056905/all']

broker_ip=brokers[nb]
broker_port=ports[nb]
username = usernames[nb]
password = passwords[nb]
sub_topic = sub_topics[nb]
pub_topic = pub_topics[nb]

update_rate = 5000
# plants_topic = 'matzi/206056905/plants'

##Fishtank default params:
fishtank_topic = 'matzi/206056905/fishtank'
fishtank_control = 'matzi/206056905/fishtank_control'
min_tmp_threshold="24"
max_tmp_threshold="26.5"
min_ox_level="6.4"
max_ox_level="7.0"
fishtank_db_name="fishtank_data"

##Ac default params:
ac_topic = 'matzi/206056905/ac'
ac_db_name="room_tmp_data"

##Door sensor default params:
door_sensor_topic = 'matzi/206056905/door_sensor'
door_sensor_db_name="door_sensor_data"
phone_number="+972508080050"
email="test@example.com"

##DB params:
db_path="db/sensors.db"