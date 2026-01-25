/* Mark Entry JavaScript */

let currentSemester = null;
let subjectsCount = 0;

document.addEventListener('DOMContentLoaded', function() {
    const semesterSelect = document.getElementById('semesterSelect');
    
    const handleSemesterChange = function() {
        currentSemester = this.value;
        
        if (currentSemester) {
            document.getElementById('marksForm').style.display = 'block';
            document.getElementById('semesterTitle').textContent = currentSemester;
            
            // Clear previous subjects
            document.getElementById('subjectsContainer').innerHTML = '';
            subjectsCount = 0;
            
            // Add one default subject to start
            addSubject();
        } else {
            document.getElementById('marksForm').style.display = 'none';
        }
    };
    
    semesterSelect.addEventListener('change', handleSemesterChange);
    
    // Trigger on page load if semester is already selected
    if (semesterSelect.value) {
        handleSemesterChange.call(semesterSelect);
    }
    
    document.getElementById('addSubjectBtn').addEventListener('click', addSubject);
    document.getElementById('saveSemesterBtn').addEventListener('click', saveSemester);
    
    loadMarkHistory();
});

function addSubject() {
    subjectsCount++;
    renderSubjectGrid();
}

function renderSubjectGrid() {
    const container = document.getElementById('subjectsContainer');
    
    const subjectHtml = `
        <div class="subject-card" id="subject_${subjectsCount}">
            <div class="subject-header">
                <h4>Subject ${subjectsCount}</h4>
                <button type="button" class="btn-remove" onclick="removeSubject(${subjectsCount})">✕</button>
            </div>
            
            <div class="form-group">
                <label>Subject Name *</label>
                <input type="text" class="subject-name" placeholder="e.g., Mathematics" required>
            </div>
            
            <div class="form-row">
                <div class="form-group">
                    <label>Marks (0-100) *</label>
                    <input type="number" class="marks-obtained" min="0" max="100" required>
                </div>
                <div class="form-group">
                    <label>Attendance % *</label>
                    <input type="number" class="attendance" min="0" max="100" required>
                </div>
            </div>
            
            <div class="form-row">
                <div class="form-group">
                    <label>Internal (0-50) *</label>
                    <input type="number" class="internal-marks" min="0" max="50" required>
                </div>
                <div class="form-group">
                    <label>Assignment (0-20) *</label>
                    <input type="number" class="assignment-score" min="0" max="20" required>
                </div>
            </div>
        </div>
    `;
    
    container.insertAdjacentHTML('beforeend', subjectHtml);
}

function removeSubject(id) {
    const element = document.getElementById('subject_' + id);
    if (element) {
        element.remove();
    }
}

function saveSemester() {
    const errorDiv = document.getElementById('errorMessage');
    const successDiv = document.getElementById('successMessage');
    
    // Get all subjects
    const subjects = document.querySelectorAll('.subject-card');
    
    if (subjects.length === 0) {
        errorDiv.textContent = 'Please add at least one subject!';
        errorDiv.style.display = 'block';
        return;
    }
    
    let allValid = true;
    
    // Validate and save each subject
    subjects.forEach((subject, index) => {
        const name = subject.querySelector('.subject-name').value;
        const marks = parseFloat(subject.querySelector('.marks-obtained').value);
        const attendance = parseFloat(subject.querySelector('.attendance').value);
        const internal = parseFloat(subject.querySelector('.internal-marks').value);
        const assignment = parseFloat(subject.querySelector('.assignment-score').value);
        
        if (!name || !marks || !attendance || !internal || assignment === '') {
            errorDiv.textContent = 'Please fill all fields for all subjects!';
            errorDiv.style.display = 'block';
            allValid = false;
            return;
        }
        
        // Send to backend
        const data = {
            semester: parseInt(currentSemester),
            subject_name: name,
            marks_obtained: marks,
            attendance_percentage: attendance,
            internal_marks: internal,
            assignment_score: assignment
        };
        
        fetch('/api/student/add-marks', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data),
            credentials: 'same-origin'
        })
        .then(response => response.json())
        .then(result => {
            if (result.error) {
                errorDiv.textContent = result.error;
                errorDiv.style.display = 'block';
                allValid = false;
            }
        })
        .catch(error => {
            errorDiv.textContent = 'Error saving marks: ' + error;
            errorDiv.style.display = 'block';
            allValid = false;
        });
    });
    
    if (allValid) {
        successDiv.textContent = 'Semester marks saved successfully!';
        successDiv.style.display = 'block';
        
        setTimeout(() => {
            document.getElementById('subjectsContainer').innerHTML = '';
            subjectsCount = 0;
            document.getElementById('semesterSelect').value = '';
            document.getElementById('marksForm').style.display = 'none';
            loadMarkHistory();
        }, 1500);
    }
}

function loadExistingMarks() {
    fetch('/api/student/get-semester-marks/' + currentSemester, {
        credentials: 'same-origin'
    })
    .then(response => response.json())
    .then(data => {
        const container = document.getElementById('subjectsContainer');
        container.innerHTML = '';
        
        if (data.marks && data.marks.length > 0) {
            let html = '<h4>Existing Marks:</h4>';
            data.marks.forEach(mark => {
                html += `
                    <div class="existing-mark">
                        <p><strong>${mark.subject_name}</strong></p>
                        <p>Marks: ${mark.marks_obtained}, Attendance: ${mark.attendance_percentage}%, Internal: ${mark.internal_marks}, Assignment: ${mark.assignment_score}</p>
                    </div>
                `;
            });
            container.innerHTML = html + '<hr>';
        }
    });
}

function loadMarkHistory() {
    fetch('/api/student/get-all-marks', {
        credentials: 'same-origin'
    })
    .then(response => response.json())
    .then(data => {
        const historyContent = document.getElementById('historyContent');
        
        if (Object.keys(data).length === 0) {
            historyContent.innerHTML = '<p>No marks entered yet</p>';
            return;
        }
        
        let html = '';
        for (const [semester, marks] of Object.entries(data)) {
            html += `<div class="semester-history"><h4>Semester ${semester}</h4><ul>`;
            marks.forEach(mark => {
                html += `<li>${mark.subject_name}: ${mark.marks_obtained}/100 (Attendance: ${mark.attendance_percentage}%)</li>`;
            });
            html += '</ul></div>';
        }
        
        historyContent.innerHTML = html;
    });
}

// Add styles for subject card grid
const marksGridStyle = document.createElement('style');
marksGridStyle.textContent = `
    #subjectsContainer {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 1.5rem;
        margin-bottom: 2rem;
    }
    
    @media (max-width: 768px) {
        #subjectsContainer {
            grid-template-columns: 1fr;
        }
    }
    
    .subject-card {
        background: var(--light-bg);
        padding: 1.5rem;
        border-radius: 8px;
        border-left: 4px solid var(--secondary-color);
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    
    .subject-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 1rem;
    }
    
    .subject-header h4 {
        color: var(--primary-color);
        margin: 0;
    }
    
    .btn-remove {
        background: #e74c3c;
        color: white;
        border: none;
        width: 30px;
        height: 30px;
        border-radius: 50%;
        cursor: pointer;
        font-size: 18px;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    
    .btn-remove:hover {
        background: #c0392b;
    }
    
    .form-row {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 1rem;
    }
    
    .existing-mark {
        background: white;
        padding: 1rem;
        margin-bottom: 0.5rem;
        border-radius: 5px;
        border-left: 3px solid var(--tertiary-color);
    }
    
    .semester-history {
        margin-bottom: 2rem;
        padding: 1rem;
        background: white;
        border-radius: 8px;
    }
`;
document.head.appendChild(marksGridStyle);
