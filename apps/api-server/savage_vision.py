import cv2
import numpy as np

class SavageVision:
    def __init__(self):
        # Your Model Initialization (YOLO, etc)
        pass

    def get_patch_data(self, frame):
        if frame is None: return []

        # 1. BRIGHTNESS CHECK (Prevents false positives in the dark)
        avg_brightness = np.mean(frame)
        if avg_brightness < 20:
            print("🌑 DARKNESS DETECTED: Lens covered or lights off. Skipping AI.")
            return []

        # 2. PROCEED TO DETECTION
        # This is where your YOLO model runs
        # results = self.model(frame)
        
        # Placeholder detection
        return [{"name": "person", "confidence": 0.9}]

vision_engine = SavageVision()