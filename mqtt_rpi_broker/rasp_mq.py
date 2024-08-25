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
    global antharax_det
    global tetanus_det
     #print("Message received: " + msg.payload.decode())
    print(f"Received message: {msg.payload.decode()} on topic {msg.topic}")
    message= list(msg.payload.decode());
    pulse=message[0]
    motion=message[1]
    temp=message[2]
    #list1=[pulse,motion,temp]
    #70–130 beats per minute.
    if (pulse>140):
        tetanus_det=1
    if (temp>40):
        antharax_det=1
    #38.5–39.7
#creation of client object
client.on_connect=on_connect
client.on_message=on_message
client.connect(hostname, broker_port, 60)
start=time.time.now()
#message = str(random.randint(1, 100))
#client.publish(topic, message)
while(True):
    client.loop_start()
    stop=time.time.now()
    if (stop-start> 7200):
        if (antharax_det==1):
            pass
        if(tetanus_det==1):
            pass
        start=time.time.now()
        antharax_det=0
        tetanus_det=0

    #Start the MQTT client's network loop by calling the loop_start() method to begin receiving messages.\


