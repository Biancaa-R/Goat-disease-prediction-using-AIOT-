import cv2
import time
from ultralytics import YOLO

# Load the model (potentially only once outside the loop)
model = YOLO("best.onnx")

fps = 0
pos = (130, 160)
cap = cv2.VideoCapture(0)

while True:
    start_time = time.time()  # Use more precise time measurement

    # Capture frame
    success, frame = cap.read()
    frame=cv2.imread("D:/Goat_disease/images_collected/goat-ppr/train/1.jpg")
    path="D:/Goat_disease/images_collected/goat-ppr/train/"
    img="3"
    frame=cv2.imread(path+img+".jpg")
    if not success:
        print("Error capturing frame")
        break

    # Preprocess (consider resizing for faster inference)
    #frame = cv2.rotate(frame, cv2.ROTATE_180)  # Rotate if needed
    # Consider resizing the frame to a smaller size (e.g., 320x320)
    # resized_frame = cv2.resize(frame, (320, 320))

    # Perform object detection with lower verbosity for speed
    results = model.predict(source=frame, conf=0.01, verbose=False)

    # Process detections (if any)
    if results:
        try:
            # Extract bounding box and draw rectangle
            detection = results[0]  # Assuming single object detection
            box = detection.boxes[0]
            start_point = (int(box.xyxy[0]), int(box.xyxy[1]))
            end_point = (int(box.xyxy[2]), int(box.xyxy[3]))
            cv2.rectangle(frame, start_point, end_point, (255, 0, 0), 3)
        except IndexError:
            #print("No detections found")
            #import xml.dom.minidom as minidom

        # Parse the XML file
        #doc = minidom.parse(path+"16.xml")
            import xml.etree.ElementTree as ET

            tree = ET.parse(path+img+".xml")
            root = tree.getroot()

            boxes = []
            for obj in root.findall('object'):
                bbox = obj.find('bndbox')
                xmin = int(bbox.find('xmin').text)
                ymin = int(bbox.find('ymin').text)
                xmax = int(bbox.find('xmax').text)
                ymax = int(bbox.find('ymax').text) 

                boxes.append({'xmin':xmin, 'ymin': ymin, 'xmax': xmax, 'ymax': ymax})
                start_point = (int(xmin), int(ymin))
                end_point = (int(xmax), int(ymax))
                cv2.rectangle(frame, start_point, end_point, (255, 0, 0), 3)
                print(boxes)



    # Calculate FPS (consider different averaging methods)
    end_time = time.time()
    loop_time = end_time - start_time
    fps = 1 / loop_time  # Simple FPS calculation (can be improved)

    # Display frame with FPS (optional)
    # cv2.putText(frame, f"FPS: {fps:.2f}", pos, cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 0, 0), 4)
    cv2.imshow("Object Detection", frame)

    if cv2.waitKey(1) == ord('q'):
        break

cv2.destroyAllWindows()