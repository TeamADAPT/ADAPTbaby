import os
import babyagi
from flask import request, jsonify, render_template
from dotenv import load_dotenv
import logging
from datetime import datetime
from langchain_community.llms import OpenAI
from langchain_community.chat_models import ChatOpenAI
from langchain.schema import HumanMessage
from litellm import completion

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

print("Starting ADAPTbaby application...")
logger.info("Initializing ADAPTbaby application")

# Load environment variables
load_dotenv()

# Initialize agent memory
agent_memory = []

# Available models
AVAILABLE_MODELS = {
    "gpt-4o": "GPT-4o",
    "gpt-4o-mini": "GPT-4o Mini",
    "gpt-3.5-turbo": "GPT-3.5 Turbo",
    "gpt-3.5-turbo-16k": "GPT-3.5 Turbo 16k",
    "ai21-jumbo-instruct": "AI21 Jumbo Instruct",
    "cohere-command-r": "Cohere Command R",
    "cohere-command-r-plus": "Cohere Command R Plus",
    "meta-llama-3-70b-instruct": "Meta Llama 3 70B Instruct",
    "meta-llama-3-8b-instruct": "Meta Llama 3 8B Instruct",
    "mixtral-large": "Mixtral Large",
    "mistral-small": "Mistral Small",
    "phi-3-medium-instruct-12b": "Phi-3 Medium Instruct 12B",
}

def get_llm(model_key):
    if model_key.startswith("gpt-"):
        return ChatOpenAI(model_name=model_key, temperature=0.7, openai_api_key=os.getenv('OpenAI_PROJECT_API_KEY'))
    elif model_key in ["ai21-jumbo-instruct", "cohere-command-r", "cohere-command-r-plus", "meta-llama-3-70b-instruct", "meta-llama-3-8b-instruct", "mixtral-large", "mistral-small", "phi-3-medium-instruct-12b"]:
        return f"azure_ai/{model_key}"
    else:
        return ChatOpenAI(temperature=0.7, openai_api_key=os.getenv('OpenAI_PROJECT_API_KEY'))

def langchain_completion(prompt, model_key="gpt-3.5-turbo"):
    llm = get_llm(model_key)
    if isinstance(llm, str) and llm.startswith("azure_ai/"):
        response = completion(
            model=llm,
            messages=[{"role": "user", "content": prompt}],
            api_key=os.getenv('TeamADAPT_GitHub_FINE_GRAINED_PAT'),
            api_base=os.getenv('GITHUB_MODELS_ENDPOINT')
        )
        return response.choices[0].message.content
    else:
        messages = [HumanMessage(content=prompt)]
        response = llm(messages)
        return response.content

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