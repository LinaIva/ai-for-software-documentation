import json
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct

COLLECTION_NAME = "codeExamples"

class CodeVectorDB:
    def __init__(self, dataset_path="dataset.json", db_path="./qdrant_data"):
        self.dataset_path = dataset_path
        self.client = QdrantClient(path=db_path)
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.vector_size = self.model.get_sentence_embedding_dimension()
        self._ensureCollection()

    def _ensureCollection(self):
        collections = self.client.get_collections().collections
        existing_names = {c.name for c in collections}
        if COLLECTION_NAME not in existing_names:
            self.client.create_collection(collection_name=COLLECTION_NAME,
                vectors_config=VectorParams(size=self.vector_size, distance=Distance.COSINE))

    def loadDataset(self):
        with open(self.dataset_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def indexDataset(self, force_reindex=False):
        dataset = self.loadDataset()
        if force_reindex:
            collections = self.client.get_collections().collections
            existingNames = {c.name for c in collections}
            if COLLECTION_NAME in existingNames:
                self.client.delete_collection(COLLECTION_NAME)
            self._ensureCollection()
        info = self.client.get_collection(COLLECTION_NAME)
        if getattr(info, "points_count", 0) and not force_reindex:
            return
        points = []
        for idx, item in enumerate(dataset):
            code = item.get("code", "")
            vector = self.model.encode(code).tolist()
            points.append(PointStruct(id=idx, vector=vector,payload={
                        "code": code, "summary": item.get("summary", ""), "instruction": item.get("instruction", "")}))
        self.client.upsert(collection_name=COLLECTION_NAME, points=points)

    def searchSimilarCode(self, inputCode, k=2):
        query_vector = self.model.encode(inputCode).tolist()
        results = self.client.query_points(collection_name=COLLECTION_NAME, query=query_vector,  limit=k).points
        return [{"code": point.payload.get("code", ""),"summary": point.payload.get("summary", ""),
                "instruction": point.payload.get("instruction", ""),"score": point.score} for point in results]