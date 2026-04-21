from vectorDB import CodeVectorDB
from chatWithAI import chatWithAi
from prompts import PROMPTS


def buildRagPrompt(inputCode, topK):
    examplesText = []
    for i, example in enumerate(topK, start=1):
        examplesText.append(f"Example {i}:\nCode:\n{example['code']}\n\nSummary: {example['summary']}\n")
    joinedExamples = ("\n" + "-" * 50 + "\n").join(examplesText)
    prompt = f"""
You are a code summarization assistant. Your task is to read the input Python code and generate a clear summary.
Below are examples with code similar to the input code:
{joinedExamples}

Now summarize this new code:
Code:
{inputCode}
"""
    return prompt.strip()

def generateSummaryWithRag(inputCode, k=2):
    vectordb = CodeVectorDB(dataset_path="dataset.json", db_path="./qdrant_data")
    vectordb.indexDataset()
    topK = vectordb.searchSimilarCode(inputCode, k=k)
    prompt = buildRagPrompt(inputCode, topK)
    aiResponse = chatWithAi(prompt)
    return topK, aiResponse


if __name__ == "__main__":
    inputCode = PROMPTS[0]
    topExamples, generatedSummary = generateSummaryWithRag(inputCode, k=2)
    print("TOP K=2 MATCHES:")
    for ex in topExamples:
        print(ex["score"], ex["summary"])
    print("\nGENERATED SUMMARY:")
    print(generatedSummary)