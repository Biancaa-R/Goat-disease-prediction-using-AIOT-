# Goat-disease-prediction-using-AIOT-
project for predicting goat disease using AIOT

for now the diseases considered:

1.ppr-scabby mouth

2.Tetanus

3.Antharax

4.Goat pox


MQTT:

1. https://www.emqx.com/en/blog/esp8266_mqtt_led
2. https://www.emqx.com/en/blog/esp32-connects-to-the-free-public-mqtt-broker
3. https://www.emqx.com/en/blog/use-mqtt-with-raspberry-pi
4. https://www.aranacorp.com/en/udp-communication-between-raspberry-pi-and-esp32/#:~:text=Code%20ESP32%20UDP%20Client,network%20as%20the%20Raspberry%20Pi.
5. https://helloworld.co.in/article/mqtt-raspberry-pi-esp32

IP:
1. https://www.kaspersky.com/resource-center/definitions/what-is-an-ip-address
2. https://www.geeksforgeeks.org/structure-and-types-of-ip-address/

Note: Initial attempt to use tensorflow api for bounding boxes is set for future and I decided to go with YOLOv8n instead as there were unresolved version clashes when using tf api with 1 and 2 ...YOLO   was an easier option to try. So probably in future I would fix the bugs with tensor api (seems quite unlikely now)

The .pt YOLO v8 model was converted to onnx for deployment in raspberrypi 4b .The result of the form (x,y,h,w) is used for the generation of bounding boxes.

Tool used for annotation: LabelImg
from the xml files , annotations were converted to yolo 1.1 format ie txt
