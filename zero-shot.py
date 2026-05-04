import os
import json
import random
from openai import OpenAI
from dotenv import load_dotenv
from similarity import evaluateSimilarity
from prompts import PROMPTS


load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
DATA_FILE = "dataset.json"

def loadExamples(file_path: str):
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

def getRandomSample(data):
    index = random.randint(0, len(data) - 1)
    return data[index], index

def build_prompt(prompt_name: str, **kwargs) -> str:
    return PROMPTS[prompt_name].format(**kwargs).strip()

def summarizeCode(code: str, prompt_name: str = "zero_shot") -> str:
    prompt = build_prompt(prompt_name, code=code)
    # print(prompt)
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
    summary = summarizeCode(sample["code"], prompt_name="zero_shot")
    print("\nAI summary:")
    print(summary)
    # evaluate(sample["summary"], summary)