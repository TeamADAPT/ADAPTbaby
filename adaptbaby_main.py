import os
import babyagi
from flask import Flask, request, jsonify, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_bcrypt import Bcrypt
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from dotenv import load_dotenv
import logging
from datetime import datetime
import time
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_cohere import Cohere
from langchain.schema import HumanMessage
import litellm
from transformers import pipeline
from huggingface_hub import snapshot_download
import requests
import pygments
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# ... (previous code remains the same)

# Set up API clients
openai_client = ChatOpenAI(model_name="gpt-4o", api_key=os.environ.get('OPENAI_API_KEY'))
anthropic_client = ChatAnthropic(model="claude-3-5-sonnet-20240620", api_key=os.environ.get('ANTHROPIC_API_KEY'))
google_client = ChatGoogleGenerativeAI(model="gemini-pro", api_key=os.environ.get('GOOGLE_API_KEY'))
cohere_client = Cohere(model="command", api_key=os.environ.get('COHERE_API_KEY'))

# Groq client setup
groq_api_key = os.environ.get('GROQ_API_KEY')
groq_url = "https://api.groq.com/openai/v1/chat/completions"
groq_headers = {
    "Authorization": f"Bearer {groq_api_key}",
    "Content-Type": "application/json"
}

# ... (previous code remains the same)

@app.route('/test_models', methods=['POST'])
@login_required
@limiter.limit("10 per minute")
def test_models():
    if current_user.api_calls_count >= current_user.api_calls_quota:
        return jsonify({"error": "API call quota exceeded"}), 429

    # Increment the API call count
    current_user.api_calls_count += 1
    db.session.commit()

    results = {}
    data = request.json
    test_prompt = data.get('prompt', "Hello, can you introduce yourself?")
    
    for model_key, model_name in MODELS.items():
        try:
            start_time = time.time()
            if model_key == 'gpt-4o':
                response = openai_client.invoke(test_prompt)
            elif model_key == 'claude-3-5-sonnet-20240620':
                response = anthropic_client.invoke(test_prompt)
            elif model_key == 'gemini-pro':
                response = google_client.invoke(test_prompt)
            elif model_key == 'cohere-command':
                response = cohere_client.invoke(test_prompt)
            elif model_key == 'groq-mixtral':
                groq_data = {
                    "messages": [{"role": "user", "content": test_prompt}],
                    "model": "llama3-8b-8192"
                }
                groq_response = requests.post(groq_url, headers=groq_headers, json=groq_data)
                groq_response.raise_for_status()
                response = groq_response.json()['choices'][0]['message']['content']
            else:
                # Handle GitHub models or other cases
                response = "Test not implemented for this model yet."
            end_time = time.time()
            
            response_time = end_time - start_time
            
            results[model_key] = {
                "status": "success",
                "response": str(response)[:500] + "..." if len(str(response)) > 500 else str(response),
                "response_time": round(response_time, 2)
            }
            logger.info(f"Successfully tested {model_name} in {response_time:.2f} seconds")
            
            # Log usage
            usage = ModelUsage(user_id=current_user.id, model=model_key, prompt=test_prompt, response_time=response_time)
            db.session.add(usage)
            db.session.commit()
        except Exception as e:
            results[model_key] = {
                "status": "error",
                "message": str(e),
                "response_time": None
            }
            logger.error(f"Error testing {model_name}: {str(e)}")
    
    return jsonify(results)

# ... (rest of the code remains the same)
