import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
print("LLM chat started\n")

while True:
    user_input = input("You: ")
    if user_input.lower() in ["exit", "quit"]:
        print("bye")
        break
    response = client.responses.create(
        model="gpt-4o-mini", input=user_input)
    print("AI:", response.output_text)
    print()
