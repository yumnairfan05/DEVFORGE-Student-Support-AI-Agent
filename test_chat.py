import os
import requests
from dotenv import load_dotenv

load_dotenv()

headers = {
    "Authorization": f"Bearer {os.getenv('OLLAMAAPIKEY')}",
    "Content-Type": "application/json"
}

data = {
    "model": "gpt-oss:20b",
    "messages": [
        {
            "role": "user",
            "content": "Hello"
        }
    ]
}

response = requests.post(
    "https://ollama.com/api/chat",
    headers=headers,
    json=data
)

print(response.status_code)
print(response.text)