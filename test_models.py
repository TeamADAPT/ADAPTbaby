import os
import requests
from dotenv import load_dotenv
import concurrent.futures
from termcolor import colored
import traceback

print("Starting script...")

# Load environment variables
load_dotenv()
print("Environment variables loaded.")

# Define model categories
MODELS = {
    "OpenAI": {
        "gpt-3.5-turbo": "GPT-3.5 Turbo",
        "gpt-4": "GPT-4",
    },
    "Anthropic": {
        "claude-2.1": "Claude 2.1",
        "claude-3-opus-20240229": "Claude 3 Opus",
    },
    "Google": {
        "gemini-pro": "Gemini Pro",
    },
    "Groq": {
        "llama2-70b-4096": "Llama 2 70B",
        "mixtral-8x7b-32768": "Mixtral 8x7B 32K",
    },
    "Mistral": {
        "mistral-small": "Mistral Small",
        "mistral-medium": "Mistral Medium",
    },
}

print("Models defined.")

def test_model(provider, model_key, model_name):
    print(f"Testing {provider} - {model_name}...")
    try:
        if provider == "OpenAI":
            return test_openai_model(model_key)
        elif provider == "Anthropic":
            return test_anthropic_model(model_key)
        elif provider == "Google":
            return test_google_model(model_key)
        elif provider == "Groq":
            return test_groq_model(model_key)
        elif provider == "Mistral":
            return test_mistral_model(model_key)
        else:
            return False, f"{model_key} - Error: Unknown provider"
    except Exception as e:
        print(f"Error testing {provider} - {model_name}: {str(e)}")
        traceback.print_exc()
        return False, f"{model_key} - Error: {str(e)}"

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
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    return True, f"{model} - Success"

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
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    return True, f"{model} - Success"

def test_google_model(model):
    api_key = os.getenv('GOOGLE_API_KEY')
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "contents": [{"parts": [{"text": "Hello, how are you?"}]}]
    }
    response = requests.post(f"{url}?key={api_key}", headers=headers, json=data)
    response.raise_for_status()
    return True, f"{model} - Success"

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
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    return True, f"{model} - Success"

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
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    return True, f"{model} - Success"

def test_models():
    print("Starting model tests...")
    results = []
    total_tested = 0
    total_passed = 0
    total_failed = 0
    failed_models = []

    for provider, models in MODELS.items():
        for model_key, model_name in models.items():
            try:
                success, message = test_model(provider, model_key, model_name)
                total_tested += 1
                if success:
                    total_passed += 1
                    results.append((provider, model_name, colored(message, 'green')))
                else:
                    total_failed += 1
                    results.append((provider, model_name, colored(message, 'red')))
                    failed_models.append((model_key, message.split(' - Error: ')[-1]))
            except Exception as exc:
                total_tested += 1
                total_failed += 1
                error_message = f"{model_key} - Error: {str(exc)}"
                results.append((provider, model_name, colored(error_message, 'red')))
                failed_models.append((model_key, str(exc)))
                print(f"Exception occurred while testing {provider} - {model_name}: {str(exc)}")
                traceback.print_exc()

    # Print results
    print("\nTest Results:")
    for provider, model_name, message in results:
        print(f"{provider} - {model_name}: {message}")

    print(f"\n{colored('Total Tested:', 'magenta')} {total_tested}")
    print(f"{colored('Total Passed:', 'green')} {total_passed}")
    print(f"{colored('Total Failed:', 'red')} {total_failed}")

    print("\nFailed Models (with error codes):")
    for model, error in failed_models:
        print(f"{model}: {error}")

if __name__ == "__main__":
    print("Script main section started.")
    test_models()
    print("Script completed.")