#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include <WiFiClientSecure.h>  // Include the secure WiFi client

// WiFi settings
const char *ssid = "Xiaomi 11i";             // Replace with your WiFi name
const char *password = "goodthing";   // Replace with your WiFi password

// MQTT Broker settings
const char *mqtt_broker = "a1b07db6.ala.asia-southeast1.emqxsl.com";  // EMQX broker endpoint
const char *mqtt_topic = "testtopic/1";     // MQTT topic
const char *mqtt_username = "mqtt";  // MQTT username for authentication
const char *mqtt_password = "goat";  // MQTT password for authentication
const int mqtt_port = 8883;  // MQTT port for TLS (SSL)

WiFiClientSecure espClientSecure;  // Secure WiFi client
PubSubClient mqtt_client(espClientSecure);

void connectToWiFi();

void connectToMQTTBroker();

void mqttCallback(char *topic, byte *payload, unsigned int length);

void setup() {
    Serial.begin(115200);
    connectToWiFi();
    
    // Set up TLS/SSL certificates (optional, depending on your broker's settings)
    espClientSecure.setInsecure(); // Use this for testing purposes only (disables certificate validation)
    
    mqtt_client.setServer(mqtt_broker, mqtt_port);
    mqtt_client.setCallback(mqttCallback);
    connectToMQTTBroker();
}

void connectToWiFi() {
    WiFi.begin(ssid, password);
    Serial.print("Connecting to WiFi");
    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
    }
    Serial.println("\nConnected to the WiFi network");
}

void connectToMQTTBroker() {
    while (!mqtt_client.connected()) {
        String client_id = "esp8266-client-" + String(WiFi.macAddress());
        Serial.printf("Connecting to MQTT Broker as %s.....\n", client_id.c_str());
        if (mqtt_client.connect(client_id.c_str(), mqtt_username, mqtt_password)) {
            Serial.println("Connected to MQTT broker");
            mqtt_client.subscribe(mqtt_topic);
            // Publish message upon successful connection
            mqtt_client.publish(mqtt_topic, "Hi EMQX I'm ESP8266 ^^");
        } else {
            Serial.print("Failed to connect to MQTT broker, rc=");
            Serial.print(mqtt_client.state());
            Serial.println(" try again in 5 seconds");
            delay(5000);
        }
    }
}

void mqttCallback(char *topic, byte *payload, unsigned int length) {
    Serial.print("Message received on topic: ");
    Serial.println(topic);
    Serial.print("Message:");
    for (unsigned int i = 0; i < length; i++) {
        Serial.print((char) payload[i]);
    }
    Serial.println();
    Serial.println("-----------------------");
}

void loop() {
    if (!mqtt_client.connected()) {
        connectToMQTTBroker();
    }
    mqtt_client.loop();
}
