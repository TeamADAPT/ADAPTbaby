import os
import time
import json
import logging
import ast
from datetime import datetime

import requests
import networkx as nx
import plotly.graph_objs as go
import plotly.utils

from flask import Flask, request, jsonify, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_bcrypt import Bcrypt
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from dotenv import load_dotenv

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

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Groq client setup
groq_api_key = os.environ.get('GROQ_API_KEY')
groq_url = "https://api.groq.com/openai/v1/chat/completions"
groq_headers = {
    "Authorization": f"Bearer {groq_api_key}",
    "Content-Type": "application/json"
}

# Available models
MODELS = {
    'groq-mixtral': 'Groq Mixtral-8x7B-32768',
    'gpt-4o': 'OpenAI GPT-4O',
    'gemini-pro': 'Google Gemini Pro',
    'claude-3-5-sonnet-20240620': 'Anthropic Claude 3.5 Sonnet',
    'meta-llama-3-70b-instruct': 'GitHub Meta Llama 3 70B Instruct',
    'mixtral-large': 'GitHub Mixtral Large',
    'phi-3-medium-instruct-12b': 'GitHub Phi-3 Medium Instruct 12B'
}

# Database Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    api_calls_quota = db.Column(db.Integer, default=1000)
    api_calls_count = db.Column(db.Integer, default=0)

class ModelUsage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    model = db.Column(db.String(80), nullable=False)
    prompt = db.Column(db.Text, nullable=False)
    response_time = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

# Routes
@app.route('/test_models', methods=['POST'])
@login_required
def test_models():
    results = {}
    data = request.json
    test_prompt = data.get('prompt', "Hello, can you introduce yourself?")
    
    for model_key, model_name in MODELS.items():
        try:
            start_time = time.time()
            if model_key == 'groq-mixtral':
                response_content = test_groq_model(test_prompt)
            else:
                # Placeholder for other models
                response_content = f"Test response for {model_name}"
            
            end_time = time.time()
            response_time = end_time - start_time
            
            results[model_key] = {
                "status": "success",
                "response": response_content[:500] + "..." if len(response_content) > 500 else response_content,
                "response_time": round(response_time, 2)
            }
            logger.info(f"Successfully tested {model_name} in {response_time:.2f} seconds")
            
            # Log usage
            log_model_usage(current_user.id, model_key, test_prompt, response_time)
        except Exception as e:
            results[model_key] = {
                "status": "error",
                "message": str(e),
                "response_time": None
            }
            logger.error(f"Error testing {model_name}: {str(e)}")
    
    return jsonify(results)

@app.route('/dashboard')
@login_required
def dashboard():
    user_history = get_user_history(current_user.id)
    model_usage_graph = create_model_usage_graph()
    response_time_graph = create_response_time_graph()
    function_graph = create_function_graph()
    
    return render_template('dashboard.html', 
                           user_history=user_history, 
                           model_usage_graph=model_usage_graph, 
                           response_time_graph=response_time_graph, 
                           function_graph=function_graph)

@app.route('/self_build', methods=['POST'])
@login_required
def self_build():
    data = request.json
    prompt = data.get('prompt', "")
    
    function_name, function_body = generate_function(prompt)
    
    if function_name and function_body:
        result = execute_generated_function(function_body)
        return jsonify({
            "status": "success",
            "function_name": function_name,
            "function_body": function_body,
            "result": result
        })
    else:
        return jsonify({
            "status": "error",
            "message": "Failed to generate a valid function"
        })

# Helper functions
def test_groq_model(prompt):
    groq_data = {
        "messages": [{"role": "user", "content": prompt}],
        "model": "mixtral-8x7b-32768"
    }
    response = requests.post(groq_url, headers=groq_headers, json=groq_data)
    response.raise_for_status()
    return response.json()['choices'][0]['message']['content']

def log_model_usage(user_id, model, prompt, response_time):
    usage = ModelUsage(user_id=user_id, model=model, prompt=prompt, response_time=response_time)
    db.session.add(usage)
    db.session.commit()

def get_user_history(user_id, limit=10):
    return ModelUsage.query.filter_by(user_id=user_id).order_by(ModelUsage.timestamp.desc()).limit(limit).all()

def create_model_usage_graph():
    model_usage = db.session.query(ModelUsage.model, db.func.count(ModelUsage.id)).group_by(ModelUsage.model).all()
    models, counts = zip(*model_usage)
    
    trace = go.Bar(x=models, y=counts)
    layout = go.Layout(title='Model Usage', xaxis=dict(title='Model'), yaxis=dict(title='Usage Count'))
    fig = go.Figure(data=[trace], layout=layout)
    
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

def create_response_time_graph():
    response_times = db.session.query(ModelUsage.model, db.func.avg(ModelUsage.response_time)).group_by(ModelUsage.model).all()
    models, times = zip(*response_times)
    
    trace = go.Bar(x=models, y=times)
    layout = go.Layout(title='Average Response Time by Model', xaxis=dict(title='Model'), yaxis=dict(title='Average Response Time (s)'))
    fig = go.Figure(data=[trace], layout=layout)
    
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

def create_function_graph():
    G = nx.DiGraph()
    G.add_edge("main", "test_models")
    G.add_edge("main", "dashboard")
    G.add_edge("test_models", "test_groq_model")
    G.add_edge("test_models", "log_model_usage")
    G.add_edge("dashboard", "get_user_history")
    G.add_edge("dashboard", "create_model_usage_graph")
    G.add_edge("dashboard", "create_response_time_graph")
    G.add_edge("dashboard", "create_function_graph")

    pos = nx.spring_layout(G)
    edge_trace = go.Scatter(
        x=[], y=[], line=dict(width=0.5, color='#888'), hoverinfo='none', mode='lines')

    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_trace['x'] += tuple([x0, x1, None])
        edge_trace['y'] += tuple([y0, y1, None])

    node_trace = go.Scatter(
        x=[], y=[], text=[], mode='markers', hoverinfo='text',
        marker=dict(
            showscale=True,
            colorscale='YlGnBu',
            reversescale=True,
            color=[],
            size=10,
            colorbar=dict(
                thickness=15,
                title='Node Connections',
                xanchor='left',
                titleside='right'
            ),
            line_width=2))

    for node in G.nodes():
        x, y = pos[node]
        node_trace['x'] += tuple([x])
        node_trace['y'] += tuple([y])
        node_trace['text'] += tuple([node])

    for node, adjacencies in enumerate(G.adjacency()):
        node_trace['marker']['color'] += tuple([len(adjacencies[1])])

    fig = go.Figure(data=[edge_trace, node_trace],
                    layout=go.Layout(
                        title='Function Call Graph',
                        titlefont_size=16,
                        showlegend=False,
                        hovermode='closest',
                        margin=dict(b=20,l=5,r=5,t=40),
                        annotations=[ dict(
                            text="Function relationships",
                            showarrow=False,
                            xref="paper", yref="paper",
                            x=0.005, y=-0.002 ) ],
                        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                    )

    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

def generate_function(prompt):
    # Use Groq to generate a Python function based on the prompt
    function_prompt = f"Generate a Python function that does the following: {prompt}"
    function_code = test_groq_model(function_prompt)
    
    # Extract the function definition from the generated code
    try:
        tree = ast.parse(function_code)
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                function_name = node.name
                function_body = ast.unparse(node)
                return function_name, function_body
    except SyntaxError:
        return None, None

def execute_generated_function(function_body, *args, **kwargs):
    # Execute the generated function
    try:
        exec(function_body, globals())
        function_name = function_body.split("def ")[1].split("(")[0]
        return eval(f"{function_name}(*args, **kwargs)")
    except Exception as e:
        return f"Error executing function: {str(e)}"

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
