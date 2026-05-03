from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv

# Load environment variables from .env file before importing app modules
# This ensures database credentials, secret keys, and encryption keys are available at startup
load_dotenv()

from models import db, User, Candidate, Application, init_db
from middleware import generate_token, token_required, hr_required
from config import DevelopmentConfig
from utils_security import SecurityManager

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)

# Enable Cross-Origin Resource Sharing so the frontend can communicate with the API
CORS(app)

# Bind SQLAlchemy to this Flask application instance
db.init_app(app)

# Create all database tables defined in models if they don't already exist
with app.app_context():
    db.create_all()


# --- AUTHENTICATION: User Registration ---
# Allows new users to create an account with the default role "Candidate"
# Passwords are never stored in plaintext — set_password() hashes them securely (e.g., bcrypt)
@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    first_name = data.get("first_name")
    last_name = data.get("last_name")
    email = data.get("email")
    password = data.get("password")

    # Validate that all required fields are present
    if not all([first_name, last_name, email, password]):
        return jsonify({"error": "All fields are required!"}), 400

    # Validate email format using SecurityManager
    if not SecurityManager.validate_email(email):
        return jsonify({"error": "Invalid email format!"}), 400

    # Validate password strength using SecurityManager
    if not SecurityManager.validate_password(password):
        return jsonify({"error": "Password must be at least 8 characters and contain uppercase, lowercase, digit and special character!"}), 400

    # Prevent duplicate accounts by checking if the email is already registered
    if User.query.filter_by(email=email).first():
        return jsonify({"error": "User with this email already exists!"}), 409

    new_user = User(
        first_name=first_name,
        last_name=last_name,
        email=email,
        role="Candidate"  # Default role assigned to every new registrant
    )
    # Hash and store the password securely — no plaintext passwords are saved
    new_user.set_password(password)

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully!"}), 201


# --- ACCESS CONTROL: Role Elevation to HR (Admin) ---
# A logged-in Candidate can upgrade their role to "HR" (admin) by providing a secret code.
# This route is protected by @token_required, so only authenticated users can call it.
# In RBAC terms, this is the mechanism for granting elevated (admin) privileges.
@app.route("/hr/upgrade", methods=["POST"])
@token_required
def upgrade_to_hr():
    data = request.get_json()
    secret_code = data.get("secret_code")

    # Verify the secret authorization code before granting HR/admin role
    # The code is read from the environment variable for security
    if secret_code != os.getenv("HR_SECRET_CODE"):
        return jsonify({"error": "Invalid HR authorization code!"}), 403

    user_id = request.user["id"]
    user = User.query.get(user_id)
    if user:
        # Elevate the user's role to HR (admin level) in the database
        user.role = "HR"
        db.session.commit()

    return jsonify({"message": "Your role has been updated to HR! Please log in again."}), 200


# --- AUTHENTICATION: User Login ---
# Validates credentials and issues a JWT token that encodes the user's id, name, and role.
# The token is used by all subsequent protected routes to verify identity and enforce RBAC.
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Email and password required!"}), 400

    user = User.query.filter_by(email=email).first()

    # check_password() compares the submitted password against the stored hash
    if not user or not user.check_password(password):
        return jsonify({"error": "Invalid credentials!"}), 401

    # Generate a signed JWT containing the user's role for downstream access control checks
    token = generate_token(user.id, user.first_name, user.last_name, user.role)
    return jsonify({
        "token": token,
        "role": user.role,
        "user": {
            "first_name": user.first_name,
            "last_name": user.last_name
        }
    }), 200


# --- ACCESS CONTROL + ENCRYPTION: Submit Job Application ---
# Protected route — requires a valid JWT (@token_required).
# Only users with the "Candidate" role are permitted; HR users are blocked (RBAC enforcement).
# The expected salary is encrypted with Fernet/AES before being stored to protect sensitive data.
@app.route("/apply", methods=["POST"])
@token_required
def apply():
    # RBAC check: only Candidates may submit applications
    if request.user["role"] != "Candidate":
        return jsonify({"error": "Only candidates can apply!"}), 403

    data = request.get_json()
    user_id = request.user["id"]

    first_name = data.get("first_name")
    last_name = data.get("last_name")
    job = data.get("job")
    school = data.get("school")
    department = data.get("department")
    salary = data.get("salary")

    if not all([first_name, last_name, job, school, department, salary]):
        return jsonify({"error": "All fields are required!"}), 400

    # Create a Candidate profile for this user if one does not already exist
    candidate = Candidate.query.filter_by(user_id=user_id).first()
    if not candidate:
        candidate = Candidate(
            user_id=user_id,
            full_name=f"{first_name} {last_name}",
            position=job,
            department=department,
            school=school
        )
        db.session.add(candidate)
        db.session.commit()

    # Prevent a candidate from submitting more than one application
    existing_app = Application.query.filter_by(candidate_id=candidate.id).first()
    if existing_app:
        return jsonify({"error": "You have already submitted an application!"}), 400

    # ENCRYPTION: Encrypt the salary before storing it in the database.
    # SecurityManager uses symmetric encryption (Fernet/AES) so the value can be decrypted later.
    encrypted_salary = SecurityManager.encrypt_data(salary)

    new_app = Application(
        candidate_id=candidate.id,
        position=job,
        department=department,
        school=school,
        salary_expected=encrypted_salary  # Only the ciphertext is persisted — never plaintext
    )

    db.session.add(new_app)
    db.session.commit()

    return jsonify({"message": "Application submitted successfully!"}), 201


