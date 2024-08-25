import cv2
import time
from ultralytics import YOLO

# Load the model
model = YOLO("C:/wtf/runs/detect/train2/weights/best.onnx")

cap = cv2.VideoCapture(0)

while True:
    start_time = time.time()

    # Capture frame
    success, frame = cap.read()
    if not success:
        print("Error capturing frame")
        break

    # Perform object detection
    frame=cv2.resize(frame,(640,640))
    results = model.predict(source=frame, conf=0.5, verbose=True, task="detect")

    # Process detections
    if results:
        for detection in results:
            for box in detection.boxes:
                # Extract bounding box coordinates
                x1, y1, x2, y2 = box.xyxy[0][0].item(), box.xyxy[0][1].item(), box.xyxy[0][2].item(), box.xyxy[0][3].item()
                start_point = (int(x1), int(y1))
                end_point = (int(x2), int(y2))

                # Draw rectangle on the frame
                cv2.rectangle(frame, start_point, end_point, (255, 0, 0), 3)

    # Display the frame
    cv2.imshow("Object Detection", frame)

    if cv2.waitKey(1) == ord('q'):
        break

cv2.destroyAllWindows()
