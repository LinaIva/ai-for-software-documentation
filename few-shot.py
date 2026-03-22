import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

ZERO_SHOT_PROMPT = "Summarize the following code."

FEW_SHOT_PROMPT = """
Example 1:

Code:
def add(a, b):
    return a + b

Summary:
Language: Python
Description: This function returns the sum of two numbers.

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
    return {"status": "ok"}

Summary:
Language: Python
Description: This is an asynchronous API endpoint function that receives log messages from a request and writes them to a logger.

Now summarize the following code.
"""

print("Choose mode:")
print("0 - Zero-shot")
print("else - Few-shot")

mode = input("Mode: ")

print("\nPaste code(finish with empty line):")
code_lines = []
while True:
    line = input()
    if line == "":
        break
    code_lines.append(line)
code = "\n".join(code_lines)
if mode == "0":
    prompt = ZERO_SHOT_PROMPT + "\nCode:\n" + code.strip()
else:
    prompt = FEW_SHOT_PROMPT + "\nCode:\n" + code.strip()

response = client.responses.create(model="gpt-4o-mini", input=prompt)

print("\n:::Summary:::\n")
print(response.output_text)