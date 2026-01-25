/* Authentication JavaScript */

// Helper function to handle form submission
function handleLoginSubmit(formElement, endpoint, redirectUrl) {
    formElement.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const formData = new FormData(this);
        const data = Object.fromEntries(formData);
        
        fetch(endpoint, {
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
                // Show error
                showNotification(result.error, 'error');
            } else {
                // Store in sessionStorage
                Object.keys(result).forEach(key => {
                    if (key !== 'message') {
                        sessionStorage.setItem(key, result[key]);
                    }
                });
                
                showNotification(result.message, 'success');
                setTimeout(() => {
                    window.location.href = redirectUrl;
                }, 1000);
            }
        })
        .catch(error => {
            showNotification('An error occurred: ' + error, 'error');
        });
    });
}

// Logout user
function logoutUser(userType = 'student') {
    const endpoint = userType === 'student' ? 
        '/api/auth/student/logout' : 
        '/api/auth/staff/logout';
    
    fetch(endpoint, {
        method: 'POST',
        credentials: 'same-origin'
    })
    .then(response => response.json())
    .then(data => {
        sessionStorage.clear();
        window.location.href = '/';
    });
}

// For signup form - additional validation
function validateSignupForm(formData) {
    if (formData.password !== formData.confirm_password) {
        showNotification('Passwords do not match!', 'error');
        return false;
    }
    
    if (formData.password.length < 6) {
        showNotification('Password must be at least 6 characters!', 'error');
        return false;
    }
    
    return true;
}
