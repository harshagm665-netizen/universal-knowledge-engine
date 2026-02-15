# test_ingestion.py
import os
import torch
from ai_core.loader import UniversalLoader
from ai_core.embedder import VisionEngine
from pathlib import Path

def test_pipeline():
    # 1. Setup Paths
    raw_data_dir = Path("data/raw")
    raw_data_dir.mkdir(parents=True, exist_ok=True)
    
    # Check for a sample file
    sample_file = next(raw_data_dir.glob("*"), None)
    if not sample_file:
        print("❌ Error: Please place a file (PDF, PNG, JPG) in data/raw/ to test.")
        return

    print(f"📂 Found sample: {sample_file.name}")

    # 2. Initialize the Engine
    # Note: On an i3, we use float32 for CPU stability
    print("🧠 Initializing AI Core (this may take a minute on CPU)...")
    loader = UniversalLoader(dpi=150) # Reduced DPI for i3 performance
    engine = VisionEngine()

    # 3. Step 1: Loading
    print("📸 Converting document to vision-ready images...")
    try:
        images = loader.to_images(str(sample_file))
        print(f"✅ Converted to {len(images)} high-res pages.")
    except Exception as e:
        print(f"❌ Loading Failed: {e}")
        return

    # 4. Step 2: Embedding (The 'Heavy' Part)
    print("👁️  AI is 'reading' the document visual patches...")
    try:
        # On i3, we only process the FIRST page for the test to save time
        first_page = [images[0]]
        embeddings = engine.get_embeddings(first_page)
        
        print(f"🎯 SUCCESS!")
        print(f"   - Pages Processed: 1")
        print(f"   - Embedding Shape: {embeddings.shape}")
        print(f"   - Device Used: {engine.device.upper()}")
        
    except Exception as e:
        print(f"❌ Embedding Failed: {e}")

if __name__ == "__main__":
    test_pipeline()