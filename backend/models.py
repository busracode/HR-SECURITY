from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
from utils_security import SecurityManager

db = SQLAlchemy()


# AUTHENTICATION + ACCESS CONTROL: Represents a registered user in the system
# Stores hashed passwords (never plaintext) and a role field used for RBAC enforcement
class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(120), nullable=False)
    last_name = db.Column(db.String(120), nullable=False)
    # Email is indexed for fast lookup during login
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    # AUTHENTICATION: Only the bcrypt hash is stored — never the plaintext password
    password_hash = db.Column(db.String(255), nullable=False)
    # ACCESS CONTROL (RBAC): Role determines which routes the user can access (e.g., "Candidate", "HR")
    role = db.Column(db.String(20), nullable=False, default='Candidate')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)

    candidate = db.relationship('Candidate', uselist=False, back_populates='user')
    applications_reviewed = db.relationship('Application', foreign_keys='Application.reviewed_by',
                                            back_populates='reviewer')

    # AUTHENTICATION: Hash the password using SecurityManager (bcrypt) before storing
    def set_password(self, password):
        self.password_hash = SecurityManager.hash_password(password)

    # AUTHENTICATION: Compare a plaintext password against the stored hash during login
    def check_password(self, password):
        return SecurityManager.verify_password(self.password_hash, password)

    # ACCESS CONTROL (RBAC): Helper to check whether this user holds a specific role
    def has_role(self, role_name):
        return self.role == role_name

    def __repr__(self):
        return f'<User {self.email} ({self.role})>'


# Represents a job applicant — linked one-to-one with a User account
# Sensitive fields (salary, phone) are stored encrypted, never as plaintext
class Candidate(db.Model):
    __tablename__ = 'candidates'

    id = db.Column(db.Integer, primary_key=True)
    # Each candidate is tied to exactly one user account
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)
    full_name = db.Column(db.String(120), nullable=False)
    position = db.Column(db.String(100), nullable=False)
    department = db.Column(db.String(100), nullable=False)

    # ENCRYPTION: Salary and phone are stored as Fernet-encrypted ciphertext
    salary_encrypted = db.Column(db.Text, nullable=True)
    phone_encrypted = db.Column(db.Text, nullable=True)

    school = db.Column(db.String(150), nullable=False)
    gpa = db.Column(db.Float)
    experience_years = db.Column(db.Integer)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = db.relationship('User', back_populates='candidate')
    # Deleting a candidate also removes all their applications (cascade)
    applications = db.relationship('Application', back_populates='candidate', cascade='all, delete-orphan')

    # ENCRYPTION: Decrypt the stored salary ciphertext for display
    # Returns None if the field is empty or decryption fails
    def get_decrypted_salary(self):
        if self.salary_encrypted:
            try:
                return SecurityManager.decrypt_data(self.salary_encrypted)
            except Exception as e:
                print(f"Salary decrypt error: {str(e)}")
                return None
        return None

    # ENCRYPTION: Decrypt the stored phone ciphertext for display
    # Returns None if the field is empty or decryption fails
    def get_decrypted_phone(self):
        if self.phone_encrypted:
            try:
                return SecurityManager.decrypt_data(self.phone_encrypted)
            except Exception as e:
                print(f"Phone decrypt error: {str(e)}")
                return None
        return None

    def __repr__(self):
        return f'<Candidate {self.full_name}>'


# Represents a job application submitted by a candidate
# The expected salary is stored encrypted — decrypted only when displayed to HR
class Application(db.Model):
    __tablename__ = 'applications'

    id = db.Column(db.Integer, primary_key=True)
    candidate_id = db.Column(db.Integer, db.ForeignKey('candidates.id'), nullable=False)

    position = db.Column(db.String(100), nullable=False)
    # ENCRYPTION: Salary is stored as ciphertext — never as plaintext
    salary_expected = db.Column(db.Text)
    department = db.Column(db.String(100), nullable=False)
    school = db.Column(db.String(150))
    gpa = db.Column(db.Float)

    # Application lifecycle: submitted -> reviewing -> accepted / rejected
    status = db.Column(db.String(20), default='submitted')
    application_date = db.Column(db.DateTime, default=datetime.utcnow)

    # ACCESS CONTROL: Records which HR user reviewed this application
    reviewed_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    review_date = db.Column(db.DateTime)
    notes = db.Column(db.Text)

    candidate = db.relationship('Candidate', back_populates='applications')
    reviewer = db.relationship('User', foreign_keys=[reviewed_by], back_populates='applications_reviewed')

    # Status helper methods for cleaner conditional checks across the app
    def is_pending(self):
        return self.status == 'submitted'

    def is_accepted(self):
        return self.status == 'accepted'

    def is_rejected(self):
        return self.status == 'rejected'

    def __repr__(self):
        return f'<Application {self.position} - {self.status}>'


# Audit log model — records which user performed which action and when
# Supports accountability and security monitoring
class AccessLog(db.Model):
    __tablename__ = 'access_logs'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    action = db.Column(db.String(100), nullable=False)
    resource = db.Column(db.String(100))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    # IP address is recorded to help detect suspicious access patterns
    ip_address = db.Column(db.String(45))

    user = db.relationship('User')

    def __repr__(self):
        return f'<Log {self.user_id} - {self.action}>'


# Creates all database tables within the Flask application context
def init_db(app):
    with app.app_context():
        db.create_all()
        print("Database initialized successfully.")