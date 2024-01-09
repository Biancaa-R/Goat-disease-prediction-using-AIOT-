#include <WiFi.h>
#include <WiFiUdp.h>
WiFiUDP udp;

//udp.parsePacket() checks if there is an incoming UDP packet. If a packet is received,
// it prints information about the sender's IP address and reads the data into the packetBuffer.

char packetBuffer[255];
unsigned int localPort = 9999;
char *serverip = "192.168.1.46";
//ip of the rpi
unsigned int serverport = 8888;

const char *ssid = "******";
const char *password = "********";

void setup() {
 	Serial.begin(115200);
 	// Connect to Wifi network.
 	WiFi.begin(ssid, password);
 	while (WiFi.status() != WL_CONNECTED) {
 			delay(500); Serial.print(F("."));
 	}
 	udp.begin(localPort);
 	Serial.printf("UDP Client : %s:%i \n", WiFi.localIP().toString().c_str(), localPort);
}

void loop() {
 	int packetSize = udp.parsePacket();
 	if (packetSize) {
 			Serial.print(" Received packet from : "); Serial.println(udp.remoteIP());
 			int len = udp.read(packetBuffer, 255);
 			Serial.printf("Data : %s\n", packetBuffer);
 			Serial.println();
 	}
 	delay(500);
 	Serial.print("[Client Connected] "); Serial.println(WiFi.localIP());
 	udp.beginPacket(serverip, serverport);
 	char buf[30];
 	unsigned long testID = millis();
 	sprintf(buf, "ESP32 send millis: %lu", testID);
 	udp.printf(buf);
 	udp.endPacket();
}

// udp.beginPacket(serverip, serverport);: Initiates the preparation of a UDP packet to be sent to the server. It specifies the destination IP address (serverip) and port (serverport) to which the packet will be sent.

// unsigned long testID = millis();: Retrieves the current value of the millis() function, which returns the number of milliseconds since the ESP32 started running.

// sprintf(buf, "ESP32 send millis: %lu", testID);: Formats the data into a string (buf). It creates a message that includes the text "ESP32 send millis:" followed by the current millis() value.

// udp.printf(buf);: Sends the formatted string as the payload of the UDP packet.

// udp.endPacket();: Finalizes and sends the UDP packet to the specified server IP and port.


