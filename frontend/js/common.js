/* Common JavaScript Utilities */

// Check user session and redirect if not logged in
function checkUserSession() {
    fetch('/api/auth/check-session', {
        credentials: 'same-origin'
    })
    .then(response => response.json())
    .then(data => {
        const navLogout = document.getElementById('navLogout');
        
        if (data.logged_in) {
            if (navLogout) {
                navLogout.style.display = 'inline';
                navLogout.addEventListener('click', function(e) {
                    e.preventDefault();
                    logout();
                });
            }
        } else {
            const currentPage = window.location.pathname;
            // Only redirect from protected pages (dashboard, marks, prediction, etc.)
            // Allow access to login and signup pages
            const protectedPages = ['/student/dashboard', '/student/semester', '/student/prediction', '/student/profile',
                                   '/staff/dashboard', '/hod/dashboard'];
            if (protectedPages.some(page => currentPage.includes(page))) {
                window.location.href = '/';
            }
        }
    });
}

// Logout function
function logout() {
    const userType = sessionStorage.getItem('role') ? 'staff' : 'student';
    const endpoint = userType === 'staff' ? '/api/auth/staff/logout' : '/api/auth/student/logout';
    
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

// Format date to YYYY-MM-DD
function formatDate(date) {
    if (!date) return '';
    if (typeof date === 'string') {
        return date.split(' ')[0];
    }
    const d = new Date(date);
    let month = '' + (d.getMonth() + 1);
    let day = '' + d.getDate();
    const year = d.getFullYear();

    if (month.length < 2) month = '0' + month;
    if (day.length < 2) day = '0' + day;

    return [year, month, day].join('-');
}

// Format date to readable format
function formatDateReadable(dateStr) {
    const date = new Date(dateStr);
    const options = { year: 'numeric', month: 'short', day: 'numeric' };
    return date.toLocaleDateString('en-US', options);
}

// Capitalize first letter
function capitalize(str) {
    if (!str) return '';
    return str.charAt(0).toUpperCase() + str.slice(1);
}

// Show notification
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = type + '-message';
    notification.textContent = message;
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 15px 20px;
        border-radius: 5px;
        z-index: 1000;
        animation: slideIn 0.3s ease;
    `;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease';
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

// Theme Management
function initTheme() {
    const savedTheme = localStorage.getItem('theme') || 'light';
    document.documentElement.setAttribute('data-theme', savedTheme);
    updateThemeIcon(savedTheme);
}

function toggleTheme() {
    const currentTheme = document.documentElement.getAttribute('data-theme');
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    
    document.documentElement.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);
    updateThemeIcon(newTheme);
}

function updateThemeIcon(theme) {
    const icon = document.getElementById('themeIcon');
    if (icon) {
        icon.textContent = theme === 'dark' ? '☀️' : '🌙';
    }
}

// Initialize theme on load
document.addEventListener('DOMContentLoaded', initTheme);

// Add CSS animation
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from { transform: translateX(400px); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    @keyframes slideOut {
        from { transform: translateX(0); opacity: 1; }
        to { transform: translateX(400px); opacity: 0; }
    }
`;
document.head.appendChild(style);

// Validate email
function isValidEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

// API helper function
async function apiCall(endpoint, method = 'GET', data = null) {
    const options = {
        method: method,
        credentials: 'same-origin',
        headers: {
            'Content-Type': 'application/json'
        }
    };
    
    if (data) {
        options.body = JSON.stringify(data);
    }
    
    try {
        const response = await fetch(endpoint, options);
        return await response.json();
    } catch (error) {
        console.error('API call failed:', error);
        throw error;
    }
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    checkUserSession();
});
