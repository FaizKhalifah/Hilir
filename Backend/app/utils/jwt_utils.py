# app/utils/jwt_utils.py

import jwt
from datetime import datetime, timedelta
from flask import current_app, request, jsonify
from functools import wraps

def generate_parent_jwt_token(parent):
    payload = {
        "id": parent.id,
        "email": parent.email,
        "role": "parent",  # Include role as "parent"
        "exp": datetime.utcnow() + timedelta(days=1)  # Token expires in 1 day
    }
    token = jwt.encode(payload, current_app.config["SECRET_KEY"], algorithm="HS256")
    return token

def generate_psychologist_jwt_token(psychologist):
    payload = {
        "id": psychologist.id,
        "email": psychologist.email,
        "role": "psychologist",  # Include role as "psychologist"
        "exp": datetime.utcnow() + timedelta(hours=1)  # Token expires in 1 hour
    }
    return jwt.encode(payload, current_app.config["SECRET_KEY"], algorithm="HS256")

def decode_jwt_token(token):
    try:
        decoded_payload = jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=["HS256"])
        return decoded_payload
    except jwt.ExpiredSignatureError:
        return None  # Token has expired
    except jwt.InvalidTokenError:
        return None  # Token is invalid

# General JWT required decorator
def jwt_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get("Authorization", "").replace("Bearer ", "")
        
        if not token:
            return jsonify({"error": "Token is missing!"}), 401

        data = decode_jwt_token(token)
        if data is None:
            return jsonify({"error": "Token is invalid or expired!"}), 401

        request.user_id = data["id"]
        request.role = data.get("role")
        
        return f(*args, **kwargs)
    
    return decorated_function

# Parent-only decorator
def parent_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get("Authorization", "").replace("Bearer ", "")
        
        if not token:
            return jsonify({"error": "Token is missing!"}), 401

        data = decode_jwt_token(token)
        if data is None or data.get("role") != "parent":
            return jsonify({"error": "Access forbidden: Parent only"}), 403

        request.parent_id = data["id"]
        return f(*args, **kwargs)
    
    return decorated_function

# Psychologist-only decorator
def psychologist_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get("Authorization", "").replace("Bearer ", "")
        
        if not token:
            return jsonify({"error": "Token is missing!"}), 401

        data = decode_jwt_token(token)
        if data is None or data.get("role") != "psychologist":
            return jsonify({"error": "Access forbidden: Psychologist only"}), 403

        request.psychologist_id = data["id"]
        return f(*args, **kwargs)
    
    return decorated_function