import os
from flask import Flask, request, render_template, flash
from dotenv import load_dotenv
import requests

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__, template_folder='templates')
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key')

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

            if model == 'groq-mixtral':
                response = test_groq_model(prompt)
            else:
                response = f"Test response for {MODELS[model]}"

            results[model] = {
                'response': response,
                'time': 0.5  # Placeholder response time
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

if __name__ == "__main__":
    app.run(debug=True)
