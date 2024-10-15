#!/data/projects/active/ADAPTbaby/adaptbaby_venv/bin/python3
# -*- coding: utf-8 -*-

import sys
import os
from typing import Any, Dict
import time
import json
import logging
from datetime import datetime

import requests

try:
    import networkx as nx  # type: ignore
    import plotly.graph_objs as go  # type: ignore
    import plotly.utils  # type: ignore
    from flask import Flask, request, jsonify, render_template, redirect, url_for, flash  # type: ignore
    from flask_sqlalchemy import SQLAlchemy  # type: ignore
    from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user  # type: ignore
    from flask_bcrypt import Bcrypt  # type: ignore
    from flask_admin import Admin  # type: ignore
    from flask_admin.contrib.sqla import ModelView  # type: ignore
    from dotenv import load_dotenv  # type: ignore
except ImportError as e:
    print(f"Error importing module: {e}")
    print("Make sure you're running this script in the virtual environment.")
    sys.exit(1)

# Load environment variables
load_dotenv()

# Initialize Flask app
app: Flask = Flask(__name__, template_folder='templates')
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///adaptbaby.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db: SQLAlchemy = SQLAlchemy(app)
bcrypt: Bcrypt = Bcrypt(app)
login_manager: LoginManager = LoginManager(app)
login_manager.login_view = 'login'  # type: ignore
admin: Admin = Admin(app, name='ADAPTbaby Admin', template_mode='bootstrap3')

# Available models
MODELS: Dict[str, str] = {
    'groq-mixtral': 'Groq Mixtral-8x7B-32768',
    'gpt-4o': 'OpenAI GPT-4O',
    'gemini-pro': 'Google Gemini Pro',
    'claude-3-5-sonnet-20240620': 'Anthropic Claude 3.5 Sonnet',
}

@app.route('/')
def index() -> str:
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
            elif model == 'gpt-4o':
                response = "OpenAI GPT-4O response placeholder"
            elif model == 'gemini-pro':
                response = "Google Gemini Pro response placeholder"
            elif model == 'claude-3-5-sonnet-20240620':
                response = "Anthropic Claude 3.5 Sonnet response placeholder"
            else:
                response = "Unsupported model"

            end_time = time.time()
            results[model] = {
                'response': response,
                'time': round(end_time - start_time, 2)
            }

        return render_template('test_results.html', results=results, prompt=prompt, models=MODELS)
    
    return render_template('test_models.html', models=MODELS)

def test_groq_model(prompt: str) -> str:
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

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
