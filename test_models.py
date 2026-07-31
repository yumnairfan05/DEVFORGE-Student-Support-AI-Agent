import os
import requests
from dotenv import load_dotenv

load_dotenv()

headers = {
    "Authorization": f"Bearer {os.getenv('OLLAMAAPIKEY')}"
}

response = requests.get(
    "https://ollama.com/api/tags",
    headers=headers
)

print(response.status_code)
print(response.text)