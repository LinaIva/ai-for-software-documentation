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
    # index = 0
    return data[index], index

def summarizeCode(code: str) -> str:
    # zero shot prompt
    # prompt = f"""
    #     You are a code summarization assistant.
    #     Your task is to read the given code and produce a clear summary.
    #     Code:
    #     {code}
    #     """
    # zero shot prompt roses framework
    prompt = f"""
    Role:
    You are an expert software documentation assistant.

    Objective:
    Generate a concise and accurate summary of the given source code.

    Scenario:
    You are working with code snippets from a real-world dataset. The code may vary in complexity, and your goal is to help developers quickly understand what the code does.

    Expected Solution:
    Provide a clear summary that explains the purpose and main functionality of the code. Focus on key logic, functions, or behavior.

    Steps:
    1. Identify the main purpose of the code.
    2. Highlight important functions, classes, or logic if relevant.
    3. Focus on overall behavior, not line-by-line explanation.
    4. Do not invent or assume functionality that is not present.
    5. Write the summary in 2–4 clear sentences using simple technical English.

    Code:
    {code}
    """.strip()
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