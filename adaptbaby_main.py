import os
import babyagi
from flask import request, jsonify, render_template
from dotenv import load_dotenv
import logging
from datetime import datetime
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import HumanMessage
import litellm
from transformers import pipeline
from huggingface_hub import snapshot_download

# Set up logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='adaptbaby.log',
    filemode='w'
)
logger = logging.getLogger(__name__)

# Add console handler to print logs to console as well
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

print("Starting ADAPTbaby application...")
logger.info("Initializing ADAPTbaby application")

# Load environment variables
load_dotenv()

# Initialize agent memory
agent_memory = []

# Available models
AVAILABLE_MODELS = {
    # OpenAI models
    "gpt-4o": "GPT-4o",
    "gpt-4o-mini": "GPT-4o Mini",
    "gpt-3.5-turbo": "GPT-3.5 Turbo",
    "gpt-3.5-turbo-16k": "GPT-3.5 Turbo 16k",
    "gpt-4": "GPT-4",
    "gpt-4-32k": "GPT-4 32k",
    "gpt-4-1106-preview": "GPT-4 Turbo",
    "gpt-4-vision-preview": "GPT-4 Vision",
    
    # Anthropic models
    "claude-2.1": "Claude 2.1",
    "claude-instant-1.2": "Claude Instant 1.2",
    "claude-3-opus-20240229": "Claude 3 Opus",
    "claude-3-sonnet-20240229": "Claude 3 Sonnet",
    "claude-3-haiku-20240307": "Claude 3 Haiku",
    
    # Gemini models
    "gemini-pro": "Gemini Pro",
    "gemini-pro-vision": "Gemini Pro Vision",
    "gemini-1.5-pro-latest": "Gemini 1.5 Pro Latest",
    "gemini-1.5-pro": "Gemini 1.5 Pro",
    "gemini-1.5-pro-001": "Gemini 1.5 Pro 001",
    "gemini-1.5-pro-vision-latest": "Gemini 1.5 Pro Vision Latest",
    "gemini-1.5-pro-vision": "Gemini 1.5 Pro Vision",
    "gemini-1.5-pro-vision-001": "Gemini 1.5 Pro Vision 001",
    
    # Hugging Face models
    "hf-distilbert-base-uncased-finetuned-sst-2-english": "Hugging Face DistilBERT (Sentiment Analysis)",
    "hf-gpt2": "Hugging Face GPT-2",
}

# Enable verbose logging for LiteLLM
litellm.set_verbose = True

def get_llm(model_key):
    logger.info(f"Getting LLM for model: {model_key}")
    try:
        if model_key.startswith("gpt-"):
            return ChatOpenAI(model_name=model_key, temperature=0.7, openai_api_key=os.getenv('OpenAI_PROJECT_API_KEY'))
        elif model_key.startswith("claude-"):
            return ChatAnthropic(model=model_key, temperature=0.7, anthropic_api_key=os.getenv('ANTHROPIC_API_KEY'))
        elif model_key.startswith("gemini-"):
            return ChatGoogleGenerativeAI(model=model_key, temperature=0.7, google_api_key=os.getenv('GOOGLE_API_KEY'))
        elif model_key.startswith("hf-"):
            return get_huggingface_model(model_key)
        else:
            logger.warning(f"Unknown model key: {model_key}. Defaulting to GPT-3.5-turbo.")
            return ChatOpenAI(temperature=0.7, openai_api_key=os.getenv('OpenAI_PROJECT_API_KEY'))
    except Exception as e:
        logger.error(f"Error initializing LLM for model {model_key}: {str(e)}")
        raise

def get_huggingface_model(model_key):
    logger.info(f"Initializing Hugging Face model: {model_key}")
    try:
        model_name = model_key.replace("hf-", "")
        cache_dir = os.path.expanduser("~/.cache/huggingface/hub")
        logger.info(f"Hugging Face cache directory: {cache_dir}")

        # Check if model files are already in cache
        try:
            snapshot_download(repo_id=model_name, cache_dir=cache_dir)
            logger.info(f"Model {model_name} is already cached or has been downloaded.")
        except Exception as e:
            logger.error(f"Error downloading model {model_name}: {str(e)}")

        if model_name == "distilbert-base-uncased-finetuned-sst-2-english":
            logger.debug(f"Creating sentiment-analysis pipeline for {model_name}")
            return pipeline("sentiment-analysis", model=model_name)
        elif model_name == "gpt2":
            logger.debug(f"Creating text-generation pipeline for {model_name}")
            return pipeline("text-generation", model=model_name, max_length=200, max_new_tokens=100)
        else:
            raise ValueError(f"Unsupported Hugging Face model: {model_name}")
    except Exception as e:
        logger.error(f"Error initializing Hugging Face model {model_key}: {str(e)}")
        raise

