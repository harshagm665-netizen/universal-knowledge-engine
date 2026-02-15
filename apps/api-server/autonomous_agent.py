import time, threading, ollama

class AutonomousAgent:
    def __init__(self, arduino_link=None, vision_source=None):
        self.arduino, self.vision_source = arduino_link, vision_source
        self.active = True
        self.monitor_interval = 5.0
        self.persona = "You are 'Savage Bot', a witty AI. Give a 1-sentence reaction."

    def start_sentinel(self):
        threading.Thread(target=self._monitor_vision, daemon=True).start()

    def _monitor_vision(self):
        while self.active:
            try:
                if self.vision_source and self.vision_source.get_current_frame() is not None:
                    # Logic for vision analysis (YOLO/Ollama) goes here
                    # For now, we trigger if a person is found in vision_engine logic
                    pass 
            except Exception as e: print(f"Agent Error: {e}")
            time.sleep(self.monitor_interval)

    def execute_wave(self):
        print("🤖 [ACTION] -> Social Wave Triggered")
        try:
            response = ollama.chat(model='llama3', messages=[{'role': 'system', 'content': self.persona}, {'role': 'user', 'content': 'Someone is here.'}])
            print(f"Savage Says: {response['message']['content']}")
        except: print("Ollama offline.")
        if self.arduino: self.arduino.write(bytes([0x01]))

    def stop(self): self.active = False