from flask_jwt_extended import create_access_token, get_jwt_identity
from datetime import timedelta

def generate_token(user_id):
    access_token = create_access_token(
        identity=user_id,
        expires_delta=timedelta(days=1)
    )
    return access_token

def get_current_user_id():
    return get_jwt_identity()
