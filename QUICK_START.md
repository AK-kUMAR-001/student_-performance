# 📘 QUICK REFERENCE GUIDE - Student Performance Predictor

## 🚀 START HERE

### Option 1: Using Python Script (Recommended)
```bash
cd /home/a/Desktop/Student_Performence
python run.py
```

### Option 2: Manual Start
```bash
cd /home/a/Desktop/Student_Performence
pip install -r requirements.txt
python app.py
```

### Open Browser
```
http://localhost:5000
```

---

## 🎯 KEY PAGES

### For Students
| Page | URL | Purpose |
|------|-----|---------|
| Home | `/` | Landing page |
| Signup | `/student/signup` | Create account |
| Login | `/student/login` | Access account |
| Dashboard | `/student/dashboard` | Main hub |
| Marks Entry | `/student/marks-entry` | Add marks |
| Predictions | `/student/prediction` | View results |
| Certifications | `/student/certifications` | Upload files |
| Profile | `/student/profile` | View profile |

### For Staff
| Page | URL | Purpose |
|------|-----|---------|
| Login | `/staff/login` | Staff access |
| Dashboard | `/staff/dashboard` | Monitor students |

### For HOD
| Page | URL | Purpose |
|------|-----|---------|
| Login | `/hod/login` | HOD access |
| Dashboard | `/hod/dashboard` | Department view |

---

## 📝 MARK ENTRY EXAMPLE

**Semester 1 - Mathematics**
- Subject Name: Mathematics
- Marks Obtained: 85
- Attendance %: 90
- Internal Marks: 40
- Assignment Score: 18
- **Prediction Score**: ~82% (Good Performance)

---

## 🔑 PREDICTION FORMULA

```
Score = (Marks × 0.40) + 
        (Attendance × 0.30) + 
        (Internal/50 × 0.20) + 
        (Assignment/20 × 0.10)

75-100  → ✅ Good Performance
50-74   → ⚠️ Average Performance
0-49    → ❌ At-Risk Performance
```

---

## 👥 USER ROLES & PERMISSIONS

### Student Can:
- ✅ Register & Login
- ✅ Add marks (6 semesters)
- ✅ View predictions
- ✅ Upload certificates
- ✅ View academic profile
- ❌ Cannot view other students

### Staff Can:
- ✅ Login
- ✅ View all predictions
- ✅ Search students
- ✅ View student details
- ✅ Monitor by year/dept
- ❌ Cannot edit marks

### HOD Can:
- ✅ All staff permissions
- ✅ View department stats
- ✅ Analytics dashboard
- ✅ All student records
- ❌ Cannot edit data

---

## 🗄️ DEPARTMENTS (Select During Signup)

1. Computer Science and Engineering
2. Electronics and Communication
3. Electrical and Electronics
4. Mechanical Engineering
5. Civil Engineering
6. Information Technology
7. Biotechnology
8. Textile Technology

---

## 📊 DATABASE STRUCTURE

### Tables
- **Students** - User accounts
- **Marks** - Subject grades
- **Predictions** - ML results
- **Certifications** - Uploaded certs
- **Competitions** - Achievements
- **Staff** - Admin accounts

---

## 🔐 SECURITY NOTES

✅ Passwords hashed with SHA-256
✅ Session-based authentication
✅ File type validation
✅ File size limit: 16MB
✅ Role-based access control

---

## ⚡ COMMON TASKS

### Create Student Account
1. Go to `/student/signup`
2. Fill registration form
3. Click Register
4. Login with credentials

### Enter Marks
1. Dashboard → "Enter Marks"
2. Select semester
3. Add subjects
4. Save

### Get Prediction
1. Go to "View Predictions"
2. Select semester
3. View results

### Upload Certificate
1. Go to "Upload Certificates"
2. Select "Certificates" tab
3. Add title & date
4. Upload file

---

## 🧮 ML MODEL INFO

**Algorithm**: Linear Regression
**Training Data**: 50 sample records
**Features**: 
- Marks Obtained
- Attendance %
- Internal Marks
- Assignment Score

**Auto-trains on first run**

---

## 📱 SUPPORTED DEVICES

✅ Desktop (1200px+)
✅ Tablet (768px+)
✅ Mobile (360px+)
✅ All modern browsers

---

## 🐛 TROUBLESHOOTING

### "Port 5000 already in use"
```bash
lsof -i :5000
kill -9 <PID>
```

### "No module named 'flask'"
```bash
pip install -r requirements.txt
```

### "Database locked"
```bash
rm database.db
python app.py
```

### Files not uploading
- Check file size (<16MB)
- Check file type (PDF, PNG, JPG, GIF)
- Check uploads/ folder exists

---

## 📂 PROJECT FILES

```
Student_Performence/
├── app.py                    ← Main app
├── run.py                    ← Quick start
├── config.py                 ← Settings
├── models.py                 ← Database
├── requirements.txt          ← Dependencies
├── README.md                 ← Full docs
├── SETUP.md                  ← Setup guide
├── COMPLETION_CHECKLIST.md   ← Checklist
├── PROJECT_SUMMARY.md        ← Summary
└── backend/
    └── prediction_model.py   ← ML engine
```

---

## 🚀 DEPLOYMENT

To deploy:
1. Set `debug=False` in app.py
2. Use production WSGI server (gunicorn)
3. Configure database backup
4. Set SECRET_KEY in config.py
5. Use HTTPS in production

---

## 📞 API ENDPOINTS QUICK LIST

### Auth
- POST `/api/auth/student/signup`
- POST `/api/auth/student/login`
- POST `/api/auth/staff/login`

### Marks
- POST `/api/student/add-marks`
- GET `/api/student/get-all-marks`

### Prediction
- GET `/api/student/predict/<sem>`
- GET `/api/student/get-all-predictions`

### Files
- POST `/api/student/upload-certificate`
- POST `/api/student/upload-competition`

### Staff
- GET `/api/staff/all-predictions`
- GET `/api/staff/search-student`

---

## ✨ KEY FEATURES SUMMARY

✅ ML-based performance prediction
✅ 6-semester mark entry
✅ Role-based access control
✅ Certificate management
✅ Real-time predictions
✅ Responsive design
✅ Secure authentication
✅ Student monitoring (staff/HOD)

---

## 🎓 IMPORTANT REMINDER

**"Certificates and competition details are maintained as academic profile records and are not used in performance prediction."**

Prediction uses ONLY:
- Marks obtained
- Attendance %
- Internal marks
- Assignment scores

---

## 💡 TIPS & TRICKS

1. **Bulk Testing**: Use same credentials with different semester data
2. **Export Data**: Staff can view all predictions at once
3. **Filtering**: HOD can filter by year or department
4. **Search**: Quickly find students by roll number
5. **History**: All predictions are saved with timestamps

---

## 📊 TYPICAL STUDENT JOURNEY

1. **Day 1**: Signup on website
2. **Week 1**: Add marks for Semester 1
3. **After Input**: Get instant prediction
4. **Optional**: Upload certification
5. **End of Semester**: View performance trend

---

## 🎯 WHAT'S NEXT?

1. Start the app with `python run.py`
2. Create test student account
3. Add marks for a semester
4. Check the prediction
5. Try uploading a certificate
6. Explore staff dashboard

---

## 📞 HELP & SUPPORT

- Full docs: See `README.md`
- Setup help: See `SETUP.md`
- API info: Check `backend/routes/*.py`
- Code: Well-commented throughout

---

## ✅ QUICK CHECKLIST

- [ ] Python 3.7+ installed
- [ ] In correct directory
- [ ] Ran `pip install -r requirements.txt`
- [ ] Started app with `python run.py` or `python app.py`
- [ ] Opened `http://localhost:5000`
- [ ] Created student account
- [ ] Added marks
- [ ] Got prediction
- [ ] Explored all features

---

## 🎉 YOU'RE ALL SET!

Everything is ready to use. Start exploring! 🚀

**Questions?** Check README.md or SETUP.md

**Issues?** See Troubleshooting section above

**Ready to demo?** You're all set for viva! 📊✨

---

**Happy learning! 🎓**
