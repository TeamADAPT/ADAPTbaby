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
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_cohere import Cohere
from langchain.schema import HumanMessage
import litellm
from transformers import pipeline
from huggingface_hub import snapshot_download
import requests
import pygments
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

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

# Initialize rate limiter
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

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

# Available models
MODELS = {
    'gpt-4o': 'OpenAI GPT-4O',
    'gemini-pro': 'Google Gemini Pro',
    'claude-3-5-sonnet-20240620': 'Anthropic Claude 3.5 Sonnet',
    'cohere-command': 'Cohere Command',
    'groq-mixtral': 'Groq Mixtral-8x7B-32768',
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

# ... (rest of the code, including routes and other functionality)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