# --- ACCESS CONTROL + ENCRYPTION: Candidate Views Their Own Application ---
# Protected route — requires a valid JWT (@token_required).
# RBAC: only the "Candidate" role may access this endpoint.
# The encrypted salary is decrypted at retrieval time so the candidate can see their own data.
@app.route("/candidate/application", methods=["GET"])
@token_required
def get_my_application():
    # RBAC check: HR users cannot access candidate-specific routes
    if request.user["role"] != "Candidate":
        return jsonify({"error": "Only candidates can access this route!"}), 403

    user_id = request.user["id"]
    candidate = Candidate.query.filter_by(user_id=user_id).first()

    if not candidate:
        return jsonify({"application": None}), 200

    app_row = Application.query.filter_by(candidate_id=candidate.id).first()

    if not app_row:
        return jsonify({"application": None}), 200

    # ENCRYPTION: Decrypt the stored salary for display.
    # If decryption fails (e.g., key mismatch), fall back to a masked placeholder.
    decrypted_salary = "Hidden"
    if app_row.salary_expected:
        try:
            decrypted_salary = SecurityManager.decrypt_data(app_row.salary_expected)
        except Exception:
            pass

    user = candidate.user
    return jsonify({
        "application": {
            "id": app_row.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "job": app_row.position,
            "school": app_row.school,
            "department": app_row.department,
            "salary": decrypted_salary  # Plaintext salary returned only to the owning candidate
        }
    }), 200


# --- ACCESS CONTROL + ENCRYPTION: HR Lists All Candidates (Admin-Only Page) ---
# Protected by @hr_required — the decorator verifies the JWT and checks that role == "HR".
# This is the admin-only endpoint; any non-HR request is rejected before reaching this logic.
# Encrypted salary fields are decrypted here so HR staff can review full application details.
@app.route("/hr/candidates", methods=["GET"])
@hr_required
def get_all_candidates():
    applications = Application.query.all()
    result = []
    for app_row in applications:
        candidate = app_row.candidate
        user = candidate.user

        # ENCRYPTION: Decrypt each candidate's salary for HR review
        decrypted_salary = ""
        if app_row.salary_expected:
            try:
                decrypted_salary = SecurityManager.decrypt_data(app_row.salary_expected)
            except Exception:
                decrypted_salary = "[DECRYPTION ERROR]"

        result.append({
            "id": app_row.id,
            "name": f"{user.first_name} {user.last_name}",
            "position": app_row.position,
            "evaluator_name": "System",  # Placeholder — will be replaced with actual reviewer logic
            "decrypted_salary": decrypted_salary,
            "secret_note": app_row.notes
        })
    return jsonify(result), 200


# --- ACCESS CONTROL: HR Dashboard Statistics (Admin-Only) ---
# Returns aggregate metrics (total applications, pending reviews, alerts).
# @hr_required ensures only authenticated HR/admin users can retrieve this data.
@app.route("/hr/stats", methods=["GET"])
@hr_required
def get_hr_stats():
    applications = Application.query.all()
    # Applications without a note are considered pending review
    pending = [a for a in applications if not a.notes]
    return jsonify({
        "totalCandidates": len(applications),
        "pendingReviews": len(pending),
        "alerts": 0
    }), 200


# --- ACCESS CONTROL: HR Adds a Review Note to an Application (Admin-Only) ---
# @hr_required enforces that only HR/admin users can annotate candidate applications.
# Also records which HR user performed the review and updates the application status.
@app.route("/hr/candidates/<int:candidate_id>/note", methods=["POST"])
@hr_required
def add_note(candidate_id):
    data = request.get_json()
    note = data.get("note", "")

    app_row = Application.query.get(candidate_id)
    if app_row:
        app_row.notes = note
        app_row.reviewed_by = request.user["id"]  # Track which HR user added the note
        app_row.status = 'reviewing'  # Move application to "under review" state
        db.session.commit()
        return jsonify({"message": "Note updated successfully!"}), 200
    return jsonify({"error": "Application not found"}), 404


if __name__ == "__main__":
    # Run the development server — debug=True enables auto-reload and detailed error pages
    app.run(debug=True, host='0.0.0.0')