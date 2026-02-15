from pymilvus import MilvusClient, DataType

class VisionDB:
    def __init__(self, uri="http://localhost:19530"):
        self.client = MilvusClient(uri=uri)
        self.collection_name = "enterprise_vision_rag"

    def setup_collection(self):
        if self.client.has_collection(self.collection_name):
            self.client.drop_collection(self.collection_name)

        # 1. Define Schema
        schema = self.client.create_schema(auto_id=True, enable_dynamic_field=True)
        
        schema.add_field(field_name="id", datatype=DataType.INT64, is_primary=True)
        # Note: We use DataType.FLOAT_VECTOR but the logic for MAX_SIM 
        # often requires specific handling in the index_params.
        schema.add_field(field_name="embeddings", datatype=DataType.FLOAT_VECTOR, dim=128)
        schema.add_field(field_name="doc_name", datatype=DataType.VARCHAR, max_length=255)
        schema.add_field(field_name="page_no", datatype=DataType.INT64)

        # 2. Define Index Params
        index_params = self.client.prepare_index_params()
        
        # BRUTAL TRUTH: If MAX_SIM fails on your Docker version, 
        # fallback to IP (Inner Product) which is mathematically 
        # what we use for normalized vectors in Late Interaction.
        index_params.add_index(
            field_name="embeddings",
            index_name="vision_idx",
            index_type="HNSW",
            metric_type="IP", # Inner Product is the standard fallback for ColPali/ColQwen2
            params={"M": 16, "efConstruction": 500}
        )

        self.client.create_collection(
            collection_name=self.collection_name, 
            schema=schema, 
            index_params=index_params
        )
        print(f"✅ Collection '{self.collection_name}' ready with IP index.")