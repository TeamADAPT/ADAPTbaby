# Hugging Face Integration and Installation Guide

## Overview
This document outlines the process of integrating Hugging Face models into our application, including the installation of necessary dependencies and troubleshooting steps.

## Installation Steps

### 1. Install PyTorch (CPU Version)

Due to compatibility issues with CUDA, we opted for the CPU version of PyTorch:

```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
```

### 2. Install Hugging Face Transformers

Install the Transformers library:

```bash
pip install transformers
```

### 3. Set Up Environment Variables

Ensure the following environment variables are set:

- `HUGGING_FACE_API_KEY`: Your Hugging Face API key
- `HF_ACCESS_API_TOKEN`: Your Hugging Face access token

You can set these in your `.env` file or directly in your system's environment variables.

## Verification Process

### 1. Verify PyTorch Installation

Run the following command to check the PyTorch version:

```python
python3 -c "import torch; print(torch.__version__)"
```

Expected output: `2.4.1+cpu` (or similar, indicating CPU version)

### 2. Test Hugging Face Integration

Create a test script (`test_huggingface.py`) with the following content:

```python
import os
import sys
from dotenv import load_dotenv
import torch
from transformers import pipeline

# Load environment variables
load_dotenv('path/to/your/.env')

# Set up the API key
api_key = os.getenv("HUGGING_FACE_API_KEY")
hf_access_token = os.getenv("HF_ACCESS_API_TOKEN")

print(f"Python version: {sys.version}")
print(f"PyTorch version: {torch.__version__}")
print(f"CUDA available: {torch.cuda.is_available()}")
print(f"Current working directory: {os.getcwd()}")
print(f"HUGGING_FACE_API_KEY: {'Set' if api_key else 'Not set'}")
print(f"HF_ACCESS_API_TOKEN: {'Set' if hf_access_token else 'Not set'}")

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

    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
```

Run the test script:

```bash
python3 test_huggingface.py
```

## Troubleshooting

If you encounter issues:

1. Ensure all required packages are installed
2. Verify that environment variables are correctly set
3. Check for any error messages in the console output
4. If using a virtual environment, ensure it's activated

## Ongoing Considerations

- Regularly update PyTorch and Transformers to their latest compatible versions
- Monitor Hugging Face API usage and adjust as necessary
- Keep API keys and tokens secure and rotate them periodically
- Consider implementing caching mechanisms for frequently used models to improve performance