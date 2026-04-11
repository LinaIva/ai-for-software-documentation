import os
import json
import random
from openai import OpenAI
from dotenv import load_dotenv
from similarity import evaluateSimilarity


load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
DATA_FILE = "dataset.json"

def loadExamples(file_path: str):
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

def getRandomSample(data):
    index = random.randint(0, len(data) - 1)
    return data[index], index

def summarizeCode(code: str) -> str:
    prompt = f"""
        You are a code summarization assistant.
        Your task is to read the given code and produce a short, clear summary in one sentence.    
        Code:
        {code}
        """
    response = client.responses.create(model="gpt-4o-mini", input=prompt)
    return response.output_text.strip()

def evaluate(reference: str, generated: str):
    scores = evaluateSimilarity(reference, generated)
    print("\nMetrics:")
    for k, v in scores.items():
        if k != "rouge_scores":
            print(f"{k}: {v}")


if __name__ == "__main__":
    data = loadExamples(DATA_FILE)
    sample, idx = getRandomSample(data)
    print("Random code sample:")
    print(sample["code"])
    summary = summarizeCode(sample["code"])
    print("AI summary:")
    print(summary)
    print(evaluate(sample["summary"], summary))