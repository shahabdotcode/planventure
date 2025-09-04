from datetime import datetime
from . import db
from flask_bcrypt import Bcrypt
from utils.auth import generate_token, get_jwt_identity

bcrypt = Bcrypt()

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<User {self.email}>'

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    @classmethod
    def create(cls, email, password):
        user = cls(email=email)
        user.set_password(password)
        return user

    def generate_auth_token(self):
        return generate_token(self.id)

    @staticmethod
    def verify_auth_token(token):
        try:
            user_id = get_jwt_identity()
            return User.query.get(user_id)
        except:
            return None
