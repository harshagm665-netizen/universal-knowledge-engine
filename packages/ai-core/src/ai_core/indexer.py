import os
from pymilvus import connections, FieldSchema, CollectionSchema, DataType, Collection, utility

# Connect to the Dockerized Milvus
connections.connect("default", host="localhost", port="19530")

def create_milvus_collection():
    collection_name = "robot_patches"
    
    # If already exists, drop it to start fresh (Savage style)
    if utility.has_collection(collection_name):
        utility.drop_collection(collection_name)

    # Define the schema for your 71 patches
    fields = [
        FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
        FieldSchema(name="patch_name", dtype=DataType.VARCHAR, max_length=100),
        FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=384) # Standard for small models
    ]
    
    schema = CollectionSchema(fields, "Visual patches for Preschooler Robot project")
    collection = Collection(collection_name, schema)
    
    # Create an index for fast searching
    index_params = {
        "metric_type": "L2",
        "index_type": "IVF_FLAT",
        "params": {"nlist": 128}
    }
    collection.create_index(field_name="embedding", index_params=index_params)
    print(f"Collection {collection_name} created successfully.")
    return collection

if __name__ == "__main__":
    create_milvus_collection()