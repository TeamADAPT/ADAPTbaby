import os
import sys
import time
import json
import logging
from datetime import datetime

import requests
from flask import Flask, request, render_template, flash, jsonify, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_bcrypt import Bcrypt
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from dotenv import load_dotenv

# Try importing AI libraries
try:
    import openai
    import google.generativeai as genai
    import anthropic
    AI_IMPORTS_SUCCESSFUL = True
except ImportError as e:
    AI_IMPORTS_SUCCESSFUL = False
    print(f"Warning: Some AI libraries could not be imported. Error: {e}")

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__, template_folder='templates')
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///adaptbaby.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
admin = Admin(app, name='ADAPTbaby Admin', template_mode='bootstrap3')

# Initialize AI clients if imports were successful
if AI_IMPORTS_SUCCESSFUL:
    openai.api_key = os.environ.get('OPENAI_API_KEY', '')
    genai.configure(api_key=os.environ.get('GOOGLE_API_KEY', ''))
    anthropic_client = anthropic.Anthropic(api_key=os.environ.get('ANTHROPIC_API_KEY', ''))

# Available models
MODELS = {
    'groq-mixtral': 'Groq Mixtral-8x7B-32768',
    'gpt-4': 'OpenAI GPT-4',
    'gemini-pro': 'Google Gemini Pro',
    'claude-3-sonnet': 'Anthropic Claude 3 Sonnet',
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/test_models', methods=['GET', 'POST'])
def test_models():
    if request.method == 'POST':
        prompt = request.form.get('prompt', '').strip()
        selected_models = request.form.getlist('models')

        if not prompt:
            flash('Please enter a prompt.', 'error')
            return render_template('test_models.html', models=MODELS)

        if not selected_models:
            flash('Please select at least one model to test.', 'error')
            return render_template('test_models.html', models=MODELS)

        results = {}
        for model in selected_models:
            if model not in MODELS:
                flash(f'Invalid model selected: {model}', 'error')
                continue

            start_time = time.time()
            if model == 'groq-mixtral':
                response = test_groq_model(prompt)
            elif model == 'gpt-4':
                response = test_openai_model(prompt)
            elif model == 'gemini-pro':
                response = test_google_model(prompt)
            elif model == 'claude-3-sonnet':
                response = test_anthropic_model(prompt)
            else:
                response = "Unsupported model"

            end_time = time.time()
            results[model] = {
                'response': response,
                'time': round(end_time - start_time, 2)
            }

        return render_template('test_results.html', results=results, prompt=prompt, models=MODELS)
    
    return render_template('test_models.html', models=MODELS)

def test_groq_model(prompt):
    groq_api_key = os.environ.get('GROQ_API_KEY')
    if not groq_api_key:
        return "Groq API key not found in environment variables."

    groq_url = "https://api.groq.com/openai/v1/chat/completions"
    groq_headers = {
        "Authorization": f"Bearer {groq_api_key}",
        "Content-Type": "application/json"
    }
    groq_data = {
        "messages": [{"role": "user", "content": prompt}],
        "model": "mixtral-8x7b-32768"
    }
    try:
        response = requests.post(groq_url, headers=groq_headers, json=groq_data, timeout=30)
        response.raise_for_status()
        return response.json()['choices'][0]['message']['content']
    except requests.RequestException as e:
        return f"Error testing Groq model: {str(e)}"

def test_openai_model(prompt):
    if not AI_IMPORTS_SUCCESSFUL:
        return "OpenAI library not imported successfully."
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error testing OpenAI model: {str(e)}"

def test_google_model(prompt):
    if not AI_IMPORTS_SUCCESSFUL:
        return "Google AI library not imported successfully."
    try:
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error testing Google model: {str(e)}"

def test_anthropic_model(prompt):
    if not AI_IMPORTS_SUCCESSFUL:
        return "Anthropic library not imported successfully."
    try:
        response = anthropic_client.completions.create(
            model="claude-3-sonnet-20240229",
            prompt=f"Human: {prompt}\n\nAssistant:",
            max_tokens=300
        )
        return response.completion
    except Exception as e:
        return f"Error testing Anthropic model: {str(e)}"

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
