/* Prediction Results JavaScript */

document.addEventListener('DOMContentLoaded', function() {
    const semesterFilter = document.getElementById('semesterFilter');
    
    semesterFilter.addEventListener('change', function() {
        loadPredictions(this.value);
    });
    
    // Load predictions on page load
    loadPredictions('');
});

function loadPredictions(semester = '') {
    // Show loading message
    document.getElementById('predictionContent').innerHTML = `
        <div class="loading">
            <p>Loading your marks and predictions...</p>
        </div>
    `;
    
    // First, get all marks to see which semesters have data
    fetch('/api/student/get-all-marks', {
        credentials: 'same-origin'
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
    })
    .then(marksData => {
        const availableSemesters = Object.keys(marksData);
        
        if (availableSemesters.length === 0) {
            document.getElementById('predictionContent').innerHTML = `
                <div class="no-data">
                    <p>No marks entered yet. Please enter your marks first.</p>
                    <a href="/student/marks-entry" class="btn btn-primary">Go to Mark Entry</a>
                </div>
            `;
            return;
        }
        
        // Get predictions
        fetch('/api/student/get-all-predictions', {
            credentials: 'same-origin'
        })
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(predictionsData => {
            displayPredictions(predictionsData.predictions, semester);
        })
        .catch(error => {
            console.error('Error loading predictions:', error);
            document.getElementById('predictionContent').innerHTML = `
                <div class="error">
                    <p>Error loading predictions: ${error.message}</p>
                    <p>Please try refreshing the page.</p>
                </div>
            `;
        });
    })
    .catch(error => {
        console.error('Error loading marks:', error);
        document.getElementById('predictionContent').innerHTML = `
            <div class="error">
                <p>Error loading marks: ${error.message}</p>
                <p>Please make sure you're logged in and try again.</p>
            </div>
        `;
    });
}

function displayPredictions(predictions, filterSemester) {
    const predictionContent = document.getElementById('predictionContent');
    const historyTable = document.getElementById('predictionHistory');
    
    // Filter predictions if semester is specified
    let filteredPredictions = predictions;
    if (filterSemester) {
        filteredPredictions = predictions.filter(p => p.semester == filterSemester);
    }
    
    if (filteredPredictions.length === 0) {
        predictionContent.innerHTML = `
            <div class="no-data">
                <p>No predictions available for this semester.</p>
                <a href="/student/marks-entry" class="btn btn-primary">Enter Marks</a>
            </div>
        `;
        historyTable.style.display = 'none';
        return;
    }
    
    // Display current prediction (latest)
    const latestPred = filteredPredictions[filteredPredictions.length - 1];
    const predClass = latestPred.category.replace(/ /g, '').toLowerCase();
    
    let categoryEmoji = '⚠️';
    if (latestPred.category === 'Good Performance') categoryEmoji = '✅';
    else if (latestPred.category === 'At-Risk Performance') categoryEmoji = '❌';
    
    predictionContent.innerHTML = `
        <div class="prediction-card ${predClass}">
            <h3>Semester ${latestPred.semester} Prediction</h3>
            <div class="prediction-score">
                <div class="score-item">
                    <span class="score-label">Status</span>
                    <span class="score-value">${categoryEmoji} ${latestPred.category}</span>
                </div>
                <div class="score-item">
                    <span class="score-label">Prediction Score</span>
                    <span class="score-value">${latestPred.score}%</span>
                </div>
            </div>
            <p>Generated on: ${formatDateReadable(latestPred.generated_at)}</p>
        </div>
    `;
    
    // Display history table
    const tableBody = document.getElementById('historyTableBody');
    let tableHtml = '';
    
    predictions.forEach(pred => {
        let statusBadge = '⚠️ Average';
        if (pred.category === 'Good Performance') statusBadge = '✅ Good';
        else if (pred.category === 'At-Risk Performance') statusBadge = '❌ At-Risk';
        
        tableHtml += `
            <tr>
                <td data-label="Semester">${pred.semester}</td>
                <td data-label="Category">${pred.category}</td>
                <td data-label="Score">${pred.score}</td>
                <td data-label="Status"><span class="status-badge ${pred.category.replace(/ /g, '').toLowerCase()}">${statusBadge}</span></td>
            </tr>
        `;
    });
    
    tableBody.innerHTML = tableHtml;
    historyTable.style.display = 'block';
}

// Add animation to prediction card
const style = document.createElement('style');
style.textContent = `
    .prediction-card {
        animation: slideDown 0.5s ease;
    }
    
    @keyframes slideDown {
        from {
            opacity: 0;
            transform: translateY(-20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
`;
document.head.appendChild(style);
