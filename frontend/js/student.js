/* Student Dashboard JavaScript */

let studentStats = {
    currentScore: 0,
    semesterCount: 0
};

document.addEventListener('DOMContentLoaded', function() {
    // Always try to load profile data if profile elements exist
    if (document.getElementById('profileName')) {
        loadProfile();
        loadMarksHistory();
        loadPredictionHistory();
        loadCertifications();
        loadCompetitions();
        return; // Exit early for profile page
    }
    
    // Load student info from sessionStorage for dashboard
    const studentName = sessionStorage.getItem('name');
    const studentRoll = sessionStorage.getItem('roll_no');
    const studentDept = sessionStorage.getItem('department');
    const studentYear = sessionStorage.getItem('year');
    
    if (studentName) {
        document.getElementById('welcomeName').textContent = 'Welcome, ' + studentName;
        document.getElementById('studentName').textContent = studentName;
        document.getElementById('studentRoll').textContent = studentRoll || '-';
        document.getElementById('studentDept').textContent = studentDept || '-';
        document.getElementById('studentYear').textContent = studentYear || '-';
        
        loadSummary();
        loadProfile();
        loadMarksHistory();
        loadPredictionHistory();
        loadCertifications();
        loadCompetitions();
    } else {
        // If no session data, redirect to login
        window.location.href = '/student/login';
    }
    
    // Logout handler
    const logoutLink = document.getElementById('navLogout');
    if (logoutLink) {
        logoutLink.addEventListener('click', function(e) {
            e.preventDefault();
            logout();
        });
    }
});

function loadSummary() {
    // Load latest prediction
    fetch('/api/student/get-all-predictions', {
        credentials: 'same-origin'
    })
    .then(response => response.json())
    .then(data => {
        if (data.predictions && data.predictions.length > 0) {
            const latest = data.predictions[data.predictions.length - 1];
            document.getElementById('currentPred').textContent = latest.category;
            document.getElementById('latestScore').textContent = latest.score;
            document.getElementById('semesterCount').textContent = data.predictions.length;
            
            // Store for simulator
            studentStats.currentScore = latest.score; // Using latest score as proxy for average if cumulative not available
            studentStats.semesterCount = data.predictions.length;
        }
    })
    .catch(error => console.error('Error loading predictions:', error));
}

// Simulator Functions
function openSimulator() {
    document.getElementById('simulatorModal').style.display = 'block';
    document.getElementById('simCurrentScore').value = studentStats.currentScore || 0;
    document.getElementById('simResult').style.display = 'none';
}

function closeSimulator() {
    document.getElementById('simulatorModal').style.display = 'none';
}

function calculateWhatIf() {
    const currentScore = parseFloat(document.getElementById('simCurrentScore').value) || 0;
    const targetScore = parseFloat(document.getElementById('simTargetScore').value);
    const semCount = studentStats.semesterCount || 1;
    
    if (isNaN(targetScore) || targetScore < 0 || targetScore > 100) {
        alert("Please enter a valid target score (0-100)");
        return;
    }

    // Simple Average Calculation: (Current * N + Target) / (N + 1)
    // Assuming 'currentScore' is cumulative average. If it's just latest sem, this is an approximation.
    const newAverage = ((currentScore * semCount) + targetScore) / (semCount + 1);
    
    const resultBox = document.getElementById('simResult');
    resultBox.style.display = 'block';
    
    let color = '#f39c12'; // Average
    let text = 'Average';
    
    if (newAverage >= 70) {
        color = '#2ecc71';
        text = 'Good';
        resultBox.className = 'alert-box success';
    } else if (newAverage < 50) {
        color = '#e74c3c';
        text = 'At Risk';
        resultBox.className = 'alert-box error';
    } else {
        resultBox.className = 'alert-box warning';
    }
    
    resultBox.style.backgroundColor = color + '22'; // Add transparency
    resultBox.style.border = '1px solid ' + color;
    resultBox.style.color = color;
    
    resultBox.innerHTML = `
        <strong>New Projected Average:</strong> ${newAverage.toFixed(2)}% <br>
        <strong>Status:</strong> ${text}
    `;
}


