"""
Staff and HOD Routes - View Student Data
"""
from flask import Blueprint, request, jsonify, session
from models import db, Student, Marks, Prediction, Certification, Competition
import os

staff_bp = Blueprint('staff', __name__, url_prefix='/api/staff')

def check_staff_session():
    """Check if user is logged in as staff"""
    if 'user_id' not in session or session.get('user_type') not in ['staff', 'hod']:
        return False, jsonify({'error': 'Not authenticated'}), 401
    return True, None, None

# ==================== STAFF DASHBOARD ====================

@staff_bp.route('/all-predictions', methods=['GET'])
def all_predictions():
    """Get predictions for all students in department"""
    authenticated, error, code = check_staff_session()
    if not authenticated:
        return error, code
    
    user_type = session.get('user_type')
    department = session.get('department', '').strip() if session.get('department') else None
    
    if user_type == 'staff':
        # Staff can only see their department (case-insensitive)
        students = Student.query.filter(Student.department.ilike(department)).all()
    else:  # hod
        # HOD can see all students
        students = Student.query.all()
    
    results = []
    for student in students:
        predictions = Prediction.query.filter_by(student_id=student.student_id).order_by(Prediction.semester).all()
        
        pred_data = {}
        for pred in predictions:
            pred_data[f'sem_{pred.semester}'] = {
                'category': pred.prediction_result,
                'score': pred.prediction_score
            }
        
        # Get current prediction (latest)
        latest_pred = Prediction.query.filter_by(student_id=student.student_id).order_by(Prediction.generated_at.desc()).first()
        
        # Handle case where no prediction exists (new student)
        current_pred_data = {
            'category': 'Not Available',
            'score': 0,
            'semester': 'N/A'
        }
        if latest_pred:
            current_pred_data = {
                'category': latest_pred.prediction_result,
                'score': latest_pred.prediction_score,
                'semester': latest_pred.semester
            }
        
        results.append({
            'student_id': student.student_id,
            'name': student.name,
            'roll_no': student.roll_no,
            'department': student.department,
            'year': student.year,
            'all_predictions': pred_data,
            'current_prediction': current_pred_data
        })
    
    return jsonify({'students': results}), 200

@staff_bp.route('/student-details/<int:student_id>', methods=['GET'])
def student_details(student_id):
    """Get detailed information about a specific student"""
    authenticated, error, code = check_staff_session()
    if not authenticated:
        return error, code
    
    student = Student.query.get(student_id)
    
    if not student:
        return jsonify({'error': 'Student not found'}), 404
    
    # Get marks
    marks = Marks.query.filter_by(student_id=student_id).order_by(Marks.semester).all()
    marks_data = {}
    for mark in marks:
        sem = mark.semester
        if sem not in marks_data:
            marks_data[sem] = []
        marks_data[sem].append({
            'subject': mark.subject_name,
            'marks': mark.marks_obtained,
            'attendance': mark.attendance_percentage,
            'internal': mark.internal_marks,
            'assignment': mark.assignment_score
        })
    
    # Get predictions
    predictions = Prediction.query.filter_by(student_id=student_id).order_by(Prediction.semester).all()
    pred_data = [
        {
            'semester': p.semester,
            'category': p.prediction_result,
            'score': p.prediction_score
        }
        for p in predictions
    ]
    
    # Get certifications
    certs = Certification.query.filter_by(student_id=student_id).all()
    cert_data = [
        {
            'title': c.cert_title,
            'issue_date': c.issue_date.strftime('%Y-%m-%d'),
            'file_path': f"/uploads/{os.path.basename(c.cert_file_path)}"
        }
        for c in certs
    ]
    
    # Get competitions
    comps = Competition.query.filter_by(student_id=student_id).all()
    comp_data = [
        {
            'title': c.comp_title,
            'achievement': c.achievement_type,
            'event_date': c.event_date.strftime('%Y-%m-%d'),
            'file_path': f"/uploads/{os.path.basename(c.comp_file_path)}"
        }
        for c in comps
    ]
    
    return jsonify({
        'student': {
            'name': student.name,
            'roll_no': student.roll_no,
            'department': student.department,
            'year': student.year,
            'email': student.email
        },
        'marks': marks_data,
        'predictions': pred_data,
        'certifications': cert_data,
        'competitions': comp_data
    }), 200

@staff_bp.route('/search-student', methods=['GET'])
def search_student():
    """Search student by roll number"""
    authenticated, error, code = check_staff_session()
    if not authenticated:
        return error, code
    
    roll_no = request.args.get('roll_no', '').strip()
    
    if not roll_no:
        return jsonify({'error': 'Roll number required'}), 400
    
    # Case-insensitive search
    student = Student.query.filter(Student.roll_no.ilike(roll_no)).first()
    
    if not student:
        return jsonify({'error': 'Student not found'}), 404
    
    return jsonify({
        'student_id': student.student_id,
        'name': student.name,
        'roll_no': student.roll_no,
        'department': student.department,
        'year': student.year
    }), 200

# ==================== HOD SPECIFIC ROUTES ====================

@staff_bp.route('/department-stats', methods=['GET'])
def department_stats():
    """Get department-level statistics (HOD only)"""
    authenticated, error, code = check_staff_session()
    if not authenticated:
        return error, code
    
    if session.get('user_type') != 'hod':
        return jsonify({'error': 'Only HOD can access this'}), 403
    
    # Total students
    total_students = Student.query.count()
    
    # Average performance across all students
    all_predictions = Prediction.query.all()
    avg_score = sum(p.prediction_score for p in all_predictions) / len(all_predictions) if all_predictions else 0
    
    # Performance distribution
    good = len([p for p in all_predictions if p.prediction_result == 'Good Performance'])
    average = len([p for p in all_predictions if p.prediction_result == 'Average Performance'])
    at_risk = len([p for p in all_predictions if p.prediction_result == 'At-Risk Performance'])
    
    # Department-wise breakdown (Count and Avg Score)
    dept_stats = []
    
    # Get all distinct departments
    departments = db.session.query(Student.department).distinct().all()
    
    for dept_row in departments:
        dept_name = dept_row[0]
        if not dept_name:
            continue
            
        # Get students in this department
        dept_students = Student.query.filter_by(department=dept_name).all()
        student_count = len(dept_students)
        
        # Calculate avg score for this department
        dept_scores = []
        for student in dept_students:
            # Get latest prediction score
            latest_pred = Prediction.query.filter_by(student_id=student.student_id).order_by(Prediction.generated_at.desc()).first()
            if latest_pred:
                dept_scores.append(latest_pred.prediction_score)
        
        avg_dept_score = sum(dept_scores) / len(dept_scores) if dept_scores else 0
        
        dept_stats.append({
            'department': dept_name,
            'student_count': student_count,
            'average_score': round(avg_dept_score, 2)
        })
    
    # Sort by average score descending to find top department
    dept_stats.sort(key=lambda x: x['average_score'], reverse=True)
    
    return jsonify({
        'total_students': total_students,
        'average_score': round(avg_score, 2),
        'performance_distribution': {
            'good': good,
            'average': average,
            'at_risk': at_risk
        },
        'department_breakdown': dept_stats
    }), 200

@staff_bp.route('/filter-students', methods=['GET'])
def filter_students():
    """Filter students by year and/or department"""
    authenticated, error, code = check_staff_session()
    if not authenticated:
        return error, code
    
    year = request.args.get('year', type=int)
    department = request.args.get('department')
    
    query = Student.query
    
    if year:
        query = query.filter_by(year=year)
    if department:
        query = query.filter_by(department=department)
    
    students = query.all()
    
    results = []
    for student in students:
        latest_pred = Prediction.query.filter_by(student_id=student.student_id).order_by(Prediction.generated_at.desc()).first()
        
        # Handle case where no prediction exists
        current_pred_data = {
            'category': 'Not Available',
            'score': 0
        }
        if latest_pred:
            current_pred_data = {
                'category': latest_pred.prediction_result,
                'score': latest_pred.prediction_score
            }

        results.append({
            'student_id': student.student_id,
            'name': student.name,
            'roll_no': student.roll_no,
            'year': student.year,
            'department': student.department,
            'current_prediction': current_pred_data
        })
    
    return jsonify({'students': results}), 200

# ==================== CERTIFICATE VIEWING ====================

@staff_bp.route('/all-certificates', methods=['GET'])
def all_certificates():
    """Get all certificates from students in department"""
    authenticated, error, code = check_staff_session()
    if not authenticated:
        return error, code
    
    user_type = session.get('user_type')
    department = session.get('department', '').strip() if session.get('department') else None
    
    if user_type == 'staff':
        # Staff can only see their department (case-insensitive)
        students = Student.query.filter(Student.department.ilike(department)).all()
    else:  # hod
        # HOD can see all students
        students = Student.query.all()
    
    student_ids = [s.student_id for s in students]
    
    # Get all certificates for these students
    certs = Certification.query.filter(Certification.student_id.in_(student_ids)).all()
    
    results = []
    for cert in certs:
        student = Student.query.get(cert.student_id)
        if student:
            # Convert file path to accessible URL
            file_url = f"/uploads/{os.path.basename(cert.cert_file_path)}"
            results.append({
                'cert_id': cert.cert_id,
                'student_id': student.student_id,
                'student_name': student.name,
                'student_roll_no': student.roll_no,
                'student_department': student.department,
                'student_year': student.year,
                'title': cert.cert_title,
                'file_path': file_url,
                'issue_date': cert.issue_date.strftime('%Y-%m-%d'),
                'upload_date': cert.upload_date.strftime('%Y-%m-%d %H:%M:%S')
            })
    
    return jsonify({'certificates': results}), 200

@staff_bp.route('/student-certificates/<int:student_id>', methods=['GET'])
def student_certificates(student_id):
    """Get all certificates for a specific student"""
    authenticated, error, code = check_staff_session()
    if not authenticated:
        return error, code
    
    # Verify student exists and is in staff's department (if staff)
    student = Student.query.get(student_id)
    if not student:
        return jsonify({'error': 'Student not found'}), 404
    
    user_type = session.get('user_type')
    department = session.get('department', '').strip() if session.get('department') else None
    
    if user_type == 'staff' and not student.department.lower() == department.lower():
        return jsonify({'error': 'Access denied'}), 403
    
    # Get certificates
    certs = Certification.query.filter_by(student_id=student_id).all()
    
    results = []
    for cert in certs:
        # Convert file path to accessible URL
        file_url = f"/uploads/{os.path.basename(cert.cert_file_path)}"
        results.append({
            'cert_id': cert.cert_id,
            'title': cert.cert_title,
            'file_path': file_url,
            'issue_date': cert.issue_date.strftime('%Y-%m-%d'),
            'upload_date': cert.upload_date.strftime('%Y-%m-%d %H:%M:%S')
        })
    
    return jsonify({
        'student': {
            'name': student.name,
            'roll_no': student.roll_no,
            'department': student.department,
            'year': student.year
        },
        'certificates': results
    }), 200
