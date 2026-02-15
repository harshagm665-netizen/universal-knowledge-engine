import time, threading, ollama

class AutonomousAgent:
    def __init__(self, arduino_link=None, vision_source=None):
        self.arduino = arduino_link
        self.vision_source = vision_source 
        self.active = True
        self.monitor_interval = 5.0
        self.persona = "You are 'Savage Bot', a witty and sarcastic AI preschool teacher companion."

    def start_sentinel(self):
        threading.Thread(target=self._monitor_vision, daemon=True).start()

    def _monitor_vision(self):
        while self.active:
            # Background logic for auto-scanning students
            time.sleep(self.monitor_interval)

    def execute_wave(self):
        print("🤖 [ACTION] -> Social Wave Triggered")
        try:
            # Fetch personality response from Ollama
            response = ollama.chat(model='llama3', messages=[
                {'role': 'system', 'content': self.persona},
                {'role': 'user', 'content': 'A student is waiting for a greeting.'}
            ])
            print(f"Savage Says: {response['message']['content']}")
        except:
            print("Savage Says: Greeting sequence initiated.")
            
        if self.arduino:
            self.arduino.write(bytes([0x01]))

    def stop(self):
        self.active = False