import torch
from colpali_engine.models import ColQwen2, ColQwen2Processor

class VisionEngine:
    """
    The 'Eyes' of the system. Uses ColQwen2 to turn images 
    into multi-vector embeddings for diagram-aware retrieval.
    """
    def __init__(self, model_id: str = "vidore/colqwen2-v1.0"):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        
        # We use bfloat16 to save 50% VRAM without losing accuracy
        self.model = ColQwen2.from_pretrained(
            model_id,
            torch_dtype=torch.bfloat16 if self.device == "cuda" else torch.float32,
            device_map=self.device
        ).eval() # Set to evaluation mode (no training)
        
        self.processor = ColQwen2Processor.from_pretrained(model_id)
# packages/ai-core/src/ai_core/embedder.py

    def get_embeddings(self, images: list[Image.Image]):
        """
    Generates multi-vector embeddings. 
    Handles both object-based and raw tensor returns.
        """
        inputs = self.processor.process_images(images).to(self.device)
    
        with torch.no_grad():
            output = self.model(**inputs)
        
    # Senior Defensive Logic:
    # Some versions return an object with .embeddings, others return the tensor directly
        if hasattr(output, "embeddings"):
            return output.embeddings
    
    # If 'output' is already the tensor, return it directly
        return output