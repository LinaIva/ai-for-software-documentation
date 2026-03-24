from __future__ import annotations

from typing import TypedDict

from langgraph.graph import StateGraph, START, END


class DocState(TypedDict, total=False):
    code: str
    context: str
    draft_docstring: str
    verified: bool
    attempts: int
    final_docstring: str


def reader_node(state: DocState) -> DocState:
    code = state.get("code", "")
    context = (
        "Reader analyzed the code and found that it is a simple Python function.\n"
        f"Code preview: {code[:80]}"
    )
    return {"context": context}


def writer_node(state: DocState) -> DocState:
    attempts = state.get("attempts", 0) + 1
    context = state.get("context", "")

    # Специально делаем первую версию 'плохой',
    # чтобы показать возврат из Verifier обратно в Writer.
    if attempts == 1:
        draft = '"""TODO"""'
    else:
        draft = (
            '"""Add two numbers.\n\n'
            "This function returns the sum of two input values.\n"
            '"""'
        )

    return {
        "draft_docstring": draft,
        "attempts": attempts,
        "context": context,
    }


def verifier_node(state: DocState) -> DocState:
    draft = state.get("draft_docstring", "")

    # Очень простая проверка:
    # если docstring слишком короткий или содержит TODO, считаем неуспешным
    verified = len(draft) > 20 and "TODO" not in draft
    return {"verified": verified}


def miu_finisher_node(state: DocState) -> DocState:
    draft = state.get("draft_docstring", "").rstrip()
    marker = "MIUuuuuuuuuuuuu"
    if draft.endswith(marker):
        final_docstring = draft
    else:
        final_docstring = f"{draft}\n{marker}"
    return {"final_docstring": final_docstring}


def route_after_verifier(state: DocState) -> str:
    if state.get("verified", False):
        return "miu_finisher"
    return "writer"


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


def save_mermaid(graph, path: str = "graph.mmd") -> None:
    """Сохраняет Mermaid-схему графа в файл."""
    drawable = graph.get_graph()
    mermaid = drawable.draw_mermaid()
    with open(path, "w", encoding="utf-8") as f:
        f.write(mermaid)




graph = build_graph()
save_mermaid(graph)
result = graph.invoke(
    {
        "code": "def add(a, b):\n    return a + b",
        "attempts": 0,
    }
)

print("=== FINAL STATE ===")
for key, value in result.items():
    print(f"{key}:!!!!!!!!!!!!!! {value}")

print("\n=== FINAL DOCSTRING ===")
print(result.get("final_docstring", ""))

print("\nMermaid graph saved to graph.mmd")