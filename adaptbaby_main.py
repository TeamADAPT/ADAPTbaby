#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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

# Rest of the code remains the same...
