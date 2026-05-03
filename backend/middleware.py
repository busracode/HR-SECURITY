import jwt
import datetime
from functools import wraps
from flask import request, jsonify, current_app
import os

# AUTHENTICATION: Retrieve the secret key used to sign and verify JWT tokens
# Falls back to a default value if SECRET_KEY is not set in the environment
def get_secret_key():
    return os.getenv("SECRET_KEY", "hr_security_secret_key")

# AUTHENTICATION: Generate a signed JWT token after a successful login
# The token encodes the user's ID, full name, role, and a 2-hour expiry time
# This token is used by all protected routes to verify identity and enforce access control
def generate_token(user_id, first_name, last_name, role):
    """
    Generates a JWT token after successful login.
    Token contains the user's ID, name, and role.
    """
    payload = {
        "id": user_id,
        "first_name": first_name,
        "last_name": last_name,
        "role": role,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=2)
    }
    return jwt.encode(payload, get_secret_key(), algorithm="HS256")

# ACCESS CONTROL: Decorator that protects routes requiring a valid login
# Extracts and verifies the JWT from the Authorization header
# Unauthorized users (missing or invalid token) are blocked with a 401 response
def token_required(f):
    """
    Decorator for protected routes.
    Returns 401 if token is missing or invalid.
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("Authorization")
        if not token:
            return jsonify({"error": "Token is missing!"}), 401
        try:
            token = token.replace("Bearer ", "")
            data = jwt.decode(token, get_secret_key(), algorithms=["HS256"])
            request.user = data
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token has expired!"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token!"}), 401
        return f(*args, **kwargs)
    return decorated

# ACCESS CONTROL (RBAC): Decorator that restricts routes to HR (admin) users only
# Reuses token_required logic and additionally checks that the user's role is "HR"
# Non-HR users are blocked with a 403 response — this enforces the admin-only page requirement
def hr_required(f):
    """
    Decorator for HR-only routes.
    Returns 403 if the user is not an HR.
    """
    @wraps(f)
    @token_required
    def decorated(*args, **kwargs):
        if request.user.get("role") != "HR":
            return jsonify({"error": "Access denied! HR only."}), 403
        return f(*args, **kwargs)
    return decorated