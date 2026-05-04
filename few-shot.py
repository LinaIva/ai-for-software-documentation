import os
from openai import OpenAI
from dotenv import load_dotenv
from prompts import PROMPTS


load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def build_prompt(name: str, **kwargs) -> str:
    return PROMPTS[name].format(**kwargs).strip()

print("Choose mode:")
print("0 - zero_shot")
print("1 - few_shot")
print("2 - roses")
mode_input = input("Mode: ")
mode_map = {
    "0": "zero_shot",
    "1": "few_shot",
    "2": "roses"
}

prompt_name = mode_map.get(mode_input, "few_shot")

print("\nPaste code (finish with empty line):")
code_lines = []
while True:
    line = input()
    if line == "":
        break
    code_lines.append(line)
code = "\n".join(code_lines)
prompt = build_prompt(prompt_name, code=code)
response = client.responses.create(model="gpt-4o-mini", input=prompt)
print("\n::: Summary :::\n")
print(response.output_text)