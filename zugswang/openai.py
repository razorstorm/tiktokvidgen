import os

from openai import Client
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.environ["OPENAI_API_KEY"]

client = Client(api_key=API_KEY)


def generate_text(prompt: str, text: str, model: str = 'gpt-4o'):
    completion = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": text},
        ],
    )
    return completion.choices[0].message['content']
