"""
Authentication Routes - Student Signup and Login
"""
from flask import Blueprint, request, jsonify, session
from models import db, Student, Staff
from werkzeug.security import generate_password_hash, check_password_hash
import re

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

# Helper function to validate email
def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email)

# ==================== STUDENT AUTHENTICATION ====================

@auth_bp.route('/student/signup', methods=['POST'])
def student_signup():
    """
    Student Registration
    Expected JSON: {
        "name": "John Doe",
        "roll_no": "CS001",
        "department": "Computer Science and Engineering",
        "year": 1,
        "email": "john@example.com",
        "password": "password123"
    }
    """
    data = request.get_json()
    
    # Validation
    if not all(k in data for k in ['name', 'roll_no', 'department', 'year', 'password']):
        return jsonify({'error': 'Missing required fields'}), 400
    
    if len(data['password']) < 6:
        return jsonify({'error': 'Password must be at least 6 characters'}), 400
    
    if Student.query.filter_by(roll_no=data['roll_no']).first():
        return jsonify({'error': 'Roll number already exists'}), 400
    
    try:
        # Create new student
        student = Student(
            name=data['name'],
            roll_no=data['roll_no'],
            department=data['department'],
            year=int(data['year']),
            email=data.get('email', '')
        )
        student.set_password(data['password'])
        
        db.session.add(student)
        db.session.commit()
        
        return jsonify({
            'message': 'Student registered successfully',
            'student_id': student.student_id,
            'name': student.name
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/student/login', methods=['POST'])
def student_login():
    """
    Student Login
    Expected JSON: {
        "roll_no": "CS001",
        "password": "password123"
    }
    """
    data = request.get_json()
    
    if not all(k in data for k in ['roll_no', 'password']):
        return jsonify({'error': 'Missing roll_no or password'}), 400
    
    student = Student.query.filter_by(roll_no=data['roll_no']).first()
    
    if not student or not student.check_password(data['password']):
        return jsonify({'error': 'Invalid roll number or password'}), 401
    
    # Store in session
    session['user_id'] = student.student_id
    session['user_type'] = 'student'
    session['name'] = student.name
    
    return jsonify({
        'message': 'Login successful',
        'student_id': student.student_id,
        'name': student.name,
        'roll_no': student.roll_no,
        'department': student.department,
        'year': student.year
    }), 200

@auth_bp.route('/student/logout', methods=['POST'])
def student_logout():
    """Student Logout"""
    session.clear()
    return jsonify({'message': 'Logout successful'}), 200

# ==================== STAFF AUTHENTICATION ====================

@auth_bp.route('/staff/signup', methods=['POST'])
def staff_signup():
    """
    Staff Registration
    Expected JSON: {
        "name": "John Doe",
        "username": "staff001",
        "email": "john@college.edu",
        "department": "Computer Science",
        "password": "password123"
    }
    """
    data = request.get_json()
    
    # Validation
    if not all(k in data for k in ['name', 'username', 'email', 'department', 'password']):
        return jsonify({'error': 'Missing required fields'}), 400
    
    if len(data['password']) < 6:
        return jsonify({'error': 'Password must be at least 6 characters'}), 400
    
    if Staff.query.filter_by(username=data['username']).first():
        return jsonify({'error': 'Username already exists'}), 400
    
    try:
        # Create new staff
        staff = Staff(
            name=data['name'],
            username=data['username'],
            email=data.get('email', ''),
            department=data['department'],
            role='staff'
        )
        staff.set_password(data['password'])
        
        db.session.add(staff)
        db.session.commit()
        
        return jsonify({
            'message': 'Staff account created successfully',
            'staff_id': staff.staff_id,
            'name': staff.name
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/hod/signup', methods=['POST'])
def hod_signup():
    """
    HOD Registration
    Expected JSON: {
        "name": "Dr. John Doe",
        "username": "hod001",
        "email": "john@college.edu",
        "department": "Computer Science",
        "password": "password123"
    }
    """
    data = request.get_json()
    
    # Validation
    if not all(k in data for k in ['name', 'username', 'email', 'department', 'password']):
        return jsonify({'error': 'Missing required fields'}), 400
    
    if len(data['password']) < 6:
        return jsonify({'error': 'Password must be at least 6 characters'}), 400
    
    if Staff.query.filter_by(username=data['username']).first():
        return jsonify({'error': 'Username already exists'}), 400
    
    try:
        # Create new HOD
        hod = Staff(
            name=data['name'],
            username=data['username'],
            email=data.get('email', ''),
            department=data['department'],
            role='hod'
        )
        hod.set_password(data['password'])
        
        db.session.add(hod)
        db.session.commit()
        
        return jsonify({
            'message': 'HOD account created successfully',
            'staff_id': hod.staff_id,
            'name': hod.name
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/staff/login', methods=['POST'])
def staff_login():
    """
    Staff/HOD Login
    Expected JSON: {
        "username": "staff001",
        "password": "password123"
    }
    """
    data = request.get_json()
    
    if not all(k in data for k in ['username', 'password']):
        return jsonify({'error': 'Missing username or password'}), 400
    
    staff = Staff.query.filter_by(username=data['username']).first()
    
    if not staff or not staff.check_password(data['password']):
        return jsonify({'error': 'Invalid username or password'}), 401
    
    # Store in session
    session['user_id'] = staff.staff_id
    session['user_type'] = staff.role  # 'staff' or 'hod'
    session['name'] = staff.name
    session['department'] = staff.department
    
    return jsonify({
        'message': 'Login successful',
        'staff_id': staff.staff_id,
        'name': staff.name,
        'role': staff.role,
        'department': staff.department
    }), 200

@auth_bp.route('/staff/logout', methods=['POST'])
def staff_logout():
    """Staff/HOD Logout"""
    session.clear()
    return jsonify({'message': 'Logout successful'}), 200

@auth_bp.route('/check-session', methods=['GET'])
def check_session():
    """Check if user is logged in"""
    if 'user_id' in session:
        return jsonify({
            'logged_in': True,
            'user_type': session.get('user_type'),
            'name': session.get('name')
        }), 200
    return jsonify({'logged_in': False}), 200
