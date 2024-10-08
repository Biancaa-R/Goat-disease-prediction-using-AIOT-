

//#include <WiFi.h>
#include <ESP8266WiFi.h>
// Add other necessary includes and code below
#include <PubSubClient.h>
#include <PulseSensorPlayground.h>
#include <Adafruit_Sensor.h>
#include "DHT.h"

// Replace the SSID/Password details as per your wifi router
const char* ssid = "Xiaomi 11i";
const char* password = "goodthing";

// Replace your MQTT Broker IP address here:
const char* mqtt_server = "192.168.90.246";

WiFiClient espClient;
PubSubClient client(espClient);

long lastMsg = 0;

#define ledPin 2
int sensor = 13;  // Digital pin D7
#define DPIN 4        // Pin to connect DHT sensor (GPIO number) D2
#define DTYPE DHT11   // Define DHT 11 or DHT22 sensor 
const int pulsePin = A0;

DHT dht(DPIN, DTYPE);
// Create an instance of the pulse sensor
PulseSensorPlayground pulseSensor;

void blink_led(unsigned int times, unsigned int duration){
  for (int i = 0; i < times; i++) {
    digitalWrite(ledPin, HIGH);
    delay(duration);
    digitalWrite(ledPin, LOW); 
    delay(200);
  }
}

void setup_wifi() {
  delay(50);
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);

  WiFi.begin(ssid, password);

  int c=0;
  while (WiFi.status() != WL_CONNECTED) {
    blink_led(2,200); //blink LED twice (for 200ms ON time) to indicate that wifi not connected
    delay(1000); //
    Serial.print(".");
    c=c+1;
    if(c>10){
        ESP.restart(); //restart ESP after 10 seconds
    }
  }

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
  
}

void connect_mqttServer() {
  // Loop until we're reconnected
  while (!client.connected()) {

        //first check if connected to wifi
        if(WiFi.status() != WL_CONNECTED){
          //if not connected, then first connect to wifi
          setup_wifi();
        }

        //now attemt to connect to MQTT server
        Serial.print("Attempting MQTT connection...");
        // Attempt to connect
        if (client.connect("esp8266")) { // Change the name of client here if multiple ESP32 are connected
          //attempt successful
          Serial.println("connected");
          // Subscribe to topics here
          client.subscribe("esp8266");
          //client.subscribe("rpi/xyz"); //subscribe more topics here
          
        } 
        else {
          //attempt not successful
          Serial.print("failed, rc=");
          Serial.print(client.state());
          Serial.println(" trying again in 2 seconds");
    
          blink_led(3,200); //blink LED three times (200ms on duration) to show that MQTT server connection attempt failed
          // Wait 2 seconds before retrying
          delay(2000);
        }
  }
  
}

//this function will be executed whenever there is data available on subscribed topics
void callback(char* topic, byte* message, unsigned int length) {
  Serial.print("Message arrived on topic: ");
  Serial.print(topic);
  Serial.print(". Message: ");
  String messageTemp;
  
  for (int i = 0; i < length; i++) {
    Serial.print((char)message[i]);
    messageTemp += (char)message[i];
  }
  Serial.println();

  // Check if a message is received on the topic "rpi/broadcast"
  if (String(topic) == "esp8266") {
      if(messageTemp == "15"){
        Serial.println("Action: blink LED");
        blink_led(1,1250); //blink LED once (for 1250ms ON time)
      }
  }

  //Similarly add more if statements to check for other subscribed topics 
}

void setup() {
  pinMode(sensor, INPUT);   // Declare sensor as input
  pinMode(ledPin, OUTPUT);
  Serial.begin(115200);

  pulseSensor.analogInput(pulsePin);
  pulseSensor.begin();
  pulseSensor.setThreshold(55);

  setup_wifi();
  client.setServer(mqtt_server,1883);//1883 is the default port for MQTT server
  client.setCallback(callback);
}

void loop() {

   // Update the pulse sensor
  int pulse = pulseSensor.getBeatsPerMinute();
  long state = digitalRead(sensor);
  if (state == HIGH) {
    //Serial.println("Motion detected!");
    int motion=1;
  } else {
    //Serial.println("Motion absent!");
    int motion=0;
  }

  float tc = dht.readTemperature();  // Read temperature in Celsius
  if (isnan(tc)) {
    Serial.println("Failed to read from DHT11 sensor");
  } else {
    tc=int(tc);
  }
  
  if (!client.connected()) {
    connect_mqttServer();
  }

  client.loop();
  
  long now = millis();
  if (now - lastMsg > 4000) {
    lastMsg = now;
    float arr1 ={pulse,motion,tc};
    client.publish("esp8266",arr1); 
    
  }
  
}