from flask import request, jsonify
from functools import wraps
import jwt
from datetime import datetime, timedelta, timezone
    
SECRET_KEY = "a super secret key"

def encode_token(customer_id):
    payload = {
        'exp': datetime.now(timezone.utc) + timedelta(days=0, hours=1),
        'iat': datetime.now(timezone.utc),
        'sub': str(customer_id)
    }
    
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    
    return token

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if "Authorization" in request.headers:
            token = request.headers["Authorization"].split(" ")[1]

            if not token:
                return jsonify({"message": "Token is missing!"}), 401
            
            try:
                data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
                current_user = data["sub"]
            except jwt.ExpiredSignatureError:
                return jsonify({"message": "Token has expired!"}), 401
            except jwt.InvalidTokenError:
                return jsonify({"message": "Invalid token!"}), 401
            
            return f(current_user, *args, **kwargs)
        else:
            return jsonify({"message": "You must be logged in!"}), 401
    return decorated
