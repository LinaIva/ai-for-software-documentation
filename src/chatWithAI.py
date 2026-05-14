import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def chatWithAi(user_input):
    response = client.responses.create(
        model="gpt-4o-mini", input=user_input)
    return "AI: " + response.output_text

