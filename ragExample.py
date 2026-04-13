import json
from cosineSimilarity import cosinSim
from chatWithAI import chatWithAi
from prompts import PROMPTS


def loadDataset(path="dataset.json"):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def findTopKSimilarCodes(inputCode, dataset, k=2):
    scoredExamples = []
    for item in dataset:
        instruction = item.get("instruction", "")
        summary = item.get("summary", "")
        code = item.get("code", "")
        scoredExamples.append({"instruction": instruction, "summary": summary,
            "code": code, "score": cosinSim(inputCode, code)})
    scoredExamples.sort(key=lambda x: x["score"], reverse=True)
    return scoredExamples[:k]

def buildRagPrompt(inputCode, topK):
    examplesText = []
    for i, example in enumerate(topK, start=1):
        examplesText.append(
            f"Example {i}:\n"
            f"Code:\n{example['code']}\n\n"
            f"Summary: {example['summary']}\n")

    joinedExamples = ("\n" + "-" * 50 + "\n").join(examplesText)

    prompt = f"""
You are a code summarization assistant. Your task is to read the input Python code and generate a clear summary.
Below are similar examples from the dataset:
{joinedExamples}

Now summarize this new code:
Code:
{inputCode}

"""
    print(prompt)
    return prompt.strip()

def generateSummaryWithRag(inputCode, datasetPath="dataset.json", k=2):
    dataset = loadDataset(datasetPath)
    topK = findTopKSimilarCodes(inputCode, dataset, k=k)
    prompt = buildRagPrompt(inputCode, topK)
    aiResponse = chatWithAi(prompt)
    return topK, aiResponse


if __name__ == "__main__":
    inputCode = PROMPTS[0]
    topExamples, generatedSummary = generateSummaryWithRag(inputCode)
    print(generatedSummary)