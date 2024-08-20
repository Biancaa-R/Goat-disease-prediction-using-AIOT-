import cv2
import time
from picamera2 import Picamera2
from ultralytics import YOLO
model = YOLO("best.onnx")

import numpy as np
picam2 = Picamera2()
# picam2.preview_configuration.main.size(1280,720)
# In case of the above command picam tuple is not callable
picam2.preview_configuration.main.format = "RGB888"
# picam2.preview_configuration.align()
# picam2.configure("preview")
picam2.start()
fps = 0
pos = (130, 160)

while True:
    start = time.time()
    im = picam2.capture_array()
    stop = time.time()
    loop_time = stop - start
    fps = 0.9 * fps + 0.1 * 1 / loop_time
    cv2.putText(im, str(fps), pos, cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 0, 0), 4)
    cv2.imshow("camera", im)
    # print im([0,0]) gives data on single pixel

    # Change shapes and types to match model
    # input1 = np.zeros([1, 128, 128,3], np.float32)

    # path="C:\\Users\\Biancaa. R\\Downloads\\cluster\\cluster_qt\\screen\\images\\black\\8d8e558b-39f7-4bdb-b72b-2dcc23ad39d1.png"
    # img=cv2.imread(path)
    im = cv2.rotate(im, cv2.ROTATE_180)
    results = model.predict(source=im, conf=0.05, verbose=False)

    try:
        x = results[0]
        box = x.boxes[0]
        anss = box.xyxy[0].tolist()
        start_point = (int(anss[0]), int(anss[1]))
        end_point = (int(anss[2]), int(anss[3]))
        color = (255, 0, 0)
        thickness = 3
        frame = cv2.rectangle(frame, start_point, end_point, color, thickness)
    except:
        print("dumb model")
    if cv2.waitKey(1)==ord('q'):
	    break
cv2.destroyAllWindows()
GPIO.cleanup()