"""
Configuration file for Student Performance Predictor
"""
import os

# Database Configuration
import os
DB_PATH = os.path.join(os.path.dirname(__file__), 'database.db')
SQLALCHEMY_DATABASE_URI = f'sqlite:///{DB_PATH}'
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Flask Secret Key
SECRET_KEY = 'your_secret_key_change_in_production'

# Upload Configuration
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'gif'}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size

# Session Configuration
PERMANENT_SESSION_LIFETIME = 3600  # 1 hour

# Departments
DEPARTMENTS = [
    'CSE',
    'ECE',
    
    'Mech',
    'Civil',
    'IT',
    'Biotech',
    'AIML'
]

# Years
YEARS = [1, 2, 3]

# Semesters
SEMESTERS = [1, 2, 3, 4, 5, 6]

# Prediction Categories
PREDICTION_CATEGORIES = {
    'Good': (75, 100),
    'Average': (50, 74),
    'At-Risk': (0, 49)
}