function loadProfile() {
    // First try to load from sessionStorage
    const name = sessionStorage.getItem('name');
    const rollNo = sessionStorage.getItem('roll_no');
    const dept = sessionStorage.getItem('department');
    const year = sessionStorage.getItem('year');
    
    if (document.getElementById('profileName')) {
        document.getElementById('profileName').textContent = name || '-';
        document.getElementById('profileRoll').textContent = rollNo || '-';
        document.getElementById('profileDept').textContent = dept || '-';
        document.getElementById('profileYear').textContent = year || '-';
    }
    
    // Then fetch additional data from API
    fetch('/api/student/get-profile', {
        credentials: 'same-origin'
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) return;
        
        if (document.getElementById('profileName')) {
            document.getElementById('profileName').textContent = data.name || name || '-';
            document.getElementById('profileRoll').textContent = data.roll_no || rollNo || '-';
            document.getElementById('profileDept').textContent = data.department || dept || '-';
            document.getElementById('profileYear').textContent = data.year || year || '-';
            document.getElementById('profileEmail').textContent = data.email || 'N/A';
        }
    })
    .catch(error => console.error('Error loading profile:', error));
}

function loadCertifications() {
    fetch('/api/student/get-certifications', {
        credentials: 'same-origin'
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) return;
        
        const container = document.getElementById('certificationsContent');
        if (!container) return;
        
        if (data.certifications && data.certifications.length > 0) {
            let html = '<div class="cert-list">';
            data.certifications.forEach(cert => {
                html += `
                    <div class="item-card">
                        <h4>${cert.title}</h4>
                        <p><strong>Issue Date:</strong> ${formatDateReadable(cert.issue_date)}</p>
                        <p><strong>Upload Date:</strong> ${formatDateReadable(cert.upload_date)}</p>
                        <a href="${cert.file_path}" target="_blank" class="btn btn-sm btn-primary">View Document</a>
                    </div>
                `;
            });
            html += '</div>';
            container.innerHTML = html;
        } else {
            container.innerHTML = '<p>No certifications uploaded yet.</p>';
        }
    })
    .catch(error => console.error('Error loading certifications:', error));
}

function loadCompetitions() {
    fetch('/api/student/get-competitions', {
        credentials: 'same-origin'
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) return;
        
        const container = document.getElementById('competitionsContent');
        if (!container) return;
        
        if (data.competitions && data.competitions.length > 0) {
            let html = '<div class="comp-list">';
            data.competitions.forEach(comp => {
                html += `
                    <div class="item-card">
                        <h4>${comp.title}</h4>
                        <p><strong>Achievement:</strong> ${comp.achievement_type}</p>
                        <p><strong>Event Date:</strong> ${formatDateReadable(comp.event_date)}</p>
                        <a href="${comp.file_path}" target="_blank" class="btn btn-sm btn-primary">View Evidence</a>
                    </div>
                `;
            });
            html += '</div>';
            container.innerHTML = html;
        } else {
            container.innerHTML = '<p>No competitions recorded yet.</p>';
        }
    })
    .catch(error => console.error('Error loading competitions:', error));
}

function loadMarksHistory() {
    fetch('/api/student/get-all-marks', {
        credentials: 'same-origin'
    })
    .then(response => response.json())
    .then(data => {
        const container = document.getElementById('marksHistoryContent');
        if (!container) return;
        
        if (Object.keys(data).length === 0) {
            container.innerHTML = '<p>No marks entered yet.</p>';
            return;
        }
        
        let html = '<div class="marks-table">';
        for (const [semester, marks] of Object.entries(data)) {
            html += `<div class="semester-block"><h4>Semester ${semester}</h4><table><tr><th>Subject</th><th>Marks</th><th>Attendance %</th><th>Internal</th><th>Assignment</th></tr>`;
            marks.forEach(mark => {
                html += `<tr><td>${mark.subject_name}</td><td>${mark.marks_obtained}</td><td>${mark.attendance_percentage}</td><td>${mark.internal_marks}</td><td>${mark.assignment_score}</td></tr>`;
            });
            html += '</table></div>';
        }
        html += '</div>';
        container.innerHTML = html;
    })
    .catch(error => console.error('Error loading marks:', error));
}

function loadPredictionHistory() {
    fetch('/api/student/get-all-predictions', {
        credentials: 'same-origin'
    })
    .then(response => response.json())
    .then(data => {
        const container = document.getElementById('predictionsContent');
        if (!container) return;
        
        if (!data.predictions || data.predictions.length === 0) {
            container.innerHTML = '<p>No predictions available yet.</p>';
            return;
        }
        
        let html = '<div class="predictions-grid">';
        data.predictions.forEach((pred, idx) => {
            html += `
                <div class="prediction-card">
                    <h4>Semester ${pred.semester}</h4>
                    <p><strong>Score:</strong> ${pred.score.toFixed(2)}</p>
                    <p><strong>Category:</strong> <span class="badge-${pred.category.toLowerCase()}">${pred.category}</span></p>
                    <p><small>${formatDateReadable(pred.generated_at)}</small></p>
                </div>
            `;
        });
        html += '</div>';
        container.innerHTML = html;
    })
    .catch(error => console.error('Error loading predictions:', error));
}
