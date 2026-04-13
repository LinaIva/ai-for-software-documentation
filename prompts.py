PROMPTS = [
"""def build_graph():
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

    return builder.compile()"""
]