import os
import sys
from dotenv import load_dotenv
import torch
from transformers import pipeline

# Load environment variables
load_dotenv('../../../../../../home/x/ADAPT2/.env')

# Set up the API key
api_key = os.getenv("HUGGING_FACE_API_KEY")
hf_access_token = os.getenv("HF_ACCESS_API_TOKEN")

print(f"Python version: {sys.version}")
print(f"PyTorch version: {torch.__version__}")
print(f"CUDA available: {torch.cuda.is_available()}")
print(f"Current working directory: {os.getcwd()}")
print(f"HUGGING_FACE_API_KEY: {'Set' if api_key else 'Not set'}")
print(f"HF_ACCESS_API_TOKEN: {'Set' if hf_access_token else 'Not set'}")

if api_key:
    print(f"API Key: {api_key[:5]}...{api_key[-5:]}")
else:
    print("API Key is not set in the environment variables.")

if hf_access_token:
    print(f"HF Access Token: {hf_access_token[:5]}...{hf_access_token[-5:]}")
else:
    print("HF Access Token is not set in the environment variables.")

def main():
    try:
        # Set up the Hugging Face API token
        os.environ["HUGGINGFACE_TOKEN"] = hf_access_token

        # Initialize a text classification pipeline
        classifier = pipeline("sentiment-analysis")

        # Test the classifier
        result = classifier("I love using Hugging Face models!")

        print(f"\nTest input: I love using Hugging Face models!")
        print(f"Classification result: {result}")

    except ImportError as e:
        print(f"ImportError: {str(e)}")
        print("Please make sure you have the 'transformers' library and its dependencies installed.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()