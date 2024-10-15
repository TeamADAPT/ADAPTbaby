#!/data/projects/active/ADAPTbaby/adaptbaby_venv/bin/python3
# -*- coding: utf-8 -*-

import sys
import os
from typing import Any

print(f"Python version: {sys.version}")
print(f"Python executable: {sys.executable}")
print(f"Current working directory: {os.getcwd()}")

import time
import json
import logging
import ast
from datetime import datetime

import requests

try:
    import networkx as nx  # type: ignore
    import plotly.graph_objs as go  # type: ignore
    import plotly.utils  # type: ignore
    from flask import Flask, request, jsonify, render_template, redirect, url_for, flash  # type: ignore
    from flask_sqlalchemy import SQLAlchemy  # type: ignore
    from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user  # type: ignore
    from flask_bcrypt import Bcrypt  # type: ignore
    from flask_admin import Admin  # type: ignore
    from flask_admin.contrib.sqla import ModelView  # type: ignore
    from dotenv import load_dotenv  # type: ignore
except ImportError as e:
    print(f"Error importing module: {e}")
    print("Make sure you're running this script in the virtual environment.")
    sys.exit(1)

# Load environment variables
load_dotenv()

# Initialize Flask app
app: Flask = Flask(__name__, template_folder='templates')
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///adaptbaby.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db: SQLAlchemy = SQLAlchemy(app)
bcrypt: Bcrypt = Bcrypt(app)
login_manager: LoginManager = LoginManager(app)
login_manager.login_view = 'login'
admin: Admin = Admin(app, name='ADAPTbaby Admin', template_mode='bootstrap3')

# Define models (User, ModelUsage, etc.) here...

@app.route('/')
def index() -> str:
    return render_template('index.html')

# Other routes (test_models, dashboard, etc.) go here...

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
