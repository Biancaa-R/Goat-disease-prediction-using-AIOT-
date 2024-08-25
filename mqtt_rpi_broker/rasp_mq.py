#mqtt for sending messages:
import time
import random
import paho.mqtt.client as mqtt
hostname = "localhost"
broker_port = 1883
topic = "esp8266"
client = mqtt.Client()

def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker with result code: " + str(rc))
    client.subscribe(topic)

def on_message(client, userdata, msg):
    global antharax_det
    global tetanus_det
     #print("Message received: " + msg.payload.decode())
    print(f"Received message: {msg.payload.decode()} on topic {msg.topic}")
    message= (msg.payload.decode()).split(",");
    temp=message[0]
    motion=message[1]
    pulse=message[2]
    #list1=[pulse,motion,temp]
    #70–130 beats per minute.
    if (int(pulse)>140):
        tetanus_det=1
    if (float(temp)>40):
        antharax_det=1
    #38.5–39.7
#creation of client object
client.on_connect=on_connect
client.on_message=on_message
client.connect(hostname, broker_port, 60)
start=time.time()
#message = str(random.randint(1, 100))
#client.publish(topic, message)
while(True):
    client.loop_start()
    stop=time.time()
    if (stop-start> 7200):
        if (antharax_det==1):
            pass
        if(tetanus_det==1):
            pass
        start=time.time()
        antharax_det=0
        tetanus_det=0

    #Start the MQTT client's network loop by calling the loop_start() method to begin receiving messages.\


