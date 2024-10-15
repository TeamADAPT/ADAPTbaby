import os
import requests
from dotenv import load_dotenv

load_dotenv()

def test_groq_model():
    api_key = os.environ.get('GROQ_API_KEY')
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "messages": [{"role": "user", "content": "Explain the importance of fast language models"}],
        "model": "llama3-8b-8192"
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()
        print(f"Groq model response: {result['choices'][0]['message']['content']}")
        return True
    except Exception as e:
        print(f"Error testing Groq model: {str(e)}")
        return False

if __name__ == "__main__":
    success = test_groq_model()
    print(f"Groq model test {'succeeded' if success else 'failed'}")
