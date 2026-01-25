# Student Performance Predictor - AI-Powered Academic System

A comprehensive web-based system for predicting student performance based on academic metrics and managing student academic profiles.

## Features

### Core Functionality
- **ML-Based Performance Prediction**: Predicts student performance using marks, attendance, internal exam scores, and assignment scores
- **Semester-wise Mark Entry**: Flexible data entry system for 6 semesters with subject-by-subject entry
- **Real-time Performance Analysis**: Instant prediction results with categorization
- **Academic Profile Management**: Upload and manage certifications and competition achievements

### Prediction Categories
- ✅ **Good Performance** (75-100)
- ⚠️ **Average Performance** (50-74)
- ❌ **At-Risk Performance** (0-49)

### Role-Based Access Control
1. **Student**: Enter marks, view predictions, upload certificates, manage profile
2. **Staff**: Monitor student performance, review records, department oversight
3. **HOD**: Department-level analytics, full record access, statistics

## System Requirements

- Python 3.7+
- Flask
- SQLAlchemy
- scikit-learn
- pandas
- numpy

## Installation & Setup

### 1. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 2. Create and Configure Database
```bash
cd /path/to/Student_Performence
python app.py
```
This will automatically create the SQLite database and tables.

### 3. Train ML Model (Optional)
The ML model will train automatically on first run using `backend/training_data.csv`.

### 4. Run the Application
```bash
python app.py
```

The application will start on `http://localhost:5000`

## Project Structure

```
Student_Performence/
├── app.py                          # Main Flask application
├── config.py                       # Configuration settings
├── models.py                       # Database models
├── requirements.txt                # Python dependencies
│
├── backend/
│   ├── prediction_model.py         # ML prediction engine
│   ├── training_data.csv           # Training dataset for ML model
│   └── routes/
│       ├── auth.py                 # Authentication routes
│       ├── student.py              # Student-specific routes
│       └── hod.py                  # Staff/HOD routes
│
├── frontend/
│   ├── html/
│   │   ├── index.html              # Landing page
│   │   ├── student_signup.html     # Student registration
│   │   ├── student_login.html      # Student login
│   │   ├── staff_login.html        # Staff login
│   │   ├── hod_login.html          # HOD login
│   │   ├── student_dashboard.html  # Student dashboard
│   │   ├── semester_marks_entry.html
│   │   ├── prediction_result.html
│   │   ├── profile_view.html
│   │   ├── certification_upload.html
│   │   ├── staff_dashboard.html
│   │   └── hod_dashboard.html
│   │
│   ├── css/
│   │   ├── style.css               # Global styles
│   │   ├── forms.css               # Form styles
│   │   ├── dashboard.css           # Dashboard styles
│   │   └── table.css               # Table styles
│   │
│   └── js/
│       ├── common.js               # Utility functions
│       ├── auth.js                 # Auth logic
│       ├── student.js              # Student page logic
│       ├── marks_entry.js          # Mark entry logic
│       └── prediction.js           # Prediction display logic
│
└── database.db                     # SQLite database (auto-created)
```

## API Endpoints

### Authentication
- `POST /api/auth/student/signup` - Student registration
- `POST /api/auth/student/login` - Student login
- `POST /api/auth/staff/login` - Staff/HOD login
- `POST /api/auth/student/logout` - Student logout
- `POST /api/auth/staff/logout` - Staff logout

### Student Endpoints
- `POST /api/student/add-marks` - Add subject marks
- `GET /api/student/get-semester-marks/<sem>` - Get semester marks
- `GET /api/student/get-all-marks` - Get all marks
- `GET /api/student/predict/<sem>` - Generate prediction
- `GET /api/student/get-all-predictions` - Get prediction history
- `POST /api/student/upload-certificate` - Upload certificate
- `GET /api/student/get-certifications` - Get certificates
- `POST /api/student/upload-competition` - Upload competition record
- `GET /api/student/get-competitions` - Get competitions

### Staff/HOD Endpoints
- `GET /api/staff/all-predictions` - View all predictions
- `GET /api/staff/student-details/<id>` - View student details
- `GET /api/staff/search-student` - Search student by roll number
- `GET /api/staff/department-stats` - Department statistics (HOD only)
- `GET /api/staff/filter-students` - Filter students

## Usage Guide

### For Students

1. **Sign Up**
   - Go to Student Signup
   - Enter name, roll number, department, year
   - Create password

2. **Enter Marks**
   - Login to dashboard
   - Click "Enter Marks"
   - Select semester
   - Add subjects one by one with marks, attendance, internal marks, assignment scores
   - Save semester

3. **View Predictions**
   - Click "View Predictions"
   - See ML-predicted performance category and score
   - Review prediction history

4. **Upload Profile**
   - Click "Upload Certificates"
   - Add certifications and competition achievements
   - View uploaded documents

### For Staff

1. **Login**
   - Go to Staff Login
   - Enter username and password

2. **Monitor Students**
   - View all students and their predictions
   - Search for specific students
   - View detailed academic records

### For HOD

1. **Access Dashboard**
   - Login as HOD
   - View department statistics
   - Filter students by year or department
   - Generate reports

## Machine Learning Model

### Algorithm: Linear Regression
- Uses marks, attendance, internal marks, and assignment scores as features
- Predicts performance score (0-100)
- Automatically trained on startup

### Training Data
- Located in `backend/training_data.csv`
- 50 sample records for initial training
- Expandable with more data

### Prediction Formula (Rule-Based Fallback)
```
Score = (Marks × 0.40) + (Attendance × 0.30) + 
        (Internal/50 × 0.20) + (Assignment/20 × 0.10)
```

## Database Schema

### Students Table
- student_id, name, roll_no, department, year, password_hash, email, created_at

### Marks Table
- mark_id, student_id, semester, subject_name, marks_obtained, attendance_percentage, internal_marks, assignment_score, entry_date

### Predictions Table
- prediction_id, student_id, semester, prediction_result, prediction_score, generated_at

### Certifications Table
- cert_id, student_id, cert_title, cert_file_path, issue_date, upload_date

### Competitions Table
- comp_id, student_id, comp_title, achievement_type, comp_file_path, event_date, upload_date

### Staff Table
- staff_id, name, username, password_hash, department, role, created_at

## Department List

1. Computer Science and Engineering
2. Electronics and Communication
3. Electrical and Electronics
4. Mechanical Engineering
5. Civil Engineering
6. Information Technology
7. Biotechnology
8. Textile Technology

## Important Notes

⚠️ **ML Model Separation**: Certificates and competition details do NOT influence the ML prediction. They are maintained purely for academic profile review.

✅ **Prediction Accuracy**: Based only on:
- Attendance percentage
- Internal examination marks
- Assignment scores
- Final marks obtained

## Troubleshooting

### Database Issues
- Delete `database.db` and restart the application
- Database will be recreated automatically

### ML Model Not Training
- Check `backend/training_data.csv` format
- Ensure all columns are present

### Port Already in Use
- Change port in app.py: `app.run(..., port=5001)`

## Default Test Credentials

For testing, you can create users through the signup form or add them directly to the database.

## Future Enhancements

- Email notifications
- Advanced analytics and charts
- Batch student import
- PDF report generation
- Student performance trends
- Automated alerts for at-risk students

## License

This project is for educational purposes.

## Support

For issues or questions, please contact the development team.
# student_-performance
