from flask import Flask, request, jsonify
from flask_cors import CORS
from models import (
    init_db, insert_user, get_user_by_email, insert_application, 
    get_all_applications, get_application_by_user, update_application_note,
    get_user_by_id, update_user_role
)
from middleware import generate_token, token_required, hr_required
from security_logic import verify_password, decrypt_data

app = Flask(__name__)
CORS(app)

init_db()

@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    first_name = data.get("first_name")
    last_name = data.get("last_name")
    email = data.get("email")
    password = data.get("password")
    
    if not all([first_name, last_name, email, password]):
        return jsonify({"error": "All fields are required!"}), 400

    success = insert_user(first_name, last_name, email, password)
    if not success:
        return jsonify({"error": "User with this email already exists!"}), 409

    return jsonify({"message": "User registered successfully!"}), 201

@app.route("/hr/upgrade", methods=["POST"])
@token_required
def upgrade_to_hr():
    data = request.get_json()
    secret_code = data.get("secret_code")
    
    if secret_code != "HR-SECURE-2026":
        return jsonify({"error": "Geçersiz İK Yetki Kodu!"}), 403
        
    user_id = request.user["id"]
    update_user_role(user_id, "HR")
    
    return jsonify({"message": "Yetkiniz İK olarak güncellendi! Lütfen tekrar giriş yapın."}), 200


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Email and password required!"}), 400

    user = get_user_by_email(email)
    if not user or not verify_password(user["password"], password):
        return jsonify({"error": "Invalid credentials!"}), 401

    token = generate_token(user["id"], user["first_name"], user["last_name"], user["role"])
    return jsonify({"token": token, "role": user["role"], "user": {"first_name": user["first_name"], "last_name": user["last_name"]}}), 200


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

    existing_app = get_application_by_user(user_id)
    if existing_app:
        return jsonify({"error": "You have already submitted an application!"}), 400

    insert_application(user_id, first_name, last_name, job, school, department, salary)
    return jsonify({"message": "Application submitted successfully!"}), 201


@app.route("/candidate/application", methods=["GET"])
@token_required
def get_my_application():
    if request.user["role"] != "Candidate":
        return jsonify({"error": "Only candidates can access this route!"}), 403
    
    user_id = request.user["id"]
    app_row = get_application_by_user(user_id)
    
    if not app_row:
        return jsonify({"application": None}), 200

    return jsonify({
        "application": {
            "id": app_row["id"],
            "first_name": app_row["first_name"],
            "last_name": app_row["last_name"],
            "job": app_row["job"],
            "school": decrypt_data(app_row["school"]),
            "department": decrypt_data(app_row["department"]),
            "salary": decrypt_data(app_row["salary"])
        }
    }), 200


@app.route("/hr/candidates", methods=["GET"])
@hr_required
def get_all_candidates():
    applications = get_all_applications()
    result = []
    for app_row in applications:
        # Also let's get the user to see if we want email. But not strictly needed right now.
        result.append({
            "id": app_row["id"],
            "name": f'{app_row["first_name"]} {app_row["last_name"]}',
            "position": app_row["job"],
            "evaluator_name": "Sistem", # Placeholder for now
            "decrypted_salary": decrypt_data(app_row["salary"]),
            "secret_note": app_row["secret_note"]
        })
    return jsonify(result), 200

@app.route("/hr/stats", methods=["GET"])
@hr_required
def get_hr_stats():
    applications = get_all_applications()
    return jsonify({
        "totalCandidates": len(applications),
        "pendingReviews": len([a for a in applications if not a["secret_note"]]),
        "alerts": 0
    }), 200

@app.route("/hr/candidates/<int:candidate_id>/note", methods=["POST"])
@hr_required
def add_note(candidate_id):
    data = request.get_json()
    note = data.get("note", "")
    update_application_note(candidate_id, note)
    return jsonify({"message": "Note updated successfully!"}), 200

if __name__ == "__main__":
    app.run(debug=True)