# Student Performance Predictor - SETUP GUIDE

## Quick Start (3 Steps)

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Run Application
```bash
python app.py
```

### Step 3: Open Browser
Visit `http://localhost:5000`

---

## First Time Setup

### Option A: Automatic Setup (Linux/Mac)
```bash
chmod +x setup.sh
./setup.sh
```

### Option B: Manual Setup (All Platforms)

1. **Install Python packages**
   ```bash
   pip install -r requirements.txt
   ```

2. **Start the app** (database will be created automatically)
   ```bash
   python app.py
   ```

3. **Open in browser**
   ```
   http://localhost:5000
   ```

---

## First User Accounts

### Create Student Account
1. Go to Home Page
2. Click "Student" → "Student Signup"
3. Fill registration form:
   - Name: John Doe
   - Roll No: CSE001
   - Department: Computer Science and Engineering
   - Year: 1
   - Password: password123
4. Click Register
5. Login with credentials

### Create Staff/HOD Account
1. Stop the app (Ctrl+C)
2. Open Python interactive terminal:
   ```bash
   python
   ```

3. Execute:
   ```python
   from app import app, db
   from models import Staff
   
   with app.app_context():
       staff = Staff(
           name='Prof. Smith',
           username='staff001',
           department='Computer Science and Engineering',
           role='staff'
       )
       staff.set_password('staffpass123')
       db.session.add(staff)
       db.session.commit()
       print("Staff account created!")
   ```

4. Exit Python and restart app:
   ```bash
   python app.py
   ```

---

## Testing the System

### Test Student Workflow
1. **Login** as student
2. **Add Marks**: Go to Mark Entry
   - Semester: 1
   - Subject: Mathematics
   - Marks: 85
   - Attendance: 90%
   - Internal: 40
   - Assignment: 18
   - Save
3. **View Prediction**: Click "View Predictions"
4. **Upload Certificate**: Click "Upload Certificates"
5. **View Profile**: Click "View Profile"

### Test Staff Workflow
1. **Login** as staff (staff001/staffpass123)
2. **View Students**: See all student predictions
3. **Search Student**: Search by roll number
4. **View Details**: Click on student to see full record

### Test HOD Workflow
1. Create HOD account (role='hod')
2. **View Stats**: See department statistics
3. **Filter Students**: By year and department
4. **View Records**: Access all student data

---

## File Uploads

- **Location**: `uploads/` folder
- **Supported**: PDF, PNG, JPG, JPEG, GIF
- **Max Size**: 16MB

---

## Database Location

- **SQLite**: `database.db` (auto-created in project root)
- **Reset**: Delete `database.db` and restart app

---

## Ports & Configuration

- **Default Port**: 5000
- **Change Port**: Edit `app.py` last line
  ```python
  app.run(debug=True, port=5001)
  ```

---

## Project Structure

```
Student_Performence/
├── app.py
├── config.py
├── models.py
├── requirements.txt
├── README.md
├── SETUP.md
├── setup.sh
├── database.db
├── uploads/
├── backend/
│   ├── prediction_model.py
│   ├── training_data.csv
│   └── routes/
├── frontend/
│   ├── html/
│   ├── css/
│   └── js/
```

---

## Troubleshooting

### "Port 5000 already in use"
```bash
# Find process using port 5000
lsof -i :5000
# Kill it
kill -9 <PID>
# Or change port in app.py
```

### "ModuleNotFoundError: No module named 'flask'"
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### "Database locked"
```bash
# Delete database and restart
rm database.db
python app.py
```

### "ML model not training"
- Check `backend/training_data.csv` exists
- Verify CSV columns match expected format
- Check console for error messages

---

## Key Features Summary

✅ **Student Features**
- Semester-wise mark entry
- Real-time ML predictions
- Certificate upload
- Academic profile

✅ **Staff Features**
- Monitor all students
- View performance trends
- Search by roll number
- Department oversight

✅ **HOD Features**
- Department statistics
- Student filtering
- Complete data access
- Analytics

---

## Important Notes

⚠️ **Remember**: Certificates and competitions do NOT affect the ML prediction!

Prediction is ONLY based on:
- Marks obtained
- Attendance percentage
- Internal exam marks
- Assignment scores

---

## Need Help?

1. Check README.md for detailed documentation
2. See API endpoints in documentation
3. Check console for error messages
4. Verify all dependencies installed

---

Happy Predicting! 🎓📊
