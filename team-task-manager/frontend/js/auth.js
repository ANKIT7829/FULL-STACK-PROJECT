/**
 * Authentication Helper Functions
 * Handles user authentication and session management
 */

/**
 * Check if user is authenticated
 * @returns {boolean} True if token exists
 */
function isAuthenticated() {
    return !!localStorage.getItem('token');
}

/**
 * Get current user
 * @returns {object} User object
 */
function getCurrentUser() {
    const userStr = localStorage.getItem('user');
    return userStr ? JSON.parse(userStr) : null;
}

/**
 * Check if current user is admin
 * @returns {boolean} True if user role is admin
 */
function isAdmin() {
    const user = getCurrentUser();
    return user && user.role === 'admin';
}

/**
 * Logout user
 */
function logout() {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    window.location.href = 'index.html';
}

/**
 * Check authentication on page load
 * Redirect to login if not authenticated
 */
function checkAuthentication() {
    if (!isAuthenticated()) {
        window.location.href = 'index.html';
    } else {
        // Update user name in navbar
        const user = getCurrentUser();
        const userElements = document.querySelectorAll('#userName');
        userElements.forEach(el => {
            el.textContent = user.name || 'User';
        });
        
        // Setup logout button
        const logoutBtns = document.querySelectorAll('#logoutBtn');
        logoutBtns.forEach(btn => {
            btn.addEventListener('click', logout);
        });
    }
}

/**
 * Initialize on page load
 */
document.addEventListener('DOMContentLoaded', checkAuthentication);
