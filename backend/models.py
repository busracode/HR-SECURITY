from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
from utils_security import SecurityManager

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(120), nullable=False)
    last_name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='Candidate')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    
    candidate = db.relationship('Candidate', uselist=False, back_populates='user')
    applications_reviewed = db.relationship('Application', foreign_keys='Application.reviewed_by', back_populates='reviewer')
    
    def set_password(self, password):
        self.password_hash = SecurityManager.hash_password(password)
    
    def check_password(self, password):
        return SecurityManager.verify_password(self.password_hash, password)
    
    def has_role(self, role_name):
        return self.role == role_name
    
    def __repr__(self):
        return f'<User {self.email} ({self.role})>'

class Candidate(db.Model):
    __tablename__ = 'candidates'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)
    full_name = db.Column(db.String(120), nullable=False)
    position = db.Column(db.String(100), nullable=False)
    department = db.Column(db.String(100), nullable=False)
    
    salary_encrypted = db.Column(db.Text, nullable=True)
    phone_encrypted = db.Column(db.Text, nullable=True)
    
    school = db.Column(db.String(150), nullable=False)
    gpa = db.Column(db.Float)
    experience_years = db.Column(db.Integer)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    user = db.relationship('User', back_populates='candidate')
    applications = db.relationship('Application', back_populates='candidate', cascade='all, delete-orphan')
    
    def get_decrypted_salary(self):
        if self.salary_encrypted:
            try:
                return SecurityManager.decrypt_data(self.salary_encrypted)
            except Exception as e:
                print(f"Salary decrypt error: {str(e)}")
                return None
        return None
    
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

class Application(db.Model):
    __tablename__ = 'applications'
    
    id = db.Column(db.Integer, primary_key=True)
    candidate_id = db.Column(db.Integer, db.ForeignKey('candidates.id'), nullable=False)
    
    position = db.Column(db.String(100), nullable=False)
    salary_expected = db.Column(db.Text) # Storing encrypted salary string
    department = db.Column(db.String(100), nullable=False)
    school = db.Column(db.String(150))
    gpa = db.Column(db.Float)
    
    status = db.Column(db.String(20), default='submitted')
    application_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    reviewed_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    review_date = db.Column(db.DateTime)
    notes = db.Column(db.Text)
    
    candidate = db.relationship('Candidate', back_populates='applications')
    reviewer = db.relationship('User', foreign_keys=[reviewed_by], back_populates='applications_reviewed')
    
    def is_pending(self):
        return self.status == 'submitted'
    
    def is_accepted(self):
        return self.status == 'accepted'
    
    def is_rejected(self):
        return self.status == 'rejected'
    
    def __repr__(self):
        return f'<Application {self.position} - {self.status}>'

class AccessLog(db.Model):
    __tablename__ = 'access_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    action = db.Column(db.String(100), nullable=False)
    resource = db.Column(db.String(100))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    ip_address = db.Column(db.String(45))
    
    user = db.relationship('User')
    
    def __repr__(self):
        return f'<Log {self.user_id} - {self.action}>'

def init_db(app):
    with app.app_context():
        db.create_all()
        print("Database initialized successfully.")