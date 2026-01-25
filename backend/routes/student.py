"""
Student Routes - Mark Entry, Prediction, Profile Management
"""
from flask import Blueprint, request, jsonify, session
from models import db, Student, Marks, Prediction, Certification, Competition
from backend.prediction_model import predictor
from datetime import datetime
import os
from werkzeug.utils import secure_filename

student_bp = Blueprint('student', __name__, url_prefix='/api/student')

ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'gif'}
UPLOAD_FOLDER = 'uploads'

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def check_student_session():
    """Check if user is logged in as student"""
    if 'user_id' not in session or session.get('user_type') != 'student':
        return False, jsonify({'error': 'Not authenticated'}), 401
    return True, None, None

# ==================== MARK ENTRY ====================

@student_bp.route('/add-marks', methods=['POST'])
def add_marks():
    """
    Add marks for a subject in a semester
    Expected JSON: {
        "semester": 1,
        "subject_name": "Mathematics",
        "marks_obtained": 85,
        "attendance_percentage": 90,
        "internal_marks": 40,
        "assignment_score": 18
    }
    """
    authenticated, error, code = check_student_session()
    if not authenticated:
        return error, code
    
    data = request.get_json()
    student_id = session['user_id']
    
    # Validation
    required_fields = ['semester', 'subject_name', 'marks_obtained', 'attendance_percentage', 'internal_marks', 'assignment_score']
    if not all(k in data for k in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400
    
    # Validate ranges
    if not (0 <= data['marks_obtained'] <= 100):
        return jsonify({'error': 'Marks must be between 0-100'}), 400
    if not (0 <= data['attendance_percentage'] <= 100):
        return jsonify({'error': 'Attendance must be between 0-100'}), 400
    if not (0 <= data['internal_marks'] <= 50):
        return jsonify({'error': 'Internal marks must be between 0-50'}), 400
    if not (0 <= data['assignment_score'] <= 20):
        return jsonify({'error': 'Assignment score must be between 0-20'}), 400
    
    try:
        # Create mark entry
        mark = Marks(
            student_id=student_id,
            semester=int(data['semester']),
            subject_name=data['subject_name'],
            marks_obtained=float(data['marks_obtained']),
            attendance_percentage=float(data['attendance_percentage']),
            internal_marks=float(data['internal_marks']),
            assignment_score=float(data['assignment_score'])
        )
        
        db.session.add(mark)
        db.session.commit()
        
        return jsonify({
            'message': 'Marks added successfully',
            'mark_id': mark.mark_id
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@student_bp.route('/get-semester-marks/<int:semester>', methods=['GET'])
def get_semester_marks(semester):
    """Get all marks for a specific semester"""
    authenticated, error, code = check_student_session()
    if not authenticated:
        return error, code
    
    student_id = session['user_id']
    
    marks = Marks.query.filter_by(student_id=student_id, semester=semester).all()
    
    marks_list = []
    for mark in marks:
        marks_list.append({
            'mark_id': mark.mark_id,
            'subject_name': mark.subject_name,
            'marks_obtained': mark.marks_obtained,
            'attendance_percentage': mark.attendance_percentage,
            'internal_marks': mark.internal_marks,
            'assignment_score': mark.assignment_score,
            'entry_date': mark.entry_date.strftime('%Y-%m-%d %H:%M:%S')
        })
    
    return jsonify({
        'semester': semester,
        'marks': marks_list,
        'total_subjects': len(marks)
    }), 200

@student_bp.route('/get-all-marks', methods=['GET'])
def get_all_marks():
    """Get all marks across all semesters"""
    authenticated, error, code = check_student_session()
    if not authenticated:
        return error, code
    
    student_id = session['user_id']
    marks = Marks.query.filter_by(student_id=student_id).order_by(Marks.semester).all()
    
    marks_by_semester = {}
    for mark in marks:
        sem = mark.semester
        if sem not in marks_by_semester:
            marks_by_semester[sem] = []
        
        marks_by_semester[sem].append({
            'subject_name': mark.subject_name,
            'marks_obtained': mark.marks_obtained,
            'attendance_percentage': mark.attendance_percentage,
            'internal_marks': mark.internal_marks,
            'assignment_score': mark.assignment_score
        })
    
    return jsonify(marks_by_semester), 200

# ==================== PREDICTION ====================

@student_bp.route('/predict/<int:semester>', methods=['GET'])
def get_prediction(semester):
    """
    Get prediction for a specific semester
    Calculates average of all subjects in that semester
    """
    authenticated, error, code = check_student_session()
    if not authenticated:
        return error, code
    
    student_id = session['user_id']
    
    # Get all marks for the semester
    marks = Marks.query.filter_by(student_id=student_id, semester=semester).all()
    
    if not marks:
        return jsonify({'error': 'No marks found for this semester'}), 404
    
    # Calculate averages
    avg_marks = sum(m.marks_obtained for m in marks) / len(marks)
    avg_attendance = sum(m.attendance_percentage for m in marks) / len(marks)
    avg_internal = sum(m.internal_marks for m in marks) / len(marks)
    avg_assignment = sum(m.assignment_score for m in marks) / len(marks)
    
    # Get certifications and competitions count
    cert_count = Certification.query.filter_by(student_id=student_id).count()
    comp_count = Competition.query.filter_by(student_id=student_id).count()
                
    prediction_data = predictor.predict(avg_marks, avg_attendance, avg_internal, avg_assignment, cert_count, comp_count)
    
    # Save prediction to database
    try:
        prediction = Prediction(
            student_id=student_id,
            semester=semester,
            prediction_result=prediction_data['category'],
            prediction_score=prediction_data['score']
        )
        
        db.session.add(prediction)
        db.session.commit()
    except:
        db.session.rollback()
    
    return jsonify({
        'semester': semester,
        'prediction': prediction_data['category'],
        'score': prediction_data['score'],
        'details': {
            'avg_marks': round(avg_marks, 2),
            'avg_attendance': round(avg_attendance, 2),
            'avg_internal': round(avg_internal, 2),
            'avg_assignment': round(avg_assignment, 2),
            'certifications': cert_count,
            'competitions': comp_count
        },
        'subjects_count': len(marks)
    }), 200

@student_bp.route('/get-all-predictions', methods=['GET'])
def get_all_predictions():
    """Get prediction history for all semesters"""
    authenticated, error, code = check_student_session()
    if not authenticated:
        return error, code
    
    student_id = session['user_id']
    
    # Get all semesters that have marks
    marks_semesters = db.session.query(Marks.semester).filter_by(student_id=student_id).distinct().all()
    marks_semesters = [s[0] for s in marks_semesters]
    
    # Auto-generate predictions for semesters with marks but no predictions
    for semester in marks_semesters:
        existing_pred = Prediction.query.filter_by(student_id=student_id, semester=semester).first()
        if not existing_pred:
            # Generate prediction for this semester
            marks = Marks.query.filter_by(student_id=student_id, semester=semester).all()
            if marks:
                avg_marks = sum(m.marks_obtained for m in marks) / len(marks)
                avg_attendance = sum(m.attendance_percentage for m in marks) / len(marks)
                avg_internal = sum(m.internal_marks for m in marks) / len(marks)
                avg_assignment = sum(m.assignment_score for m in marks) / len(marks)
                
                # Get certifications and competitions count for this semester (approximate by recent ones)
                cert_count = Certification.query.filter_by(student_id=student_id).count()
                comp_count = Competition.query.filter_by(student_id=student_id).count()
                
                prediction_data = predictor.predict(avg_marks, avg_attendance, avg_internal, avg_assignment, cert_count, comp_count)
                
                try:
                    prediction = Prediction(
                        student_id=student_id,
                        semester=semester,
                        prediction_result=prediction_data['category'],
                        prediction_score=prediction_data['score']
                    )
                    db.session.add(prediction)
                    db.session.commit()
                except Exception as e:
                    db.session.rollback()
                    print(f"Error saving prediction for semester {semester}: {e}")
    
    # Force commit any pending changes
    db.session.commit()
    
    # Now get all predictions
    predictions = Prediction.query.filter_by(student_id=student_id).order_by(Prediction.semester).all()
    
    pred_list = []
    for pred in predictions:
        pred_list.append({
            'semester': pred.semester,
            'category': pred.prediction_result,
            'score': pred.prediction_score,
            'generated_at': pred.generated_at.strftime('%Y-%m-%d %H:%M:%S')
        })
    
    return jsonify({'predictions': pred_list}), 200

# ==================== PROFILE & CERTIFICATIONS ====================

@student_bp.route('/get-profile', methods=['GET'])
def get_profile():
    """Get student profile information"""
    authenticated, error, code = check_student_session()
    if not authenticated:
        return error, code
    
    student_id = session['user_id']
    student = Student.query.get(student_id)
    
    if not student:
        return jsonify({'error': 'Student not found'}), 404
    
    return jsonify({
        'student_id': student.student_id,
        'name': student.name,
        'roll_no': student.roll_no,
        'department': student.department,
        'year': student.year,
        'email': student.email,
        'created_at': student.created_at.strftime('%Y-%m-%d')
    }), 200

@student_bp.route('/upload-certificate', methods=['POST'])
def upload_certificate():
    """Upload certification document"""
    authenticated, error, code = check_student_session()
    if not authenticated:
        return error, code
    
    student_id = session['user_id']
    
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    cert_title = request.form.get('cert_title')
    issue_date_str = request.form.get('issue_date')
    
    if not cert_title or not issue_date_str:
        return jsonify({'error': 'Missing certificate title or date'}), 400
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': 'File type not allowed'}), 400
    
    try:
        # Create uploads directory if it doesn't exist
        if not os.path.exists(UPLOAD_FOLDER):
            os.makedirs(UPLOAD_FOLDER)
        
        # Save file
        filename = secure_filename(f"{student_id}_{datetime.utcnow().timestamp()}_{file.filename}")
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(file_path)
        
        # Parse date
        issue_date = datetime.strptime(issue_date_str, '%Y-%m-%d').date()
        
        # Save to database
        cert = Certification(
            student_id=student_id,
            cert_title=cert_title,
            cert_file_path=file_path,
            issue_date=issue_date
        )
        
        db.session.add(cert)
        db.session.commit()
        
        return jsonify({
            'message': 'Certificate uploaded successfully',
            'cert_id': cert.cert_id
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@student_bp.route('/get-certifications', methods=['GET'])
def get_certifications():
    """Get all uploaded certifications"""
    authenticated, error, code = check_student_session()
    if not authenticated:
        return error, code
    
    student_id = session['user_id']
    certs = Certification.query.filter_by(student_id=student_id).all()
    
    cert_list = []
    for cert in certs:
        # Convert file path to accessible URL
        file_url = f"/uploads/{os.path.basename(cert.cert_file_path)}"
        cert_list.append({
            'cert_id': cert.cert_id,
            'title': cert.cert_title,
            'file_path': file_url,
            'issue_date': cert.issue_date.strftime('%Y-%m-%d'),
            'upload_date': cert.upload_date.strftime('%Y-%m-%d')
        })
    
    return jsonify({'certifications': cert_list}), 200

@student_bp.route('/upload-competition', methods=['POST'])
def upload_competition():
    """Upload competition/achievement details"""
    authenticated, error, code = check_student_session()
    if not authenticated:
        return error, code
    
    student_id = session['user_id']
    
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    comp_title = request.form.get('comp_title')
    achievement_type = request.form.get('achievement_type')
    event_date_str = request.form.get('event_date')
    
    if not all([comp_title, achievement_type, event_date_str]):
        return jsonify({'error': 'Missing required fields'}), 400
    
    if achievement_type not in ['Participant', 'Winner', 'Runner-up']:
        return jsonify({'error': 'Invalid achievement type'}), 400
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': 'File type not allowed'}), 400
    
    try:
        # Create uploads directory if it doesn't exist
        if not os.path.exists(UPLOAD_FOLDER):
            os.makedirs(UPLOAD_FOLDER)
        
        # Save file
        filename = secure_filename(f"{student_id}_{datetime.utcnow().timestamp()}_{file.filename}")
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(file_path)
        
        # Parse date
        event_date = datetime.strptime(event_date_str, '%Y-%m-%d').date()
        
        # Save to database
        comp = Competition(
            student_id=student_id,
            comp_title=comp_title,
            achievement_type=achievement_type,
            comp_file_path=file_path,
            event_date=event_date
        )
        
        db.session.add(comp)
        db.session.commit()
        
        return jsonify({
            'message': 'Competition record uploaded successfully',
            'comp_id': comp.comp_id
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@student_bp.route('/get-competitions', methods=['GET'])
def get_competitions():
    """Get all competition records"""
    authenticated, error, code = check_student_session()
    if not authenticated:
        return error, code
    
    student_id = session['user_id']
    comps = Competition.query.filter_by(student_id=student_id).all()
    
    comp_list = []
    for comp in comps:
        # Convert file path to accessible URL
        file_url = f"/uploads/{os.path.basename(comp.comp_file_path)}"
        comp_list.append({
            'comp_id': comp.comp_id,
            'title': comp.comp_title,
            'achievement_type': comp.achievement_type,
            'file_path': file_url,
            'event_date': comp.event_date.strftime('%Y-%m-%d'),
            'upload_date': comp.upload_date.strftime('%Y-%m-%d')
        })
    
    return jsonify({'competitions': comp_list}), 200
