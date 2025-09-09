from flask import Blueprint

auth_bp = Blueprint('auth', __name__)
trip_bp = Blueprint('trips', __name__)
from .auth import *  # This imports all routes from auth.py
from .trips import *  # This imports all routes from trips.py
