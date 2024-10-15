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

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

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

# Set up API clients
openai_client = ChatOpenAI(model_name="gpt-4o", api_key=os.environ.get('OPENAI_API_KEY'))
anthropic_client = ChatAnthropic(model="claude-3-5-sonnet-20240620", api_key=os.environ.get('ANTHROPIC_API_KEY'))
google_client = ChatGoogleGenerativeAI(model="gemini-pro", api_key=os.environ.get('GOOGLE_API_KEY'))

# GitHub Models endpoint and API key
github_models_endpoint = os.environ.get('GITHUB_MODELS_ENDPOINT')
github_api_key = os.environ.get('TeamADAPT_GitHub_FINE_GRAINED_PAT')

# Available models
MODELS = {
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

# ModelUsage model for tracking
class ModelUsage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    model = db.Column(db.String(80), nullable=False)
    prompt = db.Column(db.Text, nullable=False)
    response_time = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class ProtectedModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin

admin.add_view(ProtectedModelView(User, db.session))
admin.add_view(ProtectedModelView(ModelUsage, db.session))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    return redirect(url_for('test_models_ui'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            flash('Logged in successfully.', 'success')
            return redirect(url_for('test_models_ui'))
        else:
            flash('Invalid username or password.', 'error')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully.', 'success')
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists.', 'error')
        else:
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
            new_user = User(username=username, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful. Please log in.', 'success')
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/test_models_ui')
@login_required
def test_models_ui():
    return render_template('test_models.html')

@app.route('/test_models', methods=['POST'])
@login_required
@limiter.limit("10 per minute")
def test_models():
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

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        # Create an admin user if it doesn't exist
        admin_user = User.query.filter_by(username='admin').first()
        if not admin_user:
            admin_password = os.environ.get('ADMIN_PASSWORD', 'admin_password')
            hashed_password = bcrypt.generate_password_hash(admin_password).decode('utf-8')
            admin_user = User(username='admin', password=hashed_password, is_admin=True)
            db.session.add(admin_user)
            db.session.commit()
    logger.info("ADAPTbaby application created. Starting the server...")
    app.run(host='0.0.0.0', port=8080, debug=True)
