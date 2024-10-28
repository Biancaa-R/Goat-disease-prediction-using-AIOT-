#include <ESP8266WiFi.h>
#include "ThingSpeak.h"
#include <WiFiClient.h>
#include <PulseSensorPlayground.h>
#include <Adafruit_Sensor.h>
#include "DHT.h"

const char* ssid = "Xiaomi 11i";   // your network SSID (name) 
const char* password = "goodthing";   // your network password

WiFiClient client;

unsigned long myChannelNumber = 2608946;
const char* myWriteAPIKey = "OWSF04ZGIXBJ3RIR";

int sensor = 13;  // Digital pin D7

#define DPIN 4        // Pin to connect DHT sensor (GPIO number) D2
#define DTYPE DHT11   // Define DHT 11 or DHT22 sensor type

DHT dht(DPIN, DTYPE);
// Create an instance of the pulse sensor
PulseSensorPlayground pulseSensor;

void setup() {
  Serial.begin(115200);  // Initialize serial
  WiFi.mode(WIFI_STA);

  ThingSpeak.begin(client);  // Initialize ThingSpeak
  dht.begin();

  // Define the pin for the pulse sensor
  const int pulsePin = A0;
  pinMode(sensor, INPUT);   // Declare sensor as input

  // Connect to Wi-Fi
  WiFi.begin(ssid, password);
  unsigned long startAttemptTime = millis();
  while (WiFi.status() != WL_CONNECTED && millis() - startAttemptTime < 10000) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  if (WiFi.status() != WL_CONNECTED) {
    Serial.println("Failed to connect to WiFi");
    return;
  }
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());

  // Initialize the pulse sensor
  pulseSensor.analogInput(pulsePin);
  pulseSensor.begin();
  pulseSensor.setThreshold(55);
}

void loop() {
  // Update the pulse sensor
  int pulse = pulseSensor.getBeatsPerMinute();
  Serial.print("Heart rate: ");
  Serial.println(pulse);
  String pulses=String(pulse);



  long state = digitalRead(sensor);
  if (state == HIGH) {
    Serial.println("Motion detected!");

    }
  else {
    Serial.println("Motion absent!");
  
    }

    String states= String(state);
  

  float tc = dht.readTemperature();  // Read temperature in Celsius
  if (isnan(tc)) {
    Serial.println("Failed to read from DHT11 sensor");
  } 
  else {
    Serial.print("Temp: ");
    Serial.println(tc);
    String tcs = String(tc, 2); 
    updateThingSpeak("field1=" + pulses + "&field2=" + tcs + "&field3=" + states);

  delay(15000);  // ThingSpeak rate limit is 15 seconds
}

bool sendDataToThingSpeak(unsigned long channelNumber, unsigned int field, float value, const char* apiKey) {
  int response = ThingSpeak.writeField(channelNumber, field, String(value), apiKey);
  if (response == 200) {
    return true;
  } else {
    Serial.print("HTTP error code ");
    Serial.println(response);
    return false;
  }
}
