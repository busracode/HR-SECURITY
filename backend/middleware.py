import jwt
import datetime
from functools import wraps
from flask import request, jsonify

# ============================================================
# CORE REQUIREMENT 2 — Access Control (RBAC)
# "Implement Role-Based Access Control (RBAC)"
# "Unauthorized users must be blocked"
# ============================================================

SECRET_KEY = "hr_security_secret_key"

def generate_token(first_name, last_name, role):
    """
    Generates a JWT token after successful login.
    Token contains the user's name and role.
    """
    payload = {
        "first_name": first_name,
        "last_name": last_name,
        "role": role,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=2)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

def token_required(f):
    """
    Decorator for protected routes.
    Returns 401 if token is missing or invalid.
    Professor requires: "Unauthorized users must be blocked"
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("Authorization")
        if not token:
            return jsonify({"error": "Token is missing!"}), 401
        try:
            token = token.replace("Bearer ", "")
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            request.user = data
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token has expired!"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token!"}), 401
        return f(*args, **kwargs)
    return decorated

def admin_required(f):
    """
    Decorator for Admin-only routes.
    Returns 403 if the user is not an Admin.
    Professor requires: "Admin-only page must exist"
                        "Minimum roles: Admin, User"
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("Authorization")
        if not token:
            return jsonify({"error": "Token is missing!"}), 401
        try:
            token = token.replace("Bearer ", "")
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            if data.get("role") != "Admin":
                return jsonify({"error": "Access denied! Admins only."}), 403
            request.user = data
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token has expired!"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token!"}), 401
        return f(*args, **kwargs)
    return decorated