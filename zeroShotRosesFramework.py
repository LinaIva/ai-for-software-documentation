import os
import json
import random
from openai import OpenAI
from dotenv import load_dotenv
from prompts import PROMPTS
from similarity import evaluateSimilarity


load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
DATA_FILE = "datasets/dataset.json"

def loadExamples(file_path: str):
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

def getRandomSample(data):
    index = random.randint(0, len(data) - 1)
    # index = 0
    return data[index], index

def build_prompt(prompt_name: str, **kwargs) -> str:
    return PROMPTS[prompt_name].format(**kwargs).strip()

def summarizeCode(code: str, prompt_name: str = "roses") -> str:
    prompt = build_prompt(prompt_name, code=code)
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
    # summary = summarizeCode("")
    print("AI summary:")
    print(summary)
    # print(evaluate(sample["summary"], summary))