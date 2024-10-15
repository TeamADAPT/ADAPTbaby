#!/data/projects/active/ADAPTbaby/adaptbaby_venv/bin/python3
# -*- coding: utf-8 -*-

import sys
import os

print(f"Python version: {sys.version}")
print(f"Python executable: {sys.executable}")
print(f"Current working directory: {os.getcwd()}")

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

# Define models (User, ModelUsage, etc.) here...

@app.route('/')
def index():
    return render_template('index.html')

# Other routes (test_models, dashboard, etc.) go here...

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
