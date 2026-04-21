from vectorDB import CodeVectorDB


def buildDB(datasetPath="dataset.json", dbPath="./qdrant_data"):
    db = CodeVectorDB(dataset_path=datasetPath, db_path=dbPath)
    db.indexDataset(force_reindex=True)
    print("Vector database successfully built.")

if __name__ == "__main__":
    buildDB()