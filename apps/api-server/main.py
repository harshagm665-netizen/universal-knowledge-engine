import uvicorn
import cv2
import threading
import time
import serial
import numpy as np
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from autonomous_agent import AutonomousAgent

class SavageEye:
    def __init__(self):
        # Try index 0, if it fails, try index 1 (common for laptops with webcams)
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            self.cap = cv2.VideoCapture(1)
            
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
        self.ret, self.frame = False, None
        self.stopped, self.blueprint_mode = False, True

    def start(self):
        threading.Thread(target=self.update, daemon=True).start()
        return self

    def update(self):
        while not self.stopped:
            ret, frame = self.cap.read()
            if ret:
                self.ret, self.frame = ret, frame
            else:
                time.sleep(0.1) # Prevent CPU spike on failed read
            time.sleep(0.03)

    def get_current_frame(self):
        return self.frame.copy() if self.ret and self.frame is not None else None

    def get_frame_bytes(self):
        if not self.ret or self.frame is None:
            return self.create_placeholder()
        
        display_frame = self.frame.copy()
        if self.blueprint_mode:
            # Apply the "Preschool Teacher Bot" Blueprint aesthetic
            gray = cv2.cvtColor(display_frame, cv2.COLOR_BGR2GRAY)
            edges = cv2.Canny(gray, 100, 200)
            display_frame = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
            
        _, buffer = cv2.imencode('.jpg', display_frame)
        return buffer.tobytes()

    def create_placeholder(self):
        img = np.zeros((240, 320, 3), dtype=np.uint8)
        cv2.putText(img, "CAMERA_ERROR", (60, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        _, buffer = cv2.imencode('.jpg', img)
        return buffer.tobytes()

    def release(self):
        self.stopped = True
        if self.cap:
            self.cap.release()

# Initialize Eye and Hardware
eye = SavageEye()
try:
    # Use COM3 or your specific port found in Device Manager
    arduino = serial.Serial('COM3', 115200, timeout=0)
    print("✅ Arduino Connected on COM3")
except Exception as e:
    arduino = None
    print(f"ℹ️ Hardware mode: Offline ({e})")

agent = AutonomousAgent(arduino, vision_source=eye)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Start the camera thread and agent sentinel
    eye.start()
    agent.start_sentinel()
    yield
    # Shutdown: Release hardware resources
    eye.release()
    if arduino:
        arduino.close()

app = FastAPI(lifespan=lifespan)

# CRITICAL: Allow Next.js (port 3000) to access this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def status():
    return {"status": "Savage Engine Online", "hardware_mode": "Serial" if arduino else "Simulation"}

@app.get("/video_feed")
async def video_feed():
    def generate():
        while True:
            frame_bytes = eye.get_frame_bytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
            time.sleep(0.06) # ~15 FPS
    return StreamingResponse(generate(), media_type="multipart/x-mixed-replace; boundary=frame")

@app.post("/manual/analyze")
async def manual_analyze():
    frame = eye.get_current_frame()
    if frame is not None:
        try:
            # Import vision engine only when needed to save memory
            from savage_vision import vision_engine
            detections = vision_engine.get_patch_data(frame)
            if any(d['name'] == 'person' for d in detections):
                agent.execute_wave()
            return {"status": "success", "detections": detections}
        except Exception as e:
            return {"status": "error", "message": f"Vision Engine Error: {str(e)}"}
    return {"status": "error", "message": "Camera hardware not responding"}

@app.post("/manual/wave")
async def manual_wave():
    agent.execute_wave()
    return {"status": "triggered"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)