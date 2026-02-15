import time
import threading
import ollama  # Import the official Ollama library

class AutonomousAgent:
    def __init__(self, arduino_link=None, vision_source=None):
        self.arduino = arduino_link
        self.vision_source = vision_source 
        self.active = True
        self.monitor_interval = 5.0
        self.persona = "You are 'Savage Bot', a witty and sarcastic AI education companion for Novatech Robo. You are helpful but have a sharp, funny attitude."

    def start_sentinel(self):
        threading.Thread(target=self._monitor_vision, daemon=True).start()

    def _monitor_vision(self):
        while self.active:
            try:
                if self.vision_source and self.vision_source.is_available():
                    frame = self.vision_source.get_current_frame()
                    if frame is not None:
                        from savage_vision import vision_engine
                        detections = vision_engine.get_patch_data(frame)
                        
                        if any(d['name'] == 'person' for d in detections):
                            # NEW: Get a savage reaction from Ollama
                            self.get_savage_comment()
                            self.execute_wave()
            except Exception as e:
                print(f"Error: {e}")
            time.sleep(self.monitor_interval)

    def get_savage_comment(self):
        try:
            response = ollama.chat(model='llama3', messages=[
                {'role': 'system', 'content': self.persona},
                {'role': 'user', 'content': 'A human just walked into the room. Give a 1-sentence savage greeting.'}
            ])
            print(f"🤖 SAVAGE BOT: {response['message']['content']}")
        except Exception as e:
            print(f"Ollama Error: {e}")

    def execute_wave(self):
        print("🤖 [ACTION] -> Social Wave Triggered")
        if self.arduino:
            self.arduino.write(bytes([0x01]))