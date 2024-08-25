#mqtt for sending messages:
import time
import random
import paho.mqtt.client as mqtt
hostname = "raspberrypi" #should be local host or ip address of rpi
broker_port = 1883
topic = "testtopic"
client = mqtt.Client()

def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker with result code: " + str(rc))
    client.subscribe(topic)

def on_message(client, userdata, msg):
     print("Message received: " + msg.payload.decode())
#creation of client object
client.on_connect=on_connect
client.on_message=on_message
client.connect(hostname, broker_port, 60)
message = str(random.randint(1, 100))
client.publish(topic, message)

client.loop_start()
#Start the MQTT client's network loop by calling the loop_start() method to begin receiving messages.\

