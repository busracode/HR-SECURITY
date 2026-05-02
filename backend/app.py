from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv

# Load environment variables first
load_dotenv()

from models import db, User, Candidate, Application, init_db
from middleware import generate_token, token_required, hr_required
from config import DevelopmentConfig
from utils_security import SecurityManager

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
CORS(app)

# Initialize SQLAlchemy
db.init_app(app)

# Create tables inside app context
with app.app_context():
    db.create_all()

@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    first_name = data.get("first_name")
    last_name = data.get("last_name")
    email = data.get("email")
    password = data.get("password")
    
    if not all([first_name, last_name, email, password]):
        return jsonify({"error": "All fields are required!"}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"error": "User with this email already exists!"}), 409

    new_user = User(
        first_name=first_name,
        last_name=last_name,
        email=email,
        role="Candidate"
    )
    new_user.set_password(password)
    
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully!"}), 201


@app.route("/hr/upgrade", methods=["POST"])
@token_required
def upgrade_to_hr():
    data = request.get_json()
    secret_code = data.get("secret_code")
    
    if secret_code != "HR-SECURE-2026":
        return jsonify({"error": "Geçersiz İK Yetki Kodu!"}), 403
        
    user_id = request.user["id"]
    user = User.query.get(user_id)
    if user:
        user.role = "HR"
        db.session.commit()
    
    return jsonify({"message": "Yetkiniz İK olarak güncellendi! Lütfen tekrar giriş yapın."}), 200


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Email and password required!"}), 400

    user = User.query.filter_by(email=email).first()
    
    if not user or not user.check_password(password):
        return jsonify({"error": "Invalid credentials!"}), 401

    token = generate_token(user.id, user.first_name, user.last_name, user.role)
    return jsonify({
        "token": token, 
        "role": user.role, 
        "user": {
            "first_name": user.first_name, 
            "last_name": user.last_name
        }
    }), 200


@app.route("/apply", methods=["POST"])
@token_required
def apply():
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

    # Ensure user has a candidate profile
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
        
    existing_app = Application.query.filter_by(candidate_id=candidate.id).first()
    if existing_app:
        return jsonify({"error": "You have already submitted an application!"}), 400

    # Encrypt the sensitive salary
    encrypted_salary = SecurityManager.encrypt_data(salary)

    new_app = Application(
        candidate_id=candidate.id,
        position=job,
        department=department,
        school=school,
        salary_expected=encrypted_salary
    )
    
    db.session.add(new_app)
    db.session.commit()
    
    return jsonify({"message": "Application submitted successfully!"}), 201


@app.route("/candidate/application", methods=["GET"])
@token_required
def get_my_application():
    if request.user["role"] != "Candidate":
        return jsonify({"error": "Only candidates can access this route!"}), 403
    
    user_id = request.user["id"]
    candidate = Candidate.query.filter_by(user_id=user_id).first()
    
    if not candidate:
        return jsonify({"application": None}), 200
        
    app_row = Application.query.filter_by(candidate_id=candidate.id).first()
    
    if not app_row:
        return jsonify({"application": None}), 200

    # Use utils_security logic to decrypt. Usually only HR does this, but keeping it per previous logic
    decrypted_salary = "Gizli"
    if app_row.salary_expected:
        try:
            decrypted_salary = SecurityManager.decrypt_data(app_row.salary_expected)
        except Exception:
            pass

    # Note: Previous code decrypted school/department as well, but in new models they are plain text.
    # We will return them as they are.
    user = candidate.user
    return jsonify({
        "application": {
            "id": app_row.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "job": app_row.position,
            "school": app_row.school,
            "department": app_row.department,
            "salary": decrypted_salary
        }
    }), 200


@app.route("/hr/candidates", methods=["GET"])
@hr_required
def get_all_candidates():
    applications = Application.query.all()
    result = []
    for app_row in applications:
        candidate = app_row.candidate
        user = candidate.user
        
        decrypted_salary = ""
        if app_row.salary_expected:
            try:
                decrypted_salary = SecurityManager.decrypt_data(app_row.salary_expected)
            except Exception:
                decrypted_salary = "[ŞİFRELEME HATASI]"

        result.append({
            "id": app_row.id,
            "name": f"{user.first_name} {user.last_name}",
            "position": app_row.position,
            "evaluator_name": "Sistem", # Placeholder for now
            "decrypted_salary": decrypted_salary,
            "secret_note": app_row.notes
        })
    return jsonify(result), 200


@app.route("/hr/stats", methods=["GET"])
@hr_required
def get_hr_stats():
    applications = Application.query.all()
    pending = [a for a in applications if not a.notes]
    return jsonify({
        "totalCandidates": len(applications),
        "pendingReviews": len(pending),
        "alerts": 0
    }), 200


@app.route("/hr/candidates/<int:candidate_id>/note", methods=["POST"])
@hr_required
def add_note(candidate_id):
    data = request.get_json()
    note = data.get("note", "")
    
    app_row = Application.query.get(candidate_id)
    if app_row:
        app_row.notes = note
        app_row.reviewed_by = request.user["id"]
        app_row.status = 'reviewing'
        db.session.commit()
        return jsonify({"message": "Note updated successfully!"}), 200
    return jsonify({"error": "Application not found"}), 404


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')