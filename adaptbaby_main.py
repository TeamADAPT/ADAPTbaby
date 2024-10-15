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
import requests
import plotly.graph_objs as go
import plotly.utils
import json

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

# User model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    api_calls_quota = db.Column(db.Integer, default=1000)
    api_calls_count = db.Column(db.Integer, default=0)

# ModelUsage model for tracking
class ModelUsage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    model = db.Column(db.String(80), nullable=False)
    prompt = db.Column(db.Text, nullable=False)
    response_time = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

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
                groq_data = {
                    "messages": [{"role": "user", "content": test_prompt}],
                    "model": "mixtral-8x7b-32768"
                }
                response = requests.post(groq_url, headers=groq_headers, json=groq_data)
                response.raise_for_status()
                response_content = response.json()['choices'][0]['message']['content']
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

@app.route('/dashboard')
@login_required
def dashboard():
    # Fetch user's testing history
    user_history = ModelUsage.query.filter_by(user_id=current_user.id).order_by(ModelUsage.timestamp.desc()).limit(10).all()
    
    # Generate graphs
    model_usage_graph = create_model_usage_graph()
    response_time_graph = create_response_time_graph()
    
    return render_template('dashboard.html', user_history=user_history, model_usage_graph=model_usage_graph, response_time_graph=response_time_graph)

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

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