def langchain_completion(prompt, model_key="gpt-3.5-turbo"):
    logger.info(f"Performing langchain completion with model: {model_key}")
    try:
        llm = get_llm(model_key)
        if model_key.startswith("hf-"):
            if "distilbert" in model_key:
                logger.debug(f"Using DistilBERT for sentiment analysis: {prompt}")
                result = llm(prompt)[0]
                logger.debug(f"DistilBERT result: {result}")
                return f"Sentiment: {result['label']}, Score: {result['score']:.2f}"
            elif "gpt2" in model_key:
                logger.debug(f"Using GPT-2 for text generation: {prompt}")
                result = llm(prompt, max_length=200, do_sample=True, temperature=0.7, truncation=True)[0]['generated_text']
                logger.debug(f"GPT-2 result: {result}")
                return result
        else:
            messages = [HumanMessage(content=prompt)]
            response = llm.invoke(messages)
            return response.content
    except Exception as e:
        logger.error(f"Error in langchain_completion for model {model_key}: {str(e)}")
        return f"Error: {str(e)}"

@babyagi.register_function()
def adaptbaby_agent(task, model="gpt-3.5-turbo", conversation_history=[]):
    """An enhanced agent that processes tasks using Langchain's LLMs and maintains memory."""
    global agent_memory
    logger.info(f"Processing task: {task}")
    logger.info(f"Using model: {model}")

    try:
        # Prepare conversation context
        context = "\n".join([f"{msg['role']}: {msg['content']}" for msg in conversation_history])
        
        # Analyze the task
        task_analysis = langchain_completion(f"Given the following conversation:\n{context}\n\nAnalyze and categorize this task: {task}", model)
        
        # Generate a plan
        plan = langchain_completion(f"Given the following conversation and task analysis:\n{context}\n{task_analysis}\n\nCreate a step-by-step plan to accomplish this task: {task}", model)
        
        # Execute the plan (simulated)
        execution_result = langchain_completion(f"Given the following conversation, task analysis, and plan:\n{context}\n{task_analysis}\n{plan}\n\nSimulate the execution of this plan: {plan}", model)
        
        # Summarize the result
        summary = langchain_completion(f"Given the following conversation, task analysis, plan, and execution result:\n{context}\n{task_analysis}\n{plan}\n{execution_result}\n\nSummarize the result of this task execution.", model)
        
        # Update agent memory
        memory_entry = {
            "timestamp": datetime.now().isoformat(),
            "task": task,
            "analysis": task_analysis,
            "plan": plan,
            "execution": execution_result,
            "summary": summary,
            "model": AVAILABLE_MODELS.get(model, model)
        }
        agent_memory.append(memory_entry)
        
        # Limit memory to last 10 entries
        if len(agent_memory) > 10:
            agent_memory = agent_memory[-10:]
        
        logger.info(f"Task processing completed: {task}")
        return memory_entry
    except Exception as e:
        error_message = f"Error processing task: {str(e)}"
        logger.error(error_message)
        return {"error": error_message}

def get_registered_functions():
    """Get a list of registered functions."""
    try:
        return babyagi.get_all_functions_wrapper()
    except AttributeError:
        logger.error("get_all_functions_wrapper not found in babyagi module")
        return []

def create_app():
    app = babyagi.create_app('/dashboard')

    @app.route('/')
    @app.route('/adaptbaby')
    def adaptbaby_dashboard():
        logger.info("Accessing ADAPTbaby dashboard")
        return render_template('adaptbaby.html', models=AVAILABLE_MODELS)

    @app.route('/chat', methods=['POST'])
    def chat():
        data = request.json
        message = data['message']
        model = data.get('model', 'gpt-3.5-turbo')
        conversation_history = data.get('conversation_history', [])
        conversation_history.append({"role": "user", "content": message})
        
        logger.info(f"Received chat request. Message: {message}, Model: {model}")
        
        result = adaptbaby_agent(message, model, conversation_history)
        
        response = {
            "role": "assistant",
            "content": result.get('summary', 'No summary available.'),
            "full_response": result
        }
        conversation_history.append(response)
        
        logger.info(f"Chat response generated. Summary: {response['content'][:50]}...")
        
        return jsonify({
            "response": response,
            "conversation_history": conversation_history
        })

    @app.route('/list_functions')
    def list_functions():
        logger.info("Listing available functions")
        functions = get_registered_functions()
        return jsonify({'functions': functions})

    @app.route('/get_memory')
    def get_memory():
        logger.info("Retrieving agent memory")
        return jsonify({'memory': agent_memory})

    return app

if __name__ == "__main__":
    app = create_app()
    print("ADAPTbaby application created. Starting the server...")
    logger.info("ADAPTbaby application created. Starting the server...")
    app.run(host='0.0.0.0', port=8080, debug=True)