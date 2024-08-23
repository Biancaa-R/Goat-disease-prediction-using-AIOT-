import paho.mqtt.client as mqtt 
import ssl

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected successfully")
        # Subscribe to a topic after connecting
        client.subscribe("testtopic/1")
        client.publish("testtopic/1", "Hello, this is a test message!")
    else:
        print(f"Connection failed with code {rc}")

# Callback function for when a message is received
def on_message(client, userdata, msg):
    print(f"Received message: {msg.payload.decode()} on topic {msg.topic}")

client = mqtt.Client()

# Set username and password
client.username_pw_set("mqtt", "goat")

# Enable SSL/TLS
client.tls_set(cert_reqs=ssl.CERT_NONE)  # or specify your CA certificate

# If using a self-signed certificate, you may want to disable certificate verification
client.tls_insecure_set(True)

client.on_connect = on_connect 
client.on_message = on_message 

client.connect("a1b07db6.ala.asia-southeast1.emqxsl.com", 8883, 60) 
client.loop_forever()
