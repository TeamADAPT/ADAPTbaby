# ... (previous imports remain the same)

from langchain_cohere import Cohere

# ... (previous code remains the same)

# Set up API clients
openai_client = ChatOpenAI(model_name="gpt-4o", api_key=os.environ.get('OPENAI_API_KEY'))
anthropic_client = ChatAnthropic(model="claude-3-5-sonnet-20240620", api_key=os.environ.get('ANTHROPIC_API_KEY'))
google_client = ChatGoogleGenerativeAI(model="gemini-pro", api_key=os.environ.get('GOOGLE_API_KEY'))
cohere_client = Cohere(model="command", api_key=os.environ.get('COHERE_API_KEY'))

# Available models
MODELS = {
    'gpt-4o': 'OpenAI GPT-4O',
    'gemini-pro': 'Google Gemini Pro',
    'claude-3-5-sonnet-20240620': 'Anthropic Claude 3.5 Sonnet',
    'cohere-command': 'Cohere Command',
    'meta-llama-3-70b-instruct': 'GitHub Meta Llama 3 70B Instruct',
    'mixtral-large': 'GitHub Mixtral Large',
    'phi-3-medium-instruct-12b': 'GitHub Phi-3 Medium Instruct 12B'
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
