from google import genai
import re

try:
    with open(".streamlit/secrets.toml", "r") as f:
        content = f.read()
    match = re.search(r'GEMINI_API_KEY\s*=\s*"(.*)"', content)
    api_key = match.group(1) if match else None

    if not api_key:
        print("API Key not found")
        exit(1)

    client = genai.Client(api_key=api_key)
    print("Listing models...")
    for m in client.models.list():
        print(f"Model ID: {m.name}")
except Exception as e:
    print(f"Error: {e}")
