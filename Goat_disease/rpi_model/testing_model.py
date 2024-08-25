import cv2
from ultralytics import YOLO

# Load the model
model = YOLO("C:/wtf/runs/detect/train2/weights/best.onnx")

# Load a test image
frame = cv2.imread("D:/Goat_disease/images_collected/goat-ppr/train/1.jpg")

# Perform object detection with a higher confidence threshold
results = model.predict(source=frame, conf=0.5, verbose=True, task="detect")

# Check the number of detections
if len(results) > 0 and results[0].boxes is not None:
    print(f"Detections: {len(results[0].boxes)}")
    for box in results[0].boxes:  # Assuming results[0] contains detections
        x1, y1, x2, y2 = int(box.xyxy[0]), int(box.xyxy[1]), int(box.xyxy[2]), int(box.xyxy[3])
        start_point = (x1, y1)
        end_point = (x2, y2)
        cv2.rectangle(frame, start_point, end_point, (255, 0, 0), 3)

else:
    print("No detections found")

# Display the image with detections
cv2.imshow("Object Detection", frame)
cv2.waitKey(0)
cv2.destroyAllWindows()
