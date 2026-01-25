"""
Database Models for Student Performance Predictor
"""
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import hashlib

db = SQLAlchemy()

class Student(db.Model):
    __tablename__ = 'students'
    
    student_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    roll_no = db.Column(db.String(50), unique=True, nullable=False)
    department = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    marks = db.relationship('Marks', backref='student', lazy=True, cascade='all, delete-orphan')
    predictions = db.relationship('Prediction', backref='student', lazy=True, cascade='all, delete-orphan')
    certifications = db.relationship('Certification', backref='student', lazy=True, cascade='all, delete-orphan')
    competitions = db.relationship('Competition', backref='student', lazy=True, cascade='all, delete-orphan')
    
    def set_password(self, password):
        self.password_hash = hashlib.sha256(password.encode()).hexdigest()
    
    def check_password(self, password):
        return self.password_hash == hashlib.sha256(password.encode()).hexdigest()

class Marks(db.Model):
    __tablename__ = 'marks'
    
    mark_id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.student_id'), nullable=False)
    semester = db.Column(db.Integer, nullable=False)
    subject_name = db.Column(db.String(100), nullable=False)
    marks_obtained = db.Column(db.Float, nullable=False)
    attendance_percentage = db.Column(db.Float, nullable=False)
    internal_marks = db.Column(db.Float, nullable=False)
    assignment_score = db.Column(db.Float, nullable=False)
    entry_date = db.Column(db.DateTime, default=datetime.utcnow)

class Prediction(db.Model):
    __tablename__ = 'predictions'
    
    prediction_id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.student_id'), nullable=False)
    semester = db.Column(db.Integer, nullable=False)
    prediction_result = db.Column(db.String(50), nullable=False)
    prediction_score = db.Column(db.Float, nullable=False)
    generated_at = db.Column(db.DateTime, default=datetime.utcnow)

class Certification(db.Model):
    __tablename__ = 'certifications'
    
    cert_id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.student_id'), nullable=False)
    cert_title = db.Column(db.String(150), nullable=False)
    cert_file_path = db.Column(db.String(255), nullable=False)
    issue_date = db.Column(db.Date, nullable=False)
    upload_date = db.Column(db.DateTime, default=datetime.utcnow)

class Competition(db.Model):
    __tablename__ = 'competitions'
    
    comp_id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.student_id'), nullable=False)
    comp_title = db.Column(db.String(150), nullable=False)
    achievement_type = db.Column(db.String(50), nullable=False)
    comp_file_path = db.Column(db.String(255), nullable=False)
    event_date = db.Column(db.Date, nullable=False)
    upload_date = db.Column(db.DateTime, default=datetime.utcnow)

class Staff(db.Model):
    __tablename__ = 'staff'
    
    staff_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100))
    password_hash = db.Column(db.String(255), nullable=False)
    department = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # 'staff' or 'hod'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def set_password(self, password):
        self.password_hash = hashlib.sha256(password.encode()).hexdigest()
    
    def check_password(self, password):
        return self.password_hash == hashlib.sha256(password.encode()).hexdigest()
