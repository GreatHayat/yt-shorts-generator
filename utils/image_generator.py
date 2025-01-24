import os
import json
import requests

url = "https://api.openai.com/v1/images/generations"

headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {os.environ.get("OPENAI_API_KEY")}'
}


def generate_image(prompt: str) -> str:
    if not prompt:
        return None
    try:
        payload = json.dumps({
            "model": "dall-e-3",
            "prompt": prompt,
            "n": 1,
            "size": "1024x1792"
        })

        response = requests.request("POST", url, headers=headers, data=payload)

        return response.json().get('data')[0]['url']
    except Exception as e:
        print(f"Error generating image: {e}")
        return None
