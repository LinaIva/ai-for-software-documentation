from vectorDB import CodeVectorDB
from chatWithAI import chatWithAi
from prompts import PROMPTS


def format_examples(topK):
    examples_text = []
    for i, example in enumerate(topK, start=1):
        examples_text.append(
            f"""Example {i}:
Code:
{example["code"]}

Summary:
{example["summary"]}
""")
    return ("\n" + "-" * 50 + "\n").join(examples_text)


def build_prompt(prompt_name: str, **kwargs) -> str:
    return PROMPTS[prompt_name].format(**kwargs).strip()

def generateSummaryWithRag(inputCode, k=2):
    db = CodeVectorDB(dataset_path="../datasets/dataset.json", db_path="../qdrant_data")
    topK = db.searchSimilarCode(inputCode, k=k)
    examples = format_examples(topK)
    prompt = build_prompt("rag", code=inputCode, examples=examples)
    aiResponse = chatWithAi(prompt)
    return topK, aiResponse


if __name__ == "__main__":
    inputCode = """
def build_graph():
    builder = StateGraph(DocState)
    builder.add_node("reader", reader_node)
    builder.add_node("writer", writer_node)
    builder.add_node("verifier", verifier_node)
    builder.add_node("miu_finisher", miu_finisher_node)
    builder.add_edge(START, "reader")
    builder.add_edge("reader", "writer")
    builder.add_edge("writer", "verifier")
    builder.add_conditional_edges(
        "verifier",
        route_after_verifier,
        {
            "writer": "writer",
            "miu_finisher": "miu_finisher",
        },
    )
    builder.add_edge("miu_finisher", END)
    return builder.compile()
"""
    topExamples, generatedSummary = generateSummaryWithRag(inputCode, k=2)
    print("TOP K=2 MATCHES:")
    for ex in topExamples:
        print(ex["score"], ex["summary"])
    print("\nGENERATED SUMMARY:")
    print(generatedSummary)