from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, verify_jwt_in_request
from models import db
from models.user import User
import re

auth_bp = Blueprint('auth', __name__, url_prefix='/api')

def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

@auth_bp.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        
        if not data or not data.get('email') or not data.get('password'):
            return jsonify({'error': 'Email and password are required'}), 400
            
        email = data['email']
        password = data['password']
        
        if not is_valid_email(email):
            return jsonify({'error': 'Invalid email format'}), 400
            
        if len(password) < 6:
            return jsonify({'error': 'Password must be at least 6 characters'}), 400
            
        if User.query.filter_by(email=email).first():
            return jsonify({'error': 'Email already registered'}), 409
            
        user = User.create(email=email, password=password)
        db.session.add(user)
        db.session.commit()
        
        return jsonify({'message': 'User registered successfully'}), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        
        if not data or not data.get('email') or not data.get('password'):
            return jsonify({'error': 'Email and password are required'}), 400
            
        user = User.query.filter_by(email=data['email']).first()
        
        if not user or not user.check_password(data['password']):
            return jsonify({'error': 'Invalid email or password'}), 401
            
        # Generate access token
        access_token = create_access_token(identity=str(user.id))
        
        return jsonify({
            'message': 'Login successful',
            'access_token': access_token,
            'user': {
                'id': user.id,
                'email': user.email
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def get_current_user():
    verify_jwt_in_request()
    user_id = get_jwt_identity()
    return User.query.get(user_id)

def auth_required(f):
    @jwt_required()
    def decorated_function(*args, **kwargs):
        try:
            current_user = get_current_user()
            if not current_user:
                return jsonify({'error': 'User not found'}), 404
            return f(current_user, *args, **kwargs)
        except Exception as e:
            return jsonify({'error': str(e)}), 401
    decorated_function.__name__ = f.__name__
    return decorated_function

# Example protected route
@auth_bp.route('/me', methods=['GET'])
@auth_required
def get_user_profile(current_user):
    return jsonify({
        'id': current_user.id,
        'email': current_user.email
    }), 200

# JWT handlers moved to app.py
