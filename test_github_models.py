import os
import sys
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up the API
api_key = os.getenv("OpenAI_PROJECT_API_KEY")
endpoint = "https://models.inference.ai.azure.com"
model_name = "Cohere-command-r-plus"
api_version = "2023-07-01-preview"

print(f"Python version: {sys.version}")
print(f"Requests version: {requests.__version__}")
print(f"API Key: {api_key[:5]}...{api_key[-5:]}")
print(f"Endpoint: {endpoint}")
print(f"Model: {model_name}")

def main():
    headers = {
        "Content-Type": "application/json",
        "api-key": api_key
    }

    payload = {
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "What is the capital of France?"}
        ],
        "temperature": 0.7,
        "max_tokens": 150,
        "top_p": 0.95,
        "model": model_name
    }

    try:
        url = f"{endpoint}/openai/deployments/{model_name}/chat/completions?api-version={api_version}"
        print(f"\nMaking request to: {url}")
        print(f"With headers: {headers}")
        print(f"And payload: {payload}")
        
        response = requests.post(url, headers=headers, json=payload)

        print(f"\nResponse Status Code: {response.status_code}")
        print(f"Response Headers: {response.headers}")
        print(f"Response Content: {response.text}")

        if response.status_code == 200:
            result = response.json()
            print("\nGenerated Response:")
            print(result['choices'][0]['message']['content'])
        else:
            print(f"Error: {response.status_code}")
            print(response.text)
            
            # Additional error handling
            try:
                error_json = response.json()
                if 'error' in error_json:
                    print(f"Error details: {error_json['error']}")
            except:
                print("Could not parse error response as JSON")

    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()