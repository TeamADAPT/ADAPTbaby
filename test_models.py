import os
import requests
from dotenv import load_dotenv
import concurrent.futures

# Load environment variables
load_dotenv()

# Define model categories
MODELS = {
    "OpenAI": {
        "gpt-3.5-turbo": "GPT-3.5 Turbo",
        "gpt-4": "GPT-4",
        "gpt-4-vision-preview": "GPT-4 Vision",
    },
    "Anthropic": {
        "claude-2.1": "Claude 2.1",
        "claude-3-opus-20240229": "Claude 3 Opus",
        "claude-3-sonnet-20240229": "Claude 3 Sonnet",
    },
    "Google": {
        "gemini-pro": "Gemini Pro",
        "gemini-pro-vision": "Gemini Pro Vision",
    },
    "Mistral": {
        "mistral-tiny": "Mistral Tiny",
        "mistral-small": "Mistral Small",
        "mistral-medium": "Mistral Medium",
    },
    "Groq": {
        "llama2-70b-4096": "Llama 2 70B",
        "mixtral-8x7b-32768": "Mixtral 8x7B 32K",
    },
}

def test_openai_model(model):
    api_key = os.getenv('OPENAI_API_KEY')
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "model": model,
        "messages": [{"role": "user", "content": "Hello, how are you?"}],
        "max_tokens": 50
    }
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        return True, f"{model} - Success"
    except Exception as e:
        return False, f"{model} - Error: {str(e)}"

def test_anthropic_model(model):
    api_key = os.getenv('ANTHROPIC_API_KEY')
    url = "https://api.anthropic.com/v1/chat/completions"
    headers = {
        "x-api-key": api_key,
        "Content-Type": "application/json",
        "anthropic-version": "2023-06-01"
    }
    data = {
        "model": model,
        "messages": [{"role": "user", "content": "Hello, how are you?"}],
        "max_tokens": 50
    }
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        return True, f"{model} - Success"
    except Exception as e:
        return False, f"{model} - Error: {str(e)}"

def test_google_model(model):
    api_key = os.getenv('GOOGLE_API_KEY')
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "contents": [{"parts": [{"text": "Hello, how are you?"}]}]
    }
    try:
        response = requests.post(f"{url}?key={api_key}", headers=headers, json=data)
        response.raise_for_status()
        return True, f"{model} - Success"
    except Exception as e:
        return False, f"{model} - Error: {str(e)}"

def test_mistral_model(model):
    api_key = os.getenv('MISTRAL_API_KEY')
    url = "https://api.mistral.ai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "model": model,
        "messages": [{"role": "user", "content": "Hello, how are you?"}],
        "max_tokens": 50
    }
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        return True, f"{model} - Success"
    except Exception as e:
        return False, f"{model} - Error: {str(e)}"

def test_groq_model(model):
    api_key = os.getenv('GROQ_API_KEY')
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "model": model,
        "messages": [{"role": "user", "content": "Hello, how are you?"}],
        "max_tokens": 50
    }
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        return True, f"{model} - Success"
    except Exception as e:
        return False, f"{model} - Error: {str(e)}"

def test_models():
    results = []
    total_tested = 0
    total_passed = 0
    total_failed = 0

    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        future_to_model = {}

        for provider, models in MODELS.items():
            for model_key, model_name in models.items():
                if provider == "OpenAI":
                    future = executor.submit(test_openai_model, model_key)
                elif provider == "Anthropic":
                    future = executor.submit(test_anthropic_model, model_key)
                elif provider == "Google":
                    future = executor.submit(test_google_model, model_key)
                elif provider == "Mistral":
                    future = executor.submit(test_mistral_model, model_key)
                elif provider == "Groq":
                    future = executor.submit(test_groq_model, model_key)
                future_to_model[future] = (provider, model_key, model_name)

        for future in concurrent.futures.as_completed(future_to_model):
            provider, model_key, model_name = future_to_model[future]
            try:
                success, message = future.result()
                total_tested += 1
                if success:
                    total_passed += 1
                else:
                    total_failed += 1
                results.append((provider, model_name, message))
            except Exception as exc:
                total_tested += 1
                total_failed += 1
                results.append((provider, model_name, f"{model_key} - Error: {str(exc)}"))

    # Print results
    print("\nTest Results:")
    for provider, model_name, message in results:
        print(f"{provider} - {model_name}: {message}")

    print(f"\nTotal Tested: {total_tested}")
    print(f"Total Passed: {total_passed}")
    print(f"Total Failed: {total_failed}")

if __name__ == "__main__":
    test_models()