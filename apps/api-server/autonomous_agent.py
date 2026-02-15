import time
import threading

class AutonomousAgent:
    def __init__(self, arduino_link=None, vision_source=None):
        self.arduino = arduino_link
        self.vision_source = vision_source 
        self.active = True
        self.monitor_interval = 5.0

    def start_sentinel(self):
        threading.Thread(target=self._monitor_vision, daemon=True).start()

    def _monitor_vision(self):
        while self.active:
            try:
                if self.vision_source and self.vision_source.is_available():
                    frame = self.vision_source.get_current_frame()
                    if frame is not None:
                        from savage_vision import vision_engine
                        print(f"🧠 ANALYZING: Frame at {time.strftime('%H:%M:%S')}")
                        detections = vision_engine.get_patch_data(frame)
                        
                        if any(d['name'] == 'person' for d in detections):
                            self.execute_wave()
            except Exception as e:
                print(f"Error: {e}")
            time.sleep(self.monitor_interval)

    def execute_wave(self):
        print("🤖 [ACTION] -> Social Wave Triggered")
        if self.arduino:
            self.arduino.write(bytes([0x01]))

    def stop(self):
        self.active = False