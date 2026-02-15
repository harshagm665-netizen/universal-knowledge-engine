import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

class KnowledgeRetriever:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY")
        
        # Initialize the Modern Client
        self.client = genai.Client(
            api_key=self.api_key,
            # Force v1 to avoid v1beta 404s
            http_options=types.HttpOptions(api_version="v1") 
        )
        
        # Use the standard model ID
        self.model_id = "gemini-2.5-flash" 
        self.patch_count = 71 

    def search(self, query: str):
        prompt = (
            f"You are a savage technical expert. Context: {self.patch_count} patches. "
            f"User Question: {query}\n"
            "Answer with technical precision and brutal wit."
        )
        
        try:
            # Modern generation call
            response = self.client.models.generate_content(
                model=self.model_id,
                contents=prompt
            )
            return response.text
        except Exception as e:
            return f"Savage Debugger Error: {str(e)}"