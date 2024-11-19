# Goat-disease-prediction-using-AIOT-
project for predicting goat disease using AIOT

The common diseases considered:

1.ppr-scabby mouth

2.Tetanus

3.Antharax

4.Goat pox

Documentation:

1. Plan of action/ deliverables: https://github.com/Biancaa-R/Goat-disease-prediction-using-AIOT-/tree/main/Goat_disease/DOCS
2. Final docs: https://github.com/Biancaa-R/Goat-disease-prediction-using-AIOT-/tree/main/Goat_disease/data
3. Flask app for notificaton: https://github.com/Biancaa-R/Goat-disease-prediction-using-AIOT-/tree/main/Goat_disease/goat_disease_flask/goat_disease_flask

Access specific:
1. dataset before xml annotation: https://github.com/Biancaa-R/Goat-disease-prediction-using-AIOT-/tree/main/Goat_disease/images_collected
2. converted ONNX model deployed in Raspberry pi4b : https://github.com/Biancaa-R/Goat-disease-prediction-using-AIOT-/tree/main/Goat_disease/rpi_model
3. Checking sensor reading with thinkspeak cloud: https://github.com/Biancaa-R/Goat-disease-prediction-using-AIOT-/tree/main/Goat_disease/sensor_connect ( Checking purpose)
4. MQTT with emqx as the mqtt broker (connecting both rpi and esp8266): https://github.com/Biancaa-R/Goat-disease-prediction-using-AIOT-/tree/main/emqx_tools_mqtt (possible use)
5. MQTT with raspberrypi broker : https://github.com/Biancaa-R/Goat-disease-prediction-using-AIOT-/tree/main/mqtt_rpi_broker (deployed)
6. Anotated img: Used for video stream to test model before using external realtime data :https://github.com/Biancaa-R/Goat-disease-prediction-using-AIOT-/tree/main/video_stream
7. Training files for YOLOv8 model: https://github.com/Biancaa-R/Goat-disease-prediction-using-AIOT-/tree/main/yolo_training
   
MQTT:

1. https://www.emqx.com/en/blog/esp8266_mqtt_led
2. https://www.emqx.com/en/blog/esp32-connects-to-the-free-public-mqtt-broker
3. https://www.emqx.com/en/blog/use-mqtt-with-raspberry-pi
4. https://www.aranacorp.com/en/udp-communication-between-raspberry-pi-and-esp32/#:~:text=Code%20ESP32%20UDP%20Client,network%20as%20the%20Raspberry%20Pi.
5. https://helloworld.co.in/article/mqtt-raspberry-pi-esp32

IP:
1. https://www.kaspersky.com/resource-center/definitions/what-is-an-ip-address
2. https://www.geeksforgeeks.org/structure-and-types-of-ip-address/

MQTT ONLINE SERVER:

1. https://cloud-intl.emqx.com/console/deployments

2. https://docs.emqx.com/en/cloud/latest/connect_to_deployments/python_sdk.html

3. https://docs.emqx.com/en/cloud/latest/connect_to_deployments/esp8266.html
4. control: https://docs.emqx.com/en/cloud/latest/deployments/stop_delete_deployment.html

Note: Initial attempt to use tensorflow api for bounding boxes is set for future and I decided to go with YOLOv8n instead as there were unresolved version clashes when using tf api with 1 and 2 ...YOLO   was an easier option to try. So probably in future I might fix the bugs with tensor api (seems quite unlikely now)

The .pt YOLO v8 model was converted to onnx for deployment in raspberrypi 4b .The result of the form (x,y,h,w) is used for the generation of bounding boxes.

Tool used for annotation: LabelImg
from the xml files , annotations were converted to yolo 1.1 format ie txt

FUTURE SCOPE:
1. Add more sensors in the client circuit and more disease detection
2. Display graphs with the generated data in the flask site
3. Display the general observed data as well in site as a separate webpage (now only in case of disease notification data is displayed)
4. Notification via SMS/ call additionally to website based notification
