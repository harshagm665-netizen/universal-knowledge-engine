import uvicorn, cv2, threading, time, serial, numpy as np
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from autonomous_agent import AutonomousAgent

class SavageEye:
    def __init__(self):
        self.cap = cv2.VideoCapture(0, cv2.CAP_MSMF)
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
            if ret: self.ret, self.frame = ret, frame
            time.sleep(0.05)

    def get_current_frame(self):
        return self.frame.copy() if self.ret else None

    def get_frame_bytes(self):
        if not self.ret or self.frame is None: return self.create_placeholder()
        display_frame = self.frame
        if self.blueprint_mode:
            gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
            edges = cv2.Canny(gray, 100, 200)
            display_frame = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
        _, buffer = cv2.imencode('.jpg', display_frame)
        return buffer.tobytes()

    def create_placeholder(self):
        img = np.zeros((240, 320, 3), dtype=np.uint8)
        cv2.putText(img, "OFFLINE", (110, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        _, buffer = cv2.imencode('.jpg', img)
        return buffer.tobytes()

    def release(self):
        self.stopped = True
        if self.cap: self.cap.release()

eye = SavageEye()
try:
    arduino = serial.Serial('COM3', 115200, timeout=0)
    print("✅ Arduino Connected on COM3")
except Exception as e:
    arduino = None
    print(f"⚠️ Arduino Not Found: {e}")

agent = AutonomousAgent(arduino, vision_source=eye)

@asynccontextmanager
async def lifespan(app: FastAPI):
    eye.start()
    agent.start_sentinel()
    yield
    eye.release()
    if arduino: arduino.close()

app = FastAPI(lifespan=lifespan)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

@app.get("/video_feed")
async def video_feed():
    def generate():
        while True:
            yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + eye.get_frame_bytes() + b'\r\n')
            time.sleep(0.1)
    return StreamingResponse(generate(), media_type="multipart/x-mixed-replace; boundary=frame")

@app.post("/manual/wave")
async def manual_wave():
    agent.execute_wave()
    return {"status": "triggered"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)