# ... (previous imports remain the same)
import requests

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
    # ... (previous code remains the same)

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
            
            # ... (rest of the code remains the same)

# ... (rest of the code remains the same)
