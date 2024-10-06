import os
import babyagi
from flask import request, jsonify, render_template
from dotenv import load_dotenv
import logging
from datetime import datetime

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

print("Starting ADAPTbaby application...")
logger.info("Initializing ADAPTbaby application")

# Load environment variables
load_dotenv()

# Set up OpenAI API key
openai_api_key = os.getenv('OpenAI_PROJECT_API_KEY')
if not openai_api_key:
    error_message = "OpenAI_PROJECT_API_KEY not found in environment variables. Please check your .env file."
    print(error_message)
    logger.error(error_message)
    raise ValueError(error_message)

# Set the API key directly in the environment variables
os.environ['OPENAI_API_KEY'] = openai_api_key

# Print masked API key for debugging
masked_key = f"{openai_api_key[:5]}...{openai_api_key[-5:]}"
print(f"Using API key: {masked_key}")
logger.info(f"Using API key: {masked_key}")

# Add the OpenAI API key to BabyAGI
try:
    babyagi.add_key_wrapper('openai_api_key', openai_api_key)
    logger.info("OpenAI API key added successfully to BabyAGI")
except Exception as e:
    error_message = f"Error adding OpenAI API key to BabyAGI: {str(e)}"
    print(error_message)
    logger.error(error_message)
    raise

# Load necessary function packs
try:
    babyagi.load_functions("babyagi/functionz/packs/default/default_functions.py")
    babyagi.load_functions("babyagi/functionz/packs/default/ai_functions.py")
    logger.info("Function packs loaded successfully")
except Exception as e:
    error_message = f"Error loading function packs: {str(e)}"
    print(error_message)
    logger.error(error_message)
    raise

# Initialize agent memory
agent_memory = []

# Available models
AVAILABLE_MODELS = {
    "gpt-4o": "GPT-4o",
    "gpt-4o-mini": "GPT-4o Mini",
    "gpt-3.5-turbo": "GPT-3.5 Turbo",
    "gpt-3.5-turbo-16k": "GPT-3.5 Turbo 16k",
    "o1-preview": "O1 Preview",
    "o1-mini": "O1 Mini"
}

@babyagi.register_function()
def adaptbaby_agent(task, model="gpt-4o", conversation_history=[]):
    """An enhanced agent that processes tasks using OpenAI's API and maintains memory."""
    global agent_memory
    logger.info(f"Processing task: {task}")

    try:
        # Debug: Print the current OpenAI API key
        current_key = os.getenv('OPENAI_API_KEY')
        logger.info(f"Current OpenAI API key: {current_key[:5]}...{current_key[-5:]}")

        # Prepare conversation context
        context = "\n".join([f"{msg['role']}: {msg['content']}" for msg in conversation_history])
        
        # Analyze the task
        task_analysis = babyagi.gpt_call(f"Given the following conversation:\n{context}\n\nAnalyze and categorize this task: {task}")
        
        # Generate a plan
        plan = babyagi.gpt_call(f"Given the following conversation and task analysis:\n{context}\n{task_analysis}\n\nCreate a step-by-step plan to accomplish this task: {task}")
        
        # Execute the plan (simulated)
        execution_result = babyagi.gpt_call(f"Given the following conversation, task analysis, and plan:\n{context}\n{task_analysis}\n{plan}\n\nSimulate the execution of this plan: {plan}")
        
        # Summarize the result
        summary = babyagi.gpt_call(f"Given the following conversation, task analysis, plan, and execution result:\n{context}\n{task_analysis}\n{plan}\n{execution_result}\n\nSummarize the result of this task execution.")
        
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
        model = data.get('model', 'gpt-4o')
        conversation_history = data.get('conversation_history', [])
        conversation_history.append({"role": "user", "content": message})
        
        result = adaptbaby_agent(message, model, conversation_history)
        
        response = {
            "role": "assistant",
            "content": result.get('summary', 'No summary available.'),
            "full_response": result
        }
        conversation_history.append(response)
        
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