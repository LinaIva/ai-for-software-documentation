PROMPTS = {
    "zero_shot": """
You are a code summarization assistant.
Task:
Read the given code and produce a clear and concise summary.
Code:
{code}
""",

    "roses": """
Role:
You are an expert software documentation assistant.

Objective:
Generate a concise and accurate summary of the given source code.

Scenario:
You are working with code snippets from a real-world dataset. The code may vary in complexity, and your goal is to help developers quickly understand what the code does.

Expected Solution:
Provide a clear summary that explains the purpose and main functionality of the code. Focus on key logic, functions, or behavior. Focus on overall behavior, not line-by-line explanation.  Do not invent or assume functionality that is not present.

Steps:
1. Identify the main purpose of the code.
2. Highlight important functions, classes, or logic if relevant.
3. Write the summary in 2–4 clear sentences using simple technical English.

Code:
{code}
""",

    "few_shot": """
Example 1:

Code:
def add(a, b):
    return a + b

Summary:
Language: Python
Description: This function returns the sum of two numbers.

----------------------------------------

Example 2:

Code:
async def log_endpoint(request: Request):
    data = await request.json()
    level = data.get("level", "info")
    message = data.get("message", "")
    extra = data.get("extra", [])
    if extra:
        message += " " + " ".join(map(str, extra))
    logger.log(message, level=level)
    return {{"status": "ok"}}

Summary:
Language: Python
Description: This is an asynchronous API endpoint function that receives log messages and writes them to a logger.

----------------------------------------

Now summarize the following code:
Code:
{code}
""",

    "rag": """
You are a code summarization assistant. Your task is to read the input Python code and generate a clear summary.
Below are examples with code similar to the input code:
{examples}

----------------------------------------

Now summarize this code:
Code:
{code}
"""
}
