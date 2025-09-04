from flask import Blueprint

auth_bp = Blueprint('auth', __name__)

from .auth import *  # This imports all routes from auth.py
