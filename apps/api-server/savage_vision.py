from ultralytics import YOLO

class VisionEngine:
    def __init__(self):
        # Using the Nano model for CPU efficiency
        self.model = YOLO("yolov8n.pt")

    def get_patch_data(self, frame):
        results = self.model(frame, verbose=False)
        detections = []
        for r in results:
            for box in r.boxes:
                detections.append({
                    "name": self.model.names[int(box.cls)],
                    "conf": float(box.conf),
                    "box": box.xyxy[0].tolist()
                })
        return detections

vision_engine = VisionEngine()