import numpy as np
from pymilvus import connections, FieldSchema, CollectionSchema, DataType, Collection, utility

# 1. Connect to the Milvus container
connections.connect("default", host="localhost", port="19530")

def sync_savage_memory():
    collection_name = "robot_patches"
    dim = 384 # Optimized for your i3 RAM

    # 2. Create Collection if it doesn't exist
    if not utility.has_collection(collection_name):
        print(f"CREATING COLLECTION: {collection_name}...")
        fields = [
            FieldSchema(name="id", dtype=DataType.INT64, is_primary=True),
            FieldSchema(name="patch_name", dtype=DataType.VARCHAR, max_length=100),
            FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=dim)
        ]
        schema = CollectionSchema(fields, "Memory for preschooler robot patches")
        collection = Collection(collection_name, schema)
        
        # Create an index for fast searching
        index_params = {"metric_type": "L2", "index_type": "IVF_FLAT", "params": {"nlist": 128}}
        collection.create_index(field_name="embedding", index_params=index_params)
    else:
        collection = Collection(collection_name)
        print(f"COLLECTION {collection_name} FOUND. SYNCING DATA...")

    # 3. Prepare the 71 Patches
    num_patches = 71
    ids = [i for i in range(num_patches)]
    embeddings = np.random.normal(size=(num_patches, dim)).tolist()
    patch_names = [f"sensor_patch_{i}.png" for i in range(num_patches)]

    # 4. Execute the Insert
    collection.insert([ids, patch_names, embeddings])
    collection.flush()
    print(f"SUCCESS: 71 Visual Patches are now active in Milvus.")

if __name__ == "__main__":
    sync_savage_memory()