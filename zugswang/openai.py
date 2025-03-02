import os
from typing import List

import openai
from dotenv import load_dotenv
from openai import Client

load_dotenv()

API_KEY = os.environ["OPENAI_API_KEY"]


print(API_KEY)
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

def analyze_image(image_path: str, model: str = 'image-alpha-001') -> str:
    with open(image_path, "rb") as image_file:
        image_data = image_file.read()
    
    # Use OpenAI's Vision API to analyze the image
    response = openai.Image.create(
        model=model,
        images=image_data
    )
    
    # Extract the description from the response
    image_description = response['data'][0]['text']
    
    return image_description


def analyze_image_from_url(image_path: str, prompt: str = 'What\'s in this image?', model: str = 'gpt-4o-mini') -> str:
    response = client.chat.completions.create(
        model=model,
        messages=[
            {
            "role": "user",
            "content": [
                {"type": "text", "text": prompt},
                {
                "type": "image_url",
                "image_url": {
                    "url": image_path,
                },
                },
            ],
            }
        ],
        max_tokens=300,
    )

    return response.choices[0].message.content

def generate_image(prompt: str, text: str, model: str = 'dall-e-3') -> str:
    return generate_images(prompt, text, model=model)[0]


def generate_images(prompt: str, text: str, n: int = 1, model: str = 'dall-e-3') -> List[str]:
    try:
        image = client.images.generate(
            model=model,
            prompt=f"{text} {prompt}",
            n=n,
        )
        urls = [data.url for data in image.data]
        return urls
    except Exception as e:
        print(e)
        return [""]
