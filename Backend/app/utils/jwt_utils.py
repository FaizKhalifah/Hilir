# app/utils/jwt_utils.py

import jwt
import datetime
from flask import current_app, request, jsonify
from functools import wraps

def generate_jwt_token(parent):
    payload = {
        "parent_id": parent.id,
        "email": parent.email,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(days=1)  # Token expires in 1 day
    }
    token = jwt.encode(payload, current_app.config["SECRET_KEY"], algorithm="HS256")
    return token

def decode_jwt_token(token):
    try:
        decoded_payload = jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=["HS256"])
        return decoded_payload
    except jwt.ExpiredSignatureError:
        return None  # Token has expired
    except jwt.InvalidTokenError:
        return None  # Token is invalid

# Decorator to protect routes
def jwt_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]
        
        if not token:
            return jsonify({"error": "Token is missing!"}), 401

        try:
            data = decode_jwt_token(token)
            if data is None:
                raise ValueError("Invalid token")
            request.parent_id = data["parent_id"]
        except Exception as e:
            return jsonify({"error": "Token is invalid or expired!"}), 401

        return f(*args, **kwargs)
    
    return decorated_function
