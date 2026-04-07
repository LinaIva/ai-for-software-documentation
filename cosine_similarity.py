from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


model = SentenceTransformer("all-MiniLM-L6-v2")

def cosin_sinil(text1 = "The cat is sitting on the mat.", text2 = "A cat is lying on the rug."):
    # model = SentenceTransformer("all-MiniLM-L6-v2")

    embedding1 = model.encode(text1)
    embedding2 = model.encode(text2)

    cosine_sim = np.dot(embedding1, embedding2) / (np.linalg.norm(embedding1) * np.linalg.norm(embedding2))

    similarity = cosine_similarity([embedding1], [embedding2])[0][0]

    # print("Cosine similarity(cosine_sim):", cosine_sim)
    # print("Embedding 1 shape:", embedding1.shape)
    # print("Embedding 2 shape:", embedding2.shape)
    # print("Cosine similarity(similarity):", similarity)
    return similarity

if __name__ == '__main__':
    print("Similarity: " + cosin_sinil())