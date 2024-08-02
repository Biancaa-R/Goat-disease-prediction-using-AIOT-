#conversion.py
from ultralytics import YOLO
model=YOLO("C:/wtf/runs/detect/train3/weights/best.pt")
success=model.export(format="onnx")