import cv2
import time
from ultralytics import YOLO
import os

# Load the model (potentially only once outside the loop)
model = YOLO("C:/wtf/runs/detect/train2/weights/best.onnx")

fps = 0
pos = (130, 160)
image_num = 1  # Starting image number
max_images = 40  # Maximum number of images to process

# Path to your images
path = "D:/Goat_disease/images_collected/goat-ppr/train/"

while image_num <= max_images:
    start_time = time.time()  # Use more precise time measurement

    # Construct image path
    img_path = os.path.join(path, f"{image_num}.jpg")

    # Read the image
    frame = cv2.imread(img_path)
    if frame is None:
        print(f"Error loading image {img_path}")
        image_num += 1
        continue

    # Preprocess (consider resizing for faster inference)
    frame = cv2.resize(frame, (640, 640))

    # Perform object detection with lower verbosity for speed
    results = model.predict(source=frame, conf=0.01, verbose=True, task="detect")

    if results:
        for detection in results:
            for box in detection.boxes:
                # Extract bounding box coordinates
                x1, y1, x2, y2 = box.xyxy[0][0].item(), box.xyxy[0][1].item(), box.xyxy[0][2].item(), box.xyxy[0][3].item()
                start_point = (int(x1), int(y1))
                end_point = (int(x2), int(y2))

                # Draw rectangle on the frame
                cv2.rectangle(frame, start_point, end_point, (255, 0, 0), 3)

    else:
        # Load corresponding XML file for annotations if no detections are found
        xml_path = os.path.join(path, f"{image_num}.xml")
        if os.path.exists(xml_path):
            import xml.etree.ElementTree as ET

            tree = ET.parse(xml_path)
            root = tree.getroot()

            for obj in root.findall('object'):
                bbox = obj.find('bndbox')
                xmin = int(bbox.find('xmin').text)
                ymin = int(bbox.find('ymin').text)
                xmax = int(bbox.find('xmax').text)
                ymax = int(bbox.find('ymax').text) 

                start_point = (xmin, ymin)
                end_point = (xmax, ymax)
                cv2.rectangle(frame, start_point, end_point, (255, 0, 0), 3)

    # Calculate FPS
    end_time = time.time()
    loop_time = end_time - start_time
    fps = 1 / loop_time  # Simple FPS calculation

    # Display frame with FPS (optional)
    cv2.imshow("Object Detection", frame)
    time.sleep(2)

    if cv2.waitKey(1) == ord('q'):
        break

    # Increment the image number to process the next image
    image_num += 1

cv2.destroyAllWindows()
