import os
import requests

def load_env():
    with open('.env', 'r') as f:
        for line in f:
            if line.strip() and not line.startswith('#'):
                key, value = line.strip().split('=', 1)
                os.environ[key] = value

load_env()

GROQ_API_KEY = os.environ.get('GROQ_API_KEY')
GROQ_API_BASE = os.environ.get('GROQ_BASE_URL', 'https://api.groq.com/openai/v1')

MODELS_TO_TEST = [
    "llama-3.1-70b-versatile",
    "llama-3.1-8b-instant",
    "mixtral-8x7b-32768",
    "gemma-7b-it",
]

def test_groq_models():
    if not GROQ_API_KEY:
        print("Groq API key not found in .env file.")
        return

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    # Test listing models
    print("Testing Groq API - Listing Models")
    try:
        response = requests.get(f"{GROQ_API_BASE}/models", headers=headers)
        response.raise_for_status()
        models = response.json()
        print(f"Available models: {', '.join([model['id'] for model in models['data']])}")
    except requests.exceptions.RequestException as e:
        print(f"Error listing models: {str(e)}")
        if hasattr(e, 'response'):
            print(f"Response status code: {e.response.status_code}")
            print(f"Response content: {e.response.text}")

    # Test chat completions for each model
    for model in MODELS_TO_TEST:
        print(f"\nTesting Groq API - Chat Completion with {model}")
        data = {
            "model": model,
            "messages": [{"role": "user", "content": "Say hello!"}],
            "max_tokens": 50
        }
        try:
            response = requests.post(f"{GROQ_API_BASE}/chat/completions", headers=headers, json=data)
            response.raise_for_status()
            print(f"Response for {model}: {response.json()['choices'][0]['message']['content']}")
        except requests.exceptions.RequestException as e:
            print(f"Error with {model}: {str(e)}")
            if hasattr(e, 'response'):
                print(f"Response status code: {e.response.status_code}")
                print(f"Response content: {e.response.text}")

if __name__ == "__main__":
    test_groq_models()