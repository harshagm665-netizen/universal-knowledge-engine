# services/ingestion-worker/ingest_to_db.py
import torch
from ai_core.loader import UniversalLoader
from ai_core.embedder import VisionEngine
from ai_core.database import VisionDB
from pathlib import Path

def run_ingestion():
    # 1. Init
    loader = UniversalLoader(dpi=150)
    engine = VisionEngine()
    db = VisionDB()
    
    # 2. Setup the Collection (Fresh start)
    db.setup_collection()

    # 3. Load Sample
    project_root = Path(__file__).resolve().parents[2]
    raw_dir = project_root / "data" / "raw"
    sample_file = next(raw_dir.glob("*"), None)
    
    if not sample_file:
        print("❌ No file found in data/raw/")
        return

    print(f"🚀 Processing: {sample_file.name}")

    # 4. Generate Embeddings
    images = loader.to_images(str(sample_file))
    # We only process page 1 for the test
    embeddings = engine.get_embeddings([images[0]]) 
    
    # 5. Flatten for IP Indexing
    embeddings_np = embeddings.cpu().float().numpy()
    
    data_to_insert = []
    # page_idx is 0, so page_no will be 1
    for page_idx, page_patches in enumerate(embeddings_np):
        for patch_vec in page_patches:
            data_to_insert.append({
                "doc_name": sample_file.name,
                "page_no": page_idx + 1,
                "embeddings": patch_vec.tolist()
            })

    # 6. Insert and FORCE PERSISTENCE
    print(f"💾 Inserting {len(data_to_insert)} patches into Milvus...")
    db.client.insert(collection_name=db.collection_name, data=data_to_insert)
    
    # SENIOR MOVE: Flush and Load
    # Flush ensures data is written to disk; Load moves it to RAM for searching
    db.client.flush(db.collection_name)
    db.client.load_collection(db.collection_name)
    
    stats = db.client.get_collection_stats(db.collection_name)
    print(f"✅ Ingestion Complete. Total rows now in DB: {stats['row_count']}")

if __name__ == "__main__":
    run_ingestion()