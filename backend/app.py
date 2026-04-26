from flask import Flask, request, jsonify
from flask_cors import CORS
from models import init_db, insert_user, get_user, insert_application, get_all_applications
from middleware import generate_token, token_required, admin_required
from security_logic import verify_password, decrypt_data

# ============================================================
# Flask app initialization
# ============================================================
app = Flask(__name__)
CORS(app)  # Allows frontend to communicate with backend

# Initialize database tables on startup
init_db()

# ============================================================
# CORE REQUIREMENT 1 — Authentication
# "User registration and login"
# "Passwords must be stored using secure hashing"
# ============================================================

@app.route("/register", methods=["POST"])
def register():
    """
    Registers a new user.
    Password is hashed before storing — no plaintext passwords.
    """
    data = request.get_json()
    first_name = data.get("first_name")
    last_name = data.get("last_name")
    password = data.get("password")
    role = data.get("role", "User")  # Default role is User

    if not first_name or not last_name or not password:
        return jsonify({"error": "All fields are required!"}), 400

    success = insert_user(first_name, last_name, password, role)
    if not success:
        return jsonify({"error": "User already exists!"}), 409

    return jsonify({"message": "User registered successfully!"}), 201


@app.route("/login", methods=["POST"])
def login():
    """
    Authenticates the user and returns a JWT token.
    Token contains the user's name and role for access control.
    """
    data = request.get_json()
    first_name = data.get("first_name")
    last_name = data.get("last_name")
    password = data.get("password")

    user = get_user(first_name, last_name)
    if not user or not verify_password(user["password"], password):
        return jsonify({"error": "Invalid credentials!"}), 401

    token = generate_token(first_name, last_name, user["role"])
    return jsonify({"token": token, "role": user["role"]}), 200


# ============================================================
# CORE REQUIREMENT 2 — Access Control (RBAC)
# "Implement Role-Based Access Control (RBAC)"
# ============================================================

@app.route("/apply", methods=["POST"])
@token_required  # Only logged-in users can apply
def apply():
    """
    Submits a job application form.
    Sensitive fields are encrypted before storing.
    Professor requires: "Encrypt sensitive data before storing"
    """
    data = request.get_json()
    user = request.user

    first_name = data.get("first_name")
    last_name = data.get("last_name")
    job = data.get("job")
    school = data.get("school")
    department = data.get("department")
    salary = data.get("salary")

    if not all([first_name, last_name, job, school, department, salary]):
        return jsonify({"error": "All fields are required!"}), 400

    insert_application(
        user_id=None,
        first_name=first_name,
        last_name=last_name,
        job=job,
        school=school,
        department=department,
        salary=salary
    )
    return jsonify({"message": "Application submitted successfully!"}), 201


# ============================================================
# CORE REQUIREMENT 2 — Access Control (RBAC)
# "Admin-only page must exist (e.g., /admin)"
#                     "Unauthorized users must be blocked"
# CORE REQUIREMENT 3 — Encryption
# "Decrypt data when displaying it"
# ============================================================

@app.route("/admin", methods=["GET"])
@admin_required  # Only Admin role can access this route
def admin():
    """
    Returns all job applications — Admin only.
    Encrypted fields are decrypted before returning to the admin.
    """
    applications = get_all_applications()
    result = []
    for app_row in applications:
        result.append({
            "id": app_row["id"],
            "first_name": app_row["first_name"],
            "last_name": app_row["last_name"],
            "job": app_row["job"],
            "school": decrypt_data(app_row["school"]),         # Decrypted for admin
            "department": decrypt_data(app_row["department"]), # Decrypted for admin
            "salary": decrypt_data(app_row["salary"])          # Decrypted for admin
        })
    return jsonify(result), 200


if __name__ == "__main__":
    app.run(debug=True)