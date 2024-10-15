#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os

# Check if running in a virtual environment
if not hasattr(sys, 'real_prefix') and not sys.prefix == sys.base_prefix:
    print("This script should be run from within a virtual environment.")
    sys.exit(1)

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

# Rest of the code remains the same...

if __name__ == "__main__":
    print(f"Python version: {sys.version}")
    print(f"Python executable: {sys.executable}")
    print(f"Current working directory: {os.getcwd()}")
    with app.app_context():
        db.create_all()
    app.run(debug=True)
