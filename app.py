"""
Main Flask Application - Student Performance Predictor
"""
from flask import Flask, render_template, send_from_directory, session
from models import db, Student, Staff
from config import *
from backend.routes.auth import auth_bp
from backend.routes.student import student_bp
from backend.routes.hod import staff_bp
from backend.prediction_model import predictor
import os
from datetime import timedelta

app = Flask(__name__, template_folder='frontend/html', static_folder='frontend', static_url_path='')

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS
app.config['SECRET_KEY'] = SECRET_KEY
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=1)
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

# Create upload folder
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Initialize database
db.init_app(app)

# Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(student_bp)
app.register_blueprint(staff_bp)

# ==================== STATIC FILES ====================

@app.route('/css/<path:filename>')
def serve_css(filename):
    return send_from_directory('frontend/css', filename)

@app.route('/js/<path:filename>')
def serve_js(filename):
    return send_from_directory('frontend/js', filename)

@app.route('/uploads/<path:filename>')
def serve_uploads(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

# ==================== MAIN ROUTES ====================

@app.route('/')
def index():
    """Landing page"""
    return render_template('index.html')

@app.route('/student/signup')
def student_signup_page():
    """Student signup page"""
    return render_template('student_signup.html')

@app.route('/student/login')
def student_login_page():
    """Student login page"""
    return render_template('student_login.html')

@app.route('/staff/signup')
def staff_signup_page():
    """Staff signup page"""
    return render_template('staff_signup.html')

@app.route('/staff/login')
def staff_login_page():
    """Staff login page"""
    return render_template('staff_login.html')

@app.route('/hod/signup')
def hod_signup_page():
    """HOD signup page"""
    return render_template('hod_signup.html')

@app.route('/hod/login')
def hod_login_page():
    """HOD login page"""
    return render_template('hod_login.html')

@app.route('/student/dashboard')
def student_dashboard():
    """Student dashboard"""
    return render_template('student_dashboard.html')

@app.route('/student/marks-entry')
def marks_entry_page():
    """Mark entry page"""
    return render_template('semester_marks_entry.html')

@app.route('/student/prediction')
def prediction_page():
    """Prediction result page"""
    return render_template('prediction_result.html')

@app.route('/student/profile')
def profile_page():
    """Profile view page"""
    return render_template('profile_view.html')

@app.route('/student/certifications')
def certifications_page():
    """Certification upload page"""
    return render_template('certification_upload.html')

@app.route('/staff/dashboard')
def staff_dashboard():
    """Staff dashboard"""
    return render_template('staff_dashboard.html')

@app.route('/hod/dashboard')
def hod_dashboard():
    """HOD dashboard"""
    return render_template('hod_dashboard.html')

# ==================== ERROR HANDLERS ====================

@app.errorhandler(404)
def not_found(error):
    return {'error': 'Page not found'}, 404

@app.errorhandler(500)
def internal_error(error):
    return {'error': 'Internal server error'}, 500

# ==================== INITIALIZATION ====================

def init_app():
    """Initialize application"""
    with app.app_context():
        # Create tables
        db.create_all()
        
        # Always retrain ML model to ensure latest features and prevent feature mismatch
        print("Retraining ML model with latest features...")
        predictor.train()

if __name__ == '__main__':
    init_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
