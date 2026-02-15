import torch
from ai_core.embedder import VisionEngine
from ai_core.database import VisionDB

class KnowledgeRetriever:
    def __init__(self):
        print("🧠 Loading Vision Engine for search...")
        self.engine = VisionEngine()
        self.db = VisionDB()

    def find_answer(self, query_text: str):
        # 1. Embed Query
        inputs = self.engine.processor.process_queries([query_text]).to(self.engine.device)
        with torch.no_grad():
            query_embeddings = self.engine.model(**inputs).embeddings
            query_vecs = query_embeddings[0].cpu().float().numpy().tolist()

        # 2. Search Milvus
        all_results = []
        for vec in query_vecs:
            res = self.db.client.search(
                collection_name=self.db.collection_name,
                data=[vec],
                limit=20,
                output_fields=["page_no"]
            )
            all_results.append(res[0])

        # 3. MaxSim Scoring
        page_scores = {}
        for token_results in all_results:
            for hit in token_results:
                page = hit['entity']['page_no']
                score = hit['distance']
                if page not in page_scores: page_scores[page] = []
                page_scores[page].append(score)

        final_ranking = [{"page": p, "score": max(s)} for p, s in page_scores.items()]
        final_ranking.sort(key=lambda x: x['score'], reverse=True)
        return final_ranking